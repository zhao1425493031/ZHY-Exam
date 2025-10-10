from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.models.user import User
from app.models.exam_record import ExamRecord
from app.models.wrong_answer import WrongAnswer
from app.models.question import Question
from app.models.subject import Subject
from app import db
import json
import logging

logger = logging.getLogger(__name__)

class LearningProgressService:
    """学习进度服务"""
    
    @staticmethod
    def get_learning_overview(user_id: int) -> Dict[str, Any]:
        """获取学习概览"""
        try:
            # 获取用户基本信息
            user = User.query.get(user_id)
            if not user:
                raise Exception('用户不存在')
            
            # 获取考试记录统计
            exam_records = ExamRecord.query.filter_by(user_id=user_id, status='submitted').all()
            
            # 获取错题统计
            wrong_answers = WrongAnswer.query.filter_by(user_id=user_id).all()
            
            # 计算基础统计
            total_exams = len(exam_records)
            total_score = sum(record.score for record in exam_records if record.score is not None)
            average_score = total_score / total_exams if total_exams > 0 else 0
            
            # 计算学习天数
            if exam_records:
                first_exam_date = min(record.created_at for record in exam_records)
                learning_days = (datetime.utcnow() - first_exam_date).days + 1
            else:
                learning_days = 0
            
            # 计算最近7天的学习情况
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_exams = [r for r in exam_records if r.created_at >= seven_days_ago]
            recent_study_days = len(set(r.created_at.date() for r in recent_exams))
            
            # 计算学习强度
            study_intensity = recent_study_days / 7 if learning_days >= 7 else recent_study_days / learning_days if learning_days > 0 else 0
            
            # 计算错题复习率
            reviewed_wrong_answers = len([wa for wa in wrong_answers if wa.is_reviewed])
            review_rate = reviewed_wrong_answers / len(wrong_answers) if wrong_answers else 0
            
            return {
                'user_info': {
                    'username': user.username,
                    'real_name': user.real_name,
                    'created_at': user.created_at.isoformat()
                },
                'learning_stats': {
                    'total_exams': total_exams,
                    'average_score': round(average_score, 2),
                    'learning_days': learning_days,
                    'study_intensity': round(study_intensity * 100, 2),
                    'total_wrong_answers': len(wrong_answers),
                    'review_rate': round(review_rate * 100, 2)
                },
                'recent_activity': {
                    'recent_exams': len(recent_exams),
                    'recent_study_days': recent_study_days,
                    'last_exam_date': max(r.created_at for r in exam_records).isoformat() if exam_records else None
                }
            }
            
        except Exception as e:
            logger.error(f'Get learning overview error: {str(e)}')
            raise Exception(f'获取学习概览失败: {str(e)}')
    
    @staticmethod
    def get_learning_progress(user_id: int, subject_id: Optional[int] = None, 
                            period: str = '30d') -> Dict[str, Any]:
        """获取学习进度"""
        try:
            # 计算时间范围
            now = datetime.utcnow()
            if period == '7d':
                start_date = now - timedelta(days=7)
            elif period == '30d':
                start_date = now - timedelta(days=30)
            elif period == '3m':
                start_date = now - timedelta(days=90)
            elif period == '1y':
                start_date = now - timedelta(days=365)
            else:
                start_date = now - timedelta(days=30)
            
            # 构建查询条件
            query = ExamRecord.query.filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted',
                ExamRecord.created_at >= start_date
            )
            
            if subject_id:
                query = query.join(Question).filter(Question.subject_id == subject_id)
            
            exam_records = query.all()
            
            # 按日期分组统计
            daily_stats = {}
            for record in exam_records:
                date_key = record.created_at.date().isoformat()
                if date_key not in daily_stats:
                    daily_stats[date_key] = {
                        'exams_count': 0,
                        'total_score': 0,
                        'total_points': 0,
                        'wrong_answers': 0
                    }
                
                daily_stats[date_key]['exams_count'] += 1
                if record.score is not None:
                    daily_stats[date_key]['total_score'] += record.score
                daily_stats[date_key]['total_points'] += record.total_points or 0
            
            # 获取错题数据
            wrong_query = WrongAnswer.query.filter(
                WrongAnswer.user_id == user_id,
                WrongAnswer.created_at >= start_date
            )
            
            if subject_id:
                wrong_query = wrong_query.join(Question).filter(Question.subject_id == subject_id)
            
            wrong_answers = wrong_query.all()
            
            # 按日期统计错题
            for wrong_answer in wrong_answers:
                date_key = wrong_answer.created_at.date().isoformat()
                if date_key in daily_stats:
                    daily_stats[date_key]['wrong_answers'] += 1
            
            # 生成日期序列
            date_list = []
            current_date = start_date.date()
            while current_date <= now.date():
                date_list.append(current_date.isoformat())
                current_date += timedelta(days=1)
            
            # 填充缺失的日期
            progress_data = []
            for date in date_list:
                if date in daily_stats:
                    stats = daily_stats[date]
                    avg_score = stats['total_score'] / stats['exams_count'] if stats['exams_count'] > 0 else 0
                    progress_data.append({
                        'date': date,
                        'exams_count': stats['exams_count'],
                        'average_score': round(avg_score, 2),
                        'wrong_answers': stats['wrong_answers']
                    })
                else:
                    progress_data.append({
                        'date': date,
                        'exams_count': 0,
                        'average_score': 0,
                        'wrong_answers': 0
                    })
            
            return {
                'period': period,
                'subject_id': subject_id,
                'progress_data': progress_data,
                'summary': {
                    'total_exams': len(exam_records),
                    'total_wrong_answers': len(wrong_answers),
                    'average_score': round(sum(r.score for r in exam_records if r.score is not None) / len(exam_records), 2) if exam_records else 0,
                    'study_days': len([d for d in progress_data if d['exams_count'] > 0])
                }
            }
            
        except Exception as e:
            logger.error(f'Get learning progress error: {str(e)}')
            raise Exception(f'获取学习进度失败: {str(e)}')
    
    @staticmethod
    def get_learning_statistics(user_id: int, subject_id: Optional[int] = None,
                               start_date: Optional[str] = None, 
                               end_date: Optional[str] = None) -> Dict[str, Any]:
        """获取学习统计"""
        try:
            # 构建查询条件
            query = ExamRecord.query.filter_by(user_id=user_id, status='submitted')
            
            if subject_id:
                query = query.join(Question).filter(Question.subject_id == subject_id)
            
            if start_date:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.filter(ExamRecord.created_at >= start_dt)
            
            if end_date:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.filter(ExamRecord.created_at <= end_dt)
            
            exam_records = query.all()
            
            if not exam_records:
                return {
                    'total_exams': 0,
                    'average_score': 0,
                    'score_distribution': {},
                    'subject_performance': {},
                    'difficulty_analysis': {},
                    'improvement_trend': []
                }
            
            # 基础统计
            scores = [r.score for r in exam_records if r.score is not None]
            total_exams = len(exam_records)
            average_score = sum(scores) / len(scores) if scores else 0
            
            # 分数分布
            score_distribution = {
                'excellent': len([s for s in scores if s >= 90]),
                'good': len([s for s in scores if 80 <= s < 90]),
                'medium': len([s for s in scores if 70 <= s < 80]),
                'pass': len([s for s in scores if 60 <= s < 70]),
                'fail': len([s for s in scores if s < 60])
            }
            
            # 科目表现
            subject_performance = {}
            for record in exam_records:
                # 这里需要根据exam_id获取subject_id
                # 简化处理，实际应该通过exam表关联
                subject_key = f'科目_{record.exam_id}'
                if subject_key not in subject_performance:
                    subject_performance[subject_key] = {
                        'exams_count': 0,
                        'total_score': 0,
                        'average_score': 0
                    }
                
                subject_performance[subject_key]['exams_count'] += 1
                if record.score is not None:
                    subject_performance[subject_key]['total_score'] += record.score
            
            # 计算各科目平均分
            for subject_key in subject_performance:
                stats = subject_performance[subject_key]
                stats['average_score'] = round(stats['total_score'] / stats['exams_count'], 2)
            
            # 改进趋势（按月份统计）
            monthly_stats = {}
            for record in exam_records:
                month_key = record.created_at.strftime('%Y-%m')
                if month_key not in monthly_stats:
                    monthly_stats[month_key] = []
                if record.score is not None:
                    monthly_stats[month_key].append(record.score)
            
            improvement_trend = []
            for month, scores in sorted(monthly_stats.items()):
                improvement_trend.append({
                    'month': month,
                    'average_score': round(sum(scores) / len(scores), 2),
                    'exams_count': len(scores)
                })
            
            return {
                'total_exams': total_exams,
                'average_score': round(average_score, 2),
                'score_distribution': score_distribution,
                'subject_performance': subject_performance,
                'difficulty_analysis': {},  # 待实现
                'improvement_trend': improvement_trend
            }
            
        except Exception as e:
            logger.error(f'Get learning statistics error: {str(e)}')
            raise Exception(f'获取学习统计失败: {str(e)}')
    
    @staticmethod
    def get_achievements(user_id: int) -> List[Dict[str, Any]]:
        """获取学习成就"""
        try:
            achievements = []
            
            # 获取用户数据
            exam_records = ExamRecord.query.filter_by(user_id=user_id, status='submitted').all()
            wrong_answers = WrongAnswer.query.filter_by(user_id=user_id).all()
            
            # 考试次数成就
            exam_count = len(exam_records)
            if exam_count >= 1:
                achievements.append({
                    'id': 'first_exam',
                    'title': '初试锋芒',
                    'description': '完成第一次考试',
                    'icon': 'trophy',
                    'unlocked': True,
                    'progress': 100
                })
            
            if exam_count >= 10:
                achievements.append({
                    'id': 'exam_master',
                    'title': '考试达人',
                    'description': '完成10次考试',
                    'icon': 'medal',
                    'unlocked': True,
                    'progress': 100
                })
            elif exam_count >= 5:
                achievements.append({
                    'id': 'exam_master',
                    'title': '考试达人',
                    'description': '完成10次考试',
                    'icon': 'medal',
                    'unlocked': False,
                    'progress': exam_count * 10
                })
            
            # 高分成就
            if exam_records:
                max_score = max(r.score for r in exam_records if r.score is not None)
                if max_score >= 100:
                    achievements.append({
                        'id': 'perfect_score',
                        'title': '完美无缺',
                        'description': '获得满分',
                        'icon': 'star',
                        'unlocked': True,
                        'progress': 100
                    })
                elif max_score >= 90:
                    achievements.append({
                        'id': 'excellent_score',
                        'title': '优秀表现',
                        'description': '获得90分以上',
                        'icon': 'star',
                        'unlocked': True,
                        'progress': 100
                    })
            
            # 复习成就
            reviewed_count = len([wa for wa in wrong_answers if wa.is_reviewed])
            if reviewed_count >= 10:
                achievements.append({
                    'id': 'review_master',
                    'title': '复习达人',
                    'description': '复习10道错题',
                    'icon': 'book',
                    'unlocked': True,
                    'progress': 100
                })
            elif reviewed_count >= 5:
                achievements.append({
                    'id': 'review_master',
                    'title': '复习达人',
                    'description': '复习10道错题',
                    'icon': 'book',
                    'unlocked': False,
                    'progress': reviewed_count * 10
                })
            
            # 连续学习成就
            if exam_records:
                # 计算连续学习天数
                exam_dates = sorted([r.created_at.date() for r in exam_records])
                consecutive_days = LearningProgressService._calculate_consecutive_days(exam_dates)
                
                if consecutive_days >= 7:
                    achievements.append({
                        'id': 'week_warrior',
                        'title': '一周战士',
                        'description': '连续学习7天',
                        'icon': 'fire',
                        'unlocked': True,
                        'progress': 100
                    })
                elif consecutive_days >= 3:
                    achievements.append({
                        'id': 'week_warrior',
                        'title': '一周战士',
                        'description': '连续学习7天',
                        'icon': 'fire',
                        'unlocked': False,
                        'progress': consecutive_days * 14.3
                    })
            
            return achievements
            
        except Exception as e:
            logger.error(f'Get achievements error: {str(e)}')
            raise Exception(f'获取学习成就失败: {str(e)}')
    
    @staticmethod
    def generate_learning_report(user_id: int, period: str = 'month', 
                                subject_id: Optional[int] = None) -> Dict[str, Any]:
        """生成学习报告"""
        try:
            # 计算时间范围
            now = datetime.utcnow()
            if period == 'week':
                start_date = now - timedelta(days=7)
            elif period == 'month':
                start_date = now - timedelta(days=30)
            elif period == 'quarter':
                start_date = now - timedelta(days=90)
            elif period == 'year':
                start_date = now - timedelta(days=365)
            else:
                start_date = now - timedelta(days=30)
            
            # 获取数据
            exam_records = ExamRecord.query.filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted',
                ExamRecord.created_at >= start_date
            ).all()
            
            wrong_answers = WrongAnswer.query.filter(
                WrongAnswer.user_id == user_id,
                WrongAnswer.created_at >= start_date
            ).all()
            
            # 生成报告
            report = {
                'period': period,
                'start_date': start_date.isoformat(),
                'end_date': now.isoformat(),
                'summary': {
                    'total_exams': len(exam_records),
                    'total_score': sum(r.score for r in exam_records if r.score is not None),
                    'average_score': 0,
                    'total_wrong_answers': len(wrong_answers),
                    'reviewed_wrong_answers': len([wa for wa in wrong_answers if wa.is_reviewed])
                },
                'analysis': {
                    'strengths': [],
                    'weaknesses': [],
                    'recommendations': []
                },
                'trends': {
                    'score_trend': 'stable',  # improving, stable, declining
                    'study_frequency': 'regular'  # high, regular, low
                }
            }
            
            # 计算平均分
            if exam_records:
                scores = [r.score for r in exam_records if r.score is not None]
                report['summary']['average_score'] = round(sum(scores) / len(scores), 2)
            
            # 生成分析
            if report['summary']['average_score'] >= 80:
                report['analysis']['strengths'].append('成绩优秀，学习效果良好')
            elif report['summary']['average_score'] >= 60:
                report['analysis']['strengths'].append('成绩合格，基础扎实')
            
            if report['summary']['total_wrong_answers'] > 0:
                review_rate = report['summary']['reviewed_wrong_answers'] / report['summary']['total_wrong_answers']
                if review_rate >= 0.8:
                    report['analysis']['strengths'].append('错题复习积极，学习态度认真')
                else:
                    report['analysis']['weaknesses'].append('错题复习不够充分')
                    report['analysis']['recommendations'].append('建议加强错题复习，提高学习效率')
            
            if report['summary']['total_exams'] < 3:
                report['analysis']['weaknesses'].append('考试次数较少')
                report['analysis']['recommendations'].append('建议增加练习频率，保持学习节奏')
            
            return report
            
        except Exception as e:
            logger.error(f'Generate learning report error: {str(e)}')
            raise Exception(f'生成学习报告失败: {str(e)}')
    
    @staticmethod
    def get_learning_recommendations(user_id: int) -> List[Dict[str, Any]]:
        """获取学习建议"""
        try:
            recommendations = []
            
            # 获取用户数据
            exam_records = ExamRecord.query.filter_by(user_id=user_id, status='submitted').all()
            wrong_answers = WrongAnswer.query.filter_by(user_id=user_id).all()
            
            if not exam_records:
                recommendations.append({
                    'type': 'motivation',
                    'title': '开始你的学习之旅',
                    'description': '完成第一次考试，开启学习记录',
                    'priority': 'high',
                    'action': '参加考试'
                })
                return recommendations
            
            # 分析学习情况并给出建议
            recent_exams = [r for r in exam_records if r.created_at >= datetime.utcnow() - timedelta(days=7)]
            
            if len(recent_exams) == 0:
                recommendations.append({
                    'type': 'frequency',
                    'title': '保持学习节奏',
                    'description': '最近一周没有考试记录，建议保持定期练习',
                    'priority': 'medium',
                    'action': '安排考试'
                })
            
            # 错题复习建议
            unreviewed_wrong_answers = [wa for wa in wrong_answers if not wa.is_reviewed]
            if unreviewed_wrong_answers:
                recommendations.append({
                    'type': 'review',
                    'title': '复习错题',
                    'description': f'还有{len(unreviewed_wrong_answers)}道错题待复习',
                    'priority': 'high',
                    'action': '复习错题'
                })
            
            # 成绩提升建议
            if exam_records:
                recent_scores = [r.score for r in recent_exams if r.score is not None]
                if recent_scores:
                    avg_recent_score = sum(recent_scores) / len(recent_scores)
                    if avg_recent_score < 70:
                        recommendations.append({
                            'type': 'improvement',
                            'title': '提升成绩',
                            'description': '最近成绩偏低，建议加强基础知识学习',
                            'priority': 'high',
                            'action': '加强练习'
                        })
            
            return recommendations
            
        except Exception as e:
            logger.error(f'Get learning recommendations error: {str(e)}')
            raise Exception(f'获取学习建议失败: {str(e)}')
    
    @staticmethod
    def get_learning_goals(user_id: int) -> List[Dict[str, Any]]:
        """获取学习目标"""
        try:
            # 这里应该从数据库获取用户设置的学习目标
            # 目前返回示例数据
            goals = [
                {
                    'id': 1,
                    'title': '提高平均成绩',
                    'description': '将平均成绩提升到85分以上',
                    'target_value': 85,
                    'current_value': 78,
                    'target_date': '2024-03-01',
                    'status': 'active',
                    'progress': 78
                },
                {
                    'id': 2,
                    'title': '完成错题复习',
                    'description': '复习所有错题',
                    'target_value': 20,
                    'current_value': 15,
                    'target_date': '2024-02-15',
                    'status': 'active',
                    'progress': 75
                }
            ]
            
            return goals
            
        except Exception as e:
            logger.error(f'Get learning goals error: {str(e)}')
            raise Exception(f'获取学习目标失败: {str(e)}')
    
    @staticmethod
    def create_learning_goal(user_id: int, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建学习目标"""
        try:
            # 这里应该保存到数据库
            # 目前返回示例数据
            goal = {
                'id': 3,
                'user_id': user_id,
                'title': goal_data['title'],
                'description': goal_data.get('description', ''),
                'target_value': goal_data['target_score'],
                'current_value': 0,
                'target_date': goal_data['target_date'],
                'status': 'active',
                'progress': 0,
                'created_at': datetime.utcnow().isoformat()
            }
            
            return goal
            
        except Exception as e:
            logger.error(f'Create learning goal error: {str(e)}')
            raise Exception(f'创建学习目标失败: {str(e)}')
    
    @staticmethod
    def update_learning_goal(goal_id: int, user_id: int, goal_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新学习目标"""
        try:
            # 这里应该更新数据库
            # 目前返回示例数据
            goal = {
                'id': goal_id,
                'user_id': user_id,
                'title': goal_data.get('title', ''),
                'description': goal_data.get('description', ''),
                'target_value': goal_data.get('target_score', 0),
                'current_value': goal_data.get('current_value', 0),
                'target_date': goal_data.get('target_date', ''),
                'status': goal_data.get('status', 'active'),
                'progress': goal_data.get('progress', 0),
                'updated_at': datetime.utcnow().isoformat()
            }
            
            return goal
            
        except Exception as e:
            logger.error(f'Update learning goal error: {str(e)}')
            raise Exception(f'更新学习目标失败: {str(e)}')
    
    @staticmethod
    def delete_learning_goal(goal_id: int, user_id: int) -> None:
        """删除学习目标"""
        try:
            # 这里应该从数据库删除
            pass
            
        except Exception as e:
            logger.error(f'Delete learning goal error: {str(e)}')
            raise Exception(f'删除学习目标失败: {str(e)}')
    
    @staticmethod
    def _calculate_consecutive_days(dates: List[datetime.date]) -> int:
        """计算连续学习天数"""
        if not dates:
            return 0
        
        consecutive_days = 1
        max_consecutive = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                consecutive_days += 1
                max_consecutive = max(max_consecutive, consecutive_days)
            else:
                consecutive_days = 1
        
        return max_consecutive
