from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import func, desc, and_, or_
from app.models.user import User
from app.models.subject import Subject
from app.models.question import Question
from app.models.exam import Exam
from app.models.exam_record import ExamRecord
from app.models.wrong_answer import WrongAnswer
from app import db
import logging

logger = logging.getLogger(__name__)

class StatisticsService:
    """统计分析服务"""
    
    @staticmethod
    def get_admin_dashboard_statistics() -> Dict[str, Any]:
        """获取管理员仪表盘统计数据"""
        try:
            # 基础统计
            total_users = User.query.count()
            active_users = User.query.filter(User.status == 'active').count()
            total_subjects = Subject.query.count()
            active_subjects = Subject.query.filter(Subject.status == 'active').count()
            total_questions = Question.query.count()
            published_questions = Question.query.filter(Question.status == 'published').count()
            total_exams = Exam.query.count()
            published_exams = Exam.query.filter(Exam.status == 'published').count()
            
            # 考试记录统计
            total_exam_records = ExamRecord.query.count()
            completed_exams = ExamRecord.query.filter(ExamRecord.status == 'submitted').count()
            
            # 最近7天统计
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_users = User.query.filter(User.created_at >= seven_days_ago).count()
            recent_exams = ExamRecord.query.filter(ExamRecord.created_at >= seven_days_ago).count()
            
            # 平均分统计
            avg_score_result = db.session.query(func.avg(ExamRecord.score)).filter(
                ExamRecord.status == 'submitted',
                ExamRecord.score.isnot(None)
            ).scalar()
            avg_score = round(float(avg_score_result), 2) if avg_score_result else 0
            
            # 科目统计
            subject_stats = db.session.query(
                Subject.name,
                func.count(ExamRecord.id).label('exam_count'),
                func.avg(ExamRecord.score).label('avg_score')
            ).join(Exam, Subject.id == Exam.subject_id)\
             .join(ExamRecord, Exam.id == ExamRecord.exam_id)\
             .filter(ExamRecord.status == 'submitted')\
             .group_by(Subject.id, Subject.name)\
             .order_by(desc('exam_count'))\
             .limit(5).all()
            
            subject_statistics = []
            for stat in subject_stats:
                subject_statistics.append({
                    'name': stat.name,
                    'exam_count': stat.exam_count,
                    'avg_score': round(float(stat.avg_score), 2) if stat.avg_score else 0
                })
            
            return {
                'overview': {
                    'total_users': total_users,
                    'active_users': active_users,
                    'total_subjects': total_subjects,
                    'active_subjects': active_subjects,
                    'total_questions': total_questions,
                    'published_questions': published_questions,
                    'total_exams': total_exams,
                    'published_exams': published_exams,
                    'total_exam_records': total_exam_records,
                    'completed_exams': completed_exams,
                    'avg_score': avg_score
                },
                'recent_activity': {
                    'recent_users': recent_users,
                    'recent_exams': recent_exams
                },
                'subject_statistics': subject_statistics
            }
            
        except Exception as e:
            logger.error(f'Get admin dashboard statistics error: {str(e)}')
            raise Exception(f'获取管理员仪表盘统计失败: {str(e)}')
    
    @staticmethod
    def get_user_dashboard_statistics(user_id: int) -> Dict[str, Any]:
        """获取用户仪表盘统计数据"""
        try:
            # 用户考试统计
            total_exams = ExamRecord.query.filter_by(user_id=user_id).count()
            completed_exams = ExamRecord.query.filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted'
            ).count()
            
            # 平均分统计
            avg_score_result = db.session.query(func.avg(ExamRecord.score)).filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted',
                ExamRecord.score.isnot(None)
            ).scalar()
            avg_score = round(float(avg_score_result), 2) if avg_score_result else 0
            
            # 最高分统计
            max_score_result = db.session.query(func.max(ExamRecord.score)).filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted'
            ).scalar()
            max_score = round(float(max_score_result), 2) if max_score_result else 0
            
            # 错题统计
            wrong_answers_count = WrongAnswer.query.filter_by(user_id=user_id).count()
            
            # 最近考试记录
            recent_exams = ExamRecord.query.filter_by(user_id=user_id)\
                .order_by(desc(ExamRecord.created_at))\
                .limit(5).all()
            
            recent_exam_list = []
            for exam_record in recent_exams:
                exam = Exam.query.get(exam_record.exam_id)
                subject = Subject.query.get(exam.subject_id) if exam else None
                recent_exam_list.append({
                    'id': exam_record.id,
                    'exam_title': exam.title if exam else '',
                    'subject_name': subject.name if subject else '',
                    'score': exam_record.score,
                    'status': exam_record.status,
                    'created_at': exam_record.created_at.isoformat() if exam_record.created_at else None
                })
            
            # 科目表现统计
            subject_performance = db.session.query(
                Subject.name,
                func.count(ExamRecord.id).label('exam_count'),
                func.avg(ExamRecord.score).label('avg_score'),
                func.max(ExamRecord.score).label('max_score')
            ).join(Exam, Subject.id == Exam.subject_id)\
             .join(ExamRecord, Exam.id == ExamRecord.exam_id)\
             .filter(ExamRecord.user_id == user_id)\
             .filter(ExamRecord.status == 'submitted')\
             .group_by(Subject.id, Subject.name)\
             .all()
            
            subject_performance_list = []
            for perf in subject_performance:
                subject_performance_list.append({
                    'name': perf.name,
                    'exam_count': perf.exam_count,
                    'avg_score': round(float(perf.avg_score), 2) if perf.avg_score else 0,
                    'max_score': round(float(perf.max_score), 2) if perf.max_score else 0
                })
            
            return {
                'overview': {
                    'total_exams': total_exams,
                    'completed_exams': completed_exams,
                    'avg_score': avg_score,
                    'max_score': max_score,
                    'wrong_answers_count': wrong_answers_count
                },
                'recent_exams': recent_exam_list,
                'subject_performance': subject_performance_list
            }
            
        except Exception as e:
            logger.error(f'Get user dashboard statistics error: {str(e)}')
            raise Exception(f'获取用户仪表盘统计失败: {str(e)}')
    
    @staticmethod
    def get_exam_statistics(start_date: Optional[str] = None, end_date: Optional[str] = None,
                           subject_id: Optional[int] = None) -> Dict[str, Any]:
        """获取考试数据统计"""
        try:
            # 构建查询条件
            query = ExamRecord.query.join(Exam, ExamRecord.exam_id == Exam.id)
            
            if start_date:
                query = query.filter(ExamRecord.created_at >= datetime.fromisoformat(start_date))
            
            if end_date:
                query = query.filter(ExamRecord.created_at <= datetime.fromisoformat(end_date))
            
            if subject_id:
                query = query.filter(Exam.subject_id == subject_id)
            
            # 基础统计
            total_exams = query.count()
            completed_exams = query.filter(ExamRecord.status == 'submitted').count()
            
            # 平均分统计
            avg_score_result = query.filter(
                ExamRecord.status == 'submitted',
                ExamRecord.score.isnot(None)
            ).with_entities(func.avg(ExamRecord.score)).scalar()
            avg_score = round(float(avg_score_result), 2) if avg_score_result else 0
            
            # 分数分布统计
            score_ranges = [
                (0, 60, '不及格'),
                (60, 70, '及格'),
                (70, 80, '中等'),
                (80, 90, '良好'),
                (90, 100, '优秀')
            ]
            
            score_distribution = []
            for min_score, max_score, label in score_ranges:
                count = query.filter(
                    ExamRecord.status == 'submitted',
                    ExamRecord.score >= min_score,
                    ExamRecord.score < max_score
                ).count()
                score_distribution.append({
                    'range': f'{min_score}-{max_score}',
                    'label': label,
                    'count': count,
                    'percentage': round((count / completed_exams * 100), 2) if completed_exams > 0 else 0
                })
            
            # 按科目统计
            subject_stats = query.join(Subject, Exam.subject_id == Subject.id)\
                .filter(ExamRecord.status == 'submitted')\
                .with_entities(
                    Subject.name,
                    func.count(ExamRecord.id).label('exam_count'),
                    func.avg(ExamRecord.score).label('avg_score')
                )\
                .group_by(Subject.id, Subject.name)\
                .order_by(desc('exam_count'))\
                .all()
            
            subject_statistics = []
            for stat in subject_stats:
                subject_statistics.append({
                    'name': stat.name,
                    'exam_count': stat.exam_count,
                    'avg_score': round(float(stat.avg_score), 2) if stat.avg_score else 0
                })
            
            return {
                'overview': {
                    'total_exams': total_exams,
                    'completed_exams': completed_exams,
                    'avg_score': avg_score
                },
                'score_distribution': score_distribution,
                'subject_statistics': subject_statistics
            }
            
        except Exception as e:
            logger.error(f'Get exam statistics error: {str(e)}')
            raise Exception(f'获取考试统计失败: {str(e)}')
    
    @staticmethod
    def get_user_behavior_statistics(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """获取用户行为统计"""
        try:
            # 构建查询条件
            query = User.query
            
            if start_date:
                query = query.filter(User.created_at >= datetime.fromisoformat(start_date))
            
            if end_date:
                query = query.filter(User.created_at <= datetime.fromisoformat(end_date))
            
            # 用户注册统计
            total_users = query.count()
            admin_users = query.filter(User.role == 'admin').count()
            regular_users = query.filter(User.role == 'user').count()
            active_users = query.filter(User.status == 'active').count()
            
            # 用户活跃度统计（最近30天有考试记录的用户）
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            active_users_30d = db.session.query(func.count(func.distinct(ExamRecord.user_id)))\
                .filter(ExamRecord.created_at >= thirty_days_ago)\
                .scalar()
            
            # 用户考试次数分布
            exam_count_distribution = db.session.query(
                func.count(ExamRecord.id).label('exam_count'),
                func.count(func.distinct(ExamRecord.user_id)).label('user_count')
            ).join(User, ExamRecord.user_id == User.id)\
             .filter(ExamRecord.status == 'submitted')\
             .group_by(ExamRecord.user_id)\
             .subquery()
            
            # 按考试次数分组统计用户数量
            exam_distribution = db.session.query(
                exam_count_distribution.c.exam_count,
                func.count(exam_count_distribution.c.user_count).label('user_count')
            ).group_by(exam_count_distribution.c.exam_count)\
             .order_by(exam_count_distribution.c.exam_count)\
             .all()
            
            exam_distribution_list = []
            for dist in exam_distribution:
                exam_distribution_list.append({
                    'exam_count': dist.exam_count,
                    'user_count': dist.user_count
                })
            
            return {
                'overview': {
                    'total_users': total_users,
                    'admin_users': admin_users,
                    'regular_users': regular_users,
                    'active_users': active_users,
                    'active_users_30d': active_users_30d
                },
                'exam_distribution': exam_distribution_list
            }
            
        except Exception as e:
            logger.error(f'Get user behavior statistics error: {str(e)}')
            raise Exception(f'获取用户行为统计失败: {str(e)}')
    
    @staticmethod
    def get_question_analysis(subject_id: Optional[int] = None, question_type: Optional[str] = None,
                             difficulty: Optional[str] = None) -> Dict[str, Any]:
        """获取试题分析统计"""
        try:
            # 构建查询条件
            query = Question.query
            
            if subject_id:
                query = query.filter(Question.subject_id == subject_id)
            
            if question_type:
                query = query.filter(Question.type == question_type)
            
            if difficulty:
                query = query.filter(Question.difficulty == difficulty)
            
            # 基础统计
            total_questions = query.count()
            published_questions = query.filter(Question.status == 'published').count()
            
            # 按题型统计
            type_stats = query.filter(Question.status == 'published')\
                .with_entities(
                    Question.type,
                    func.count(Question.id).label('count')
                )\
                .group_by(Question.type)\
                .all()
            
            type_statistics = []
            for stat in type_stats:
                type_statistics.append({
                    'type': stat.type,
                    'count': stat.count
                })
            
            # 按难度统计
            difficulty_stats = query.filter(Question.status == 'published')\
                .with_entities(
                    Question.difficulty,
                    func.count(Question.id).label('count')
                )\
                .group_by(Question.difficulty)\
                .all()
            
            difficulty_statistics = []
            for stat in difficulty_stats:
                difficulty_statistics.append({
                    'difficulty': stat.difficulty,
                    'count': stat.count
                })
            
            # 按科目统计
            subject_stats = query.join(Subject, Question.subject_id == Subject.id)\
                .filter(Question.status == 'published')\
                .with_entities(
                    Subject.name,
                    func.count(Question.id).label('count')
                )\
                .group_by(Subject.id, Subject.name)\
                .order_by(desc('count'))\
                .limit(10)\
                .all()
            
            subject_statistics = []
            for stat in subject_stats:
                subject_statistics.append({
                    'name': stat.name,
                    'count': stat.count
                })
            
            return {
                'overview': {
                    'total_questions': total_questions,
                    'published_questions': published_questions
                },
                'type_statistics': type_statistics,
                'difficulty_statistics': difficulty_statistics,
                'subject_statistics': subject_statistics
            }
            
        except Exception as e:
            logger.error(f'Get question analysis error: {str(e)}')
            raise Exception(f'获取试题分析失败: {str(e)}')
    
    @staticmethod
    def get_score_distribution(exam_id: Optional[int] = None, subject_id: Optional[int] = None,
                              start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """获取成绩分布统计"""
        try:
            # 构建查询条件
            query = ExamRecord.query.filter(ExamRecord.status == 'submitted')
            
            if exam_id:
                query = query.filter(ExamRecord.exam_id == exam_id)
            
            if subject_id:
                query = query.join(Exam, ExamRecord.exam_id == Exam.id)\
                    .filter(Exam.subject_id == subject_id)
            
            if start_date:
                query = query.filter(ExamRecord.created_at >= datetime.fromisoformat(start_date))
            
            if end_date:
                query = query.filter(ExamRecord.created_at <= datetime.fromisoformat(end_date))
            
            # 分数分布统计
            score_ranges = [
                (0, 60, '不及格'),
                (60, 70, '及格'),
                (70, 80, '中等'),
                (80, 90, '良好'),
                (90, 100, '优秀')
            ]
            
            score_distribution = []
            total_count = query.count()
            
            for min_score, max_score, label in score_ranges:
                count = query.filter(
                    ExamRecord.score >= min_score,
                    ExamRecord.score < max_score
                ).count()
                score_distribution.append({
                    'range': f'{min_score}-{max_score}',
                    'label': label,
                    'count': count,
                    'percentage': round((count / total_count * 100), 2) if total_count > 0 else 0
                })
            
            # 统计信息
            avg_score = query.with_entities(func.avg(ExamRecord.score)).scalar()
            max_score = query.with_entities(func.max(ExamRecord.score)).scalar()
            min_score = query.with_entities(func.min(ExamRecord.score)).scalar()
            
            return {
                'score_distribution': score_distribution,
                'statistics': {
                    'total_count': total_count,
                    'avg_score': round(float(avg_score), 2) if avg_score else 0,
                    'max_score': round(float(max_score), 2) if max_score else 0,
                    'min_score': round(float(min_score), 2) if min_score else 0
                }
            }
            
        except Exception as e:
            logger.error(f'Get score distribution error: {str(e)}')
            raise Exception(f'获取成绩分布失败: {str(e)}')
    
    @staticmethod
    def get_learning_progress_statistics(user_id: int, subject_id: Optional[int] = None) -> Dict[str, Any]:
        """获取学习进度统计"""
        try:
            # 构建查询条件
            query = ExamRecord.query.filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted'
            )
            
            if subject_id:
                query = query.join(Exam, ExamRecord.exam_id == Exam.id)\
                    .filter(Exam.subject_id == subject_id)
            
            # 学习进度统计
            total_exams = query.count()
            avg_score = query.with_entities(func.avg(ExamRecord.score)).scalar()
            max_score = query.with_entities(func.max(ExamRecord.score)).scalar()
            
            # 最近7天学习情况
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_exams = query.filter(ExamRecord.created_at >= seven_days_ago).count()
            
            # 按科目统计学习进度
            subject_progress = query.join(Exam, ExamRecord.exam_id == Exam.id)\
                .join(Subject, Exam.subject_id == Subject.id)\
                .with_entities(
                    Subject.name,
                    func.count(ExamRecord.id).label('exam_count'),
                    func.avg(ExamRecord.score).label('avg_score'),
                    func.max(ExamRecord.score).label('max_score')
                )\
                .group_by(Subject.id, Subject.name)\
                .all()
            
            subject_progress_list = []
            for progress in subject_progress:
                subject_progress_list.append({
                    'name': progress.name,
                    'exam_count': progress.exam_count,
                    'avg_score': round(float(progress.avg_score), 2) if progress.avg_score else 0,
                    'max_score': round(float(progress.max_score), 2) if progress.max_score else 0
                })
            
            return {
                'overview': {
                    'total_exams': total_exams,
                    'avg_score': round(float(avg_score), 2) if avg_score else 0,
                    'max_score': round(float(max_score), 2) if max_score else 0,
                    'recent_exams': recent_exams
                },
                'subject_progress': subject_progress_list
            }
            
        except Exception as e:
            logger.error(f'Get learning progress statistics error: {str(e)}')
            raise Exception(f'获取学习进度统计失败: {str(e)}')
    
    @staticmethod
    def get_performance_trends(user_id: int, subject_id: Optional[int] = None, days: int = 30) -> Dict[str, Any]:
        """获取成绩趋势统计"""
        try:
            # 计算开始日期
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # 构建查询条件
            query = ExamRecord.query.filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted',
                ExamRecord.created_at >= start_date
            )
            
            if subject_id:
                query = query.join(Exam, ExamRecord.exam_id == Exam.id)\
                    .filter(Exam.subject_id == subject_id)
            
            # 按日期分组统计
            trends = query.with_entities(
                func.date(ExamRecord.created_at).label('date'),
                func.count(ExamRecord.id).label('exam_count'),
                func.avg(ExamRecord.score).label('avg_score')
            )\
            .group_by(func.date(ExamRecord.created_at))\
            .order_by('date')\
            .all()
            
            trend_data = []
            for trend in trends:
                trend_data.append({
                    'date': trend.date.isoformat(),
                    'exam_count': trend.exam_count,
                    'avg_score': round(float(trend.avg_score), 2) if trend.avg_score else 0
                })
            
            return {
                'trends': trend_data,
                'period': f'{days}天'
            }
            
        except Exception as e:
            logger.error(f'Get performance trends error: {str(e)}')
            raise Exception(f'获取成绩趋势失败: {str(e)}')
    
    @staticmethod
    def get_subject_performance(user_id: int) -> Dict[str, Any]:
        """获取科目表现统计"""
        try:
            # 按科目统计表现
            performance = db.session.query(
                Subject.name,
                func.count(ExamRecord.id).label('exam_count'),
                func.avg(ExamRecord.score).label('avg_score'),
                func.max(ExamRecord.score).label('max_score'),
                func.min(ExamRecord.score).label('min_score')
            ).join(Exam, Subject.id == Exam.subject_id)\
             .join(ExamRecord, Exam.id == ExamRecord.exam_id)\
             .filter(ExamRecord.user_id == user_id)\
             .filter(ExamRecord.status == 'submitted')\
             .group_by(Subject.id, Subject.name)\
             .order_by(desc('avg_score'))\
             .all()
            
            performance_list = []
            for perf in performance:
                performance_list.append({
                    'name': perf.name,
                    'exam_count': perf.exam_count,
                    'avg_score': round(float(perf.avg_score), 2) if perf.avg_score else 0,
                    'max_score': round(float(perf.max_score), 2) if perf.max_score else 0,
                    'min_score': round(float(perf.min_score), 2) if perf.min_score else 0
                })
            
            return {
                'subject_performance': performance_list
            }
            
        except Exception as e:
            logger.error(f'Get subject performance error: {str(e)}')
            raise Exception(f'获取科目表现失败: {str(e)}')
    
    @staticmethod
    def get_weak_areas(user_id: int, subject_id: Optional[int] = None) -> Dict[str, Any]:
        """获取薄弱环节分析"""
        try:
            # 构建查询条件
            query = WrongAnswer.query.filter(WrongAnswer.user_id == user_id)
            
            if subject_id:
                query = query.join(Question, WrongAnswer.question_id == Question.id)\
                    .filter(Question.subject_id == subject_id)
            
            # 按科目统计错题
            weak_areas = query.join(Question, WrongAnswer.question_id == Question.id)\
                .join(Subject, Question.subject_id == Subject.id)\
                .with_entities(
                    Subject.name,
                    func.count(WrongAnswer.id).label('wrong_count')
                )\
                .group_by(Subject.id, Subject.name)\
                .order_by(desc('wrong_count'))\
                .all()
            
            weak_areas_list = []
            for area in weak_areas:
                weak_areas_list.append({
                    'name': area.name,
                    'wrong_count': area.wrong_count
                })
            
            return {
                'weak_areas': weak_areas_list
            }
            
        except Exception as e:
            logger.error(f'Get weak areas error: {str(e)}')
            raise Exception(f'获取薄弱环节失败: {str(e)}')
    
    @staticmethod
    def get_performance_comparison(user_id: int, subject_id: Optional[int] = None) -> Dict[str, Any]:
        """获取成绩对比统计"""
        try:
            # 获取用户成绩
            user_query = ExamRecord.query.filter(
                ExamRecord.user_id == user_id,
                ExamRecord.status == 'submitted'
            )
            
            if subject_id:
                user_query = user_query.join(Exam, ExamRecord.exam_id == Exam.id)\
                    .filter(Exam.subject_id == subject_id)
            
            user_avg_score = user_query.with_entities(func.avg(ExamRecord.score)).scalar()
            
            # 获取全体平均成绩
            all_query = ExamRecord.query.filter(ExamRecord.status == 'submitted')
            
            if subject_id:
                all_query = all_query.join(Exam, ExamRecord.exam_id == Exam.id)\
                    .filter(Exam.subject_id == subject_id)
            
            all_avg_score = all_query.with_entities(func.avg(ExamRecord.score)).scalar()
            
            # 计算排名
            user_score = user_avg_score if user_avg_score else 0
            all_score = all_avg_score if all_avg_score else 0
            
            # 计算超过的用户百分比
            better_count = all_query.filter(ExamRecord.score < user_score).count()
            total_count = all_query.count()
            percentile = round((better_count / total_count * 100), 2) if total_count > 0 else 0
            
            return {
                'user_avg_score': round(float(user_score), 2),
                'all_avg_score': round(float(all_score), 2),
                'percentile': percentile,
                'comparison': 'above' if user_score > all_score else 'below' if user_score < all_score else 'equal'
            }
            
        except Exception as e:
            logger.error(f'Get performance comparison error: {str(e)}')
            raise Exception(f'获取成绩对比失败: {str(e)}')
    
    @staticmethod
    def get_all_statistics(start_date: Optional[str] = None, end_date: Optional[str] = None,
                          export_type: str = 'all') -> Dict[str, Any]:
        """获取所有统计数据（用于导出）"""
        try:
            statistics = {}
            
            if export_type in ['all', 'exam']:
                statistics['exam_statistics'] = StatisticsService.get_exam_statistics(
                    start_date=start_date,
                    end_date=end_date
                )
            
            if export_type in ['all', 'user']:
                statistics['user_behavior'] = StatisticsService.get_user_behavior_statistics(
                    start_date=start_date,
                    end_date=end_date
                )
            
            if export_type in ['all', 'question']:
                statistics['question_analysis'] = StatisticsService.get_question_analysis()
            
            if export_type in ['all', 'score']:
                statistics['score_distribution'] = StatisticsService.get_score_distribution(
                    start_date=start_date,
                    end_date=end_date
                )
            
            return statistics
            
        except Exception as e:
            logger.error(f'Get all statistics error: {str(e)}')
            raise Exception(f'获取统计数据失败: {str(e)}')
