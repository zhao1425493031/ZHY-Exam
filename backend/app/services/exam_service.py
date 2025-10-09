# 考试服务
import random
from datetime import datetime, timedelta
from app.models.exam import Exam
from app.models.question import Question
from app.models.subject import Subject
from app.models import db
from app.utils.helpers import build_response, build_error_response, log_operation, get_client_ip

class ExamService:
    """考试服务"""
    
    @staticmethod
    def create_random_exam(subject_id, exam_config, user_id):
        """创建随机考试"""
        try:
            # 验证科目是否存在
            subject = Subject.query.get(subject_id)
            if not subject:
                raise Exception('科目不存在')
            
            # 获取配置参数
            total_questions = exam_config.get('total_questions', 10)
            difficulty_distribution = exam_config.get('difficulty_distribution', {
                'easy': 0.3,
                'medium': 0.5,
                'hard': 0.2
            })
            question_types = exam_config.get('question_types', ['single', 'multiple', 'judge'])
            
            # 构建查询条件
            query = Question.query.filter_by(subject_id=subject_id, status='published')
            
            # 按题型过滤
            if question_types:
                query = query.filter(Question.type.in_(question_types))
            
            # 获取所有符合条件的试题
            all_questions = query.all()
            
            if len(all_questions) < total_questions:
                raise Exception(f'可用试题数量不足，需要{total_questions}题，只有{len(all_questions)}题')
            
            # 按难度分组
            questions_by_difficulty = {
                'easy': [q for q in all_questions if q.difficulty == 'easy'],
                'medium': [q for q in all_questions if q.difficulty == 'medium'],
                'hard': [q for q in all_questions if q.difficulty == 'hard']
            }
            
            # 计算各难度题目数量
            selected_questions = []
            for difficulty, ratio in difficulty_distribution.items():
                if ratio > 0:
                    count = int(total_questions * ratio)
                    available_questions = questions_by_difficulty.get(difficulty, [])
                    
                    if len(available_questions) >= count:
                        selected = random.sample(available_questions, count)
                        selected_questions.extend(selected)
                    else:
                        # 如果该难度的题目不够，使用所有可用题目
                        selected_questions.extend(available_questions)
            
            # 如果选择的题目数量不够，从剩余题目中补充
            if len(selected_questions) < total_questions:
                remaining_questions = [q for q in all_questions if q not in selected_questions]
                needed = total_questions - len(selected_questions)
                if len(remaining_questions) >= needed:
                    additional = random.sample(remaining_questions, needed)
                    selected_questions.extend(additional)
                else:
                    selected_questions.extend(remaining_questions)
            
            # 如果还是不够，随机重复选择
            while len(selected_questions) < total_questions:
                selected_questions.append(random.choice(all_questions))
            
            # 随机打乱题目顺序
            random.shuffle(selected_questions)
            
            # 只取需要的数量
            selected_questions = selected_questions[:total_questions]
            
            # 计算总分
            total_points = sum(q.points for q in selected_questions)
            question_ids = [q.id for q in selected_questions]
            
            return {
                'question_ids': question_ids,
                'total_points': total_points,
                'question_count': len(question_ids)
            }
            
        except Exception as e:
            raise Exception(f'创建随机考试失败: {str(e)}')
    
    @staticmethod
    def create_exam_from_template(template_id, user_id):
        """从模板创建考试"""
        try:
            # TODO: 实现考试模板功能
            # 这里需要先创建考试模板表和相关功能
            raise Exception('考试模板功能暂未实现')
            
        except Exception as e:
            raise Exception(f'从模板创建考试失败: {str(e)}')
    
    @staticmethod
    def validate_exam_config(exam_config):
        """验证考试配置"""
        try:
            # 验证必要参数
            if 'total_questions' not in exam_config:
                raise Exception('缺少题目总数配置')
            
            total_questions = exam_config['total_questions']
            if not isinstance(total_questions, int) or total_questions <= 0:
                raise Exception('题目总数必须是正整数')
            
            if total_questions > 100:
                raise Exception('题目总数不能超过100题')
            
            # 验证难度分布
            difficulty_distribution = exam_config.get('difficulty_distribution', {})
            if difficulty_distribution:
                total_ratio = sum(difficulty_distribution.values())
                if abs(total_ratio - 1.0) > 0.01:
                    raise Exception('难度分布比例之和必须等于1')
                
                for difficulty in difficulty_distribution.keys():
                    if difficulty not in ['easy', 'medium', 'hard']:
                        raise Exception(f'无效的难度等级: {difficulty}')
            
            # 验证题型
            question_types = exam_config.get('question_types', [])
            if question_types:
                valid_types = ['single', 'multiple', 'judge', 'fill', 'essay']
                for qtype in question_types:
                    if qtype not in valid_types:
                        raise Exception(f'无效的题型: {qtype}')
            
            return True
            
        except Exception as e:
            raise Exception(f'考试配置验证失败: {str(e)}')
    
    @staticmethod
    def calculate_exam_duration(question_count, question_types):
        """计算考试时长"""
        # 基础时间配置（分钟）
        time_per_question = {
            'single': 2,
            'multiple': 3,
            'judge': 1,
            'fill': 5,
            'essay': 10
        }
        
        total_time = 0
        for qtype in question_types:
            count = question_types.count(qtype)
            total_time += count * time_per_question.get(qtype, 3)
        
        # 添加缓冲时间
        buffer_time = max(30, total_time * 0.2)
        return int(total_time + buffer_time)
    
    @staticmethod
    def get_exam_statistics(exam_id):
        """获取考试统计信息"""
        try:
            exam = Exam.query.get(exam_id)
            if not exam:
                raise Exception('考试不存在')
            
            # TODO: 实现考试统计功能
            # 需要考试记录表来统计参与人数、平均分等
            
            stats = {
                'exam_id': exam.id,
                'title': exam.title,
                'total_questions': exam.question_count,
                'total_points': exam.total_points,
                'duration': exam.duration,
                'status': exam.status,
                'created_at': exam.created_at.isoformat() if exam.created_at else None
            }
            
            return stats
            
        except Exception as e:
            raise Exception(f'获取考试统计失败: {str(e)}')
    
    @staticmethod
    def check_exam_availability(exam_id, user_id):
        """检查考试可用性"""
        try:
            exam = Exam.query.get(exam_id)
            if not exam:
                return False, '考试不存在'
            
            # 检查考试状态
            if exam.status != 'published':
                return False, '考试未发布'
            
            # 检查考试时间
            now = datetime.utcnow()
            if exam.start_time and now < exam.start_time:
                return False, '考试尚未开始'
            
            if exam.end_time and now > exam.end_time:
                return False, '考试已结束'
            
            # TODO: 检查用户是否已经参加过此考试
            # 需要考试记录表来检查
            
            # TODO: 检查用户是否有权限参加此考试
            # 需要检查科目是否收费，用户是否已购买
            
            return True, '可以参加考试'
            
        except Exception as e:
            return False, f'检查考试可用性失败: {str(e)}'
