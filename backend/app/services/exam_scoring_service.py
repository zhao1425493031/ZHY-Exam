from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models.exam_record import ExamRecord
from app.models.exam import Exam
from app.models.question import Question
from app.models.wrong_answer import WrongAnswer
from app import db
import json
import logging

logger = logging.getLogger(__name__)

class ExamScoringService:
    """考试评分服务"""
    
    @staticmethod
    def calculate_score(exam_record_id: int, answers: List[str]) -> Dict[str, Any]:
        """计算考试分数"""
        try:
            # 获取考试记录
            exam_record = ExamRecord.query.get(exam_record_id)
            if not exam_record:
                raise Exception('考试记录不存在')
            
            # 获取考试信息
            exam = Exam.query.get(exam_record.exam_id)
            if not exam:
                raise Exception('考试不存在')
            
            # 获取题目信息
            question_ids = exam.question_ids
            questions = Question.query.filter(Question.id.in_(question_ids)).all()
            
            # 创建题目ID到题目的映射
            question_map = {q.id: q for q in questions}
            
            # 计算分数
            total_score = 0
            correct_count = 0
            wrong_answers = []
            
            for i, question_id in enumerate(question_ids):
                question = question_map.get(question_id)
                if not question:
                    continue
                
                user_answer = answers[i] if i < len(answers) else ''
                correct_answer = question.answer
                
                # 判断答案是否正确
                is_correct = ExamScoringService._check_answer(question, user_answer, correct_answer)
                
                if is_correct:
                    total_score += question.points
                    correct_count += 1
                else:
                    # 记录错题
                    wrong_answer = WrongAnswer(
                        user_id=exam_record.user_id,
                        question_id=question_id,
                        exam_record_id=exam_record_id,
                        user_answer=user_answer,
                        correct_answer=correct_answer
                    )
                    wrong_answers.append(wrong_answer)
            
            # 计算得分率
            score_rate = round(total_score / exam.total_points * 100, 2) if exam.total_points > 0 else 0
            
            # 更新考试记录
            exam_record.score = total_score
            exam_record.status = 'submitted'
            exam_record.submit_time = datetime.utcnow()
            exam_record.answers = json.dumps(answers)
            
            # 保存错题记录
            for wrong_answer in wrong_answers:
                db.session.add(wrong_answer)
            
            db.session.commit()
            
            return {
                'total_score': total_score,
                'total_points': exam.total_points,
                'score_rate': score_rate,
                'correct_count': correct_count,
                'total_questions': len(question_ids),
                'wrong_count': len(wrong_answers)
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Calculate score error: {str(e)}')
            raise Exception(f'计算分数失败: {str(e)}')
    
    @staticmethod
    def _check_answer(question: Question, user_answer: str, correct_answer: str) -> bool:
        """检查答案是否正确"""
        try:
            question_type = question.type
            
            if question_type == 'single':
                # 单选题：需要将选项字母转换为内容进行比较
                if question.options and isinstance(question.options, list):
                    # 创建选项映射 A->options[0], B->options[1], ...
                    option_map = {}
                    for j, option in enumerate(question.options):
                        option_map[chr(65 + j)] = option  # A, B, C, D...
                    
                    # 将用户答案的选项字母转换为内容
                    user_answer_content = option_map.get(user_answer, user_answer)
                    return user_answer_content.strip().lower() == correct_answer.strip().lower()
                else:
                    # 如果没有选项，直接比较
                    return user_answer.strip().lower() == correct_answer.strip().lower()
            
            elif question_type == 'multiple':
                # 多选题：需要将选项字母转换为内容进行比较
                if question.options and isinstance(question.options, list):
                    # 创建选项映射 A->options[0], B->options[1], ...
                    option_map = {}
                    for j, option in enumerate(question.options):
                        option_map[chr(65 + j)] = option  # A, B, C, D...
                    
                    # 将用户答案的选项字母转换为内容
                    user_answer_content = '|'.join([option_map.get(char, char) for char in user_answer])
                    return user_answer_content.strip().lower() == correct_answer.strip().lower()
                else:
                    # 如果没有选项，直接比较
                    user_answers = set(user_answer.split(',')) if user_answer else set()
                    correct_answers = set(correct_answer.split(',')) if correct_answer else set()
                    return user_answers == correct_answers
            
            elif question_type == 'judge':
                # 判断题：比较布尔值
                user_bool = user_answer.strip().lower() in ['true', '1', '正确', '是']
                correct_bool = correct_answer.strip().lower() in ['true', '1', '正确', '是']
                return user_bool == correct_bool
            
            elif question_type == 'fill':
                # 填空题：模糊匹配
                return ExamScoringService._fuzzy_match(user_answer, correct_answer)
            
            elif question_type == 'essay':
                # 简答题：关键词匹配（简单实现）
                return ExamScoringService._keyword_match(user_answer, correct_answer)
            
            return False
            
        except Exception as e:
            logger.error(f'Check answer error: {str(e)}')
            return False
    
    @staticmethod
    def _fuzzy_match(user_answer: str, correct_answer: str) -> bool:
        """模糊匹配（填空题）"""
        try:
            if not user_answer or not correct_answer:
                return False
            
            # 去除空格和标点符号
            user_clean = ''.join(c for c in user_answer.lower() if c.isalnum())
            correct_clean = ''.join(c for c in correct_answer.lower() if c.isalnum())
            
            # 直接匹配
            if user_clean == correct_clean:
                return True
            
            # 包含匹配
            if user_clean in correct_clean or correct_clean in user_clean:
                return True
            
            # 相似度匹配（简单实现）
            similarity = ExamScoringService._calculate_similarity(user_clean, correct_clean)
            return similarity >= 0.8
            
        except Exception as e:
            logger.error(f'Fuzzy match error: {str(e)}')
            return False
    
    @staticmethod
    def _keyword_match(user_answer: str, correct_answer: str) -> bool:
        """关键词匹配（简答题）"""
        try:
            if not user_answer or not correct_answer:
                return False
            
            # 提取关键词
            user_keywords = set(user_answer.lower().split())
            correct_keywords = set(correct_answer.lower().split())
            
            # 计算关键词重叠度
            if len(correct_keywords) == 0:
                return False
            
            overlap = len(user_keywords.intersection(correct_keywords))
            overlap_rate = overlap / len(correct_keywords)
            
            # 如果重叠度超过60%，认为答案正确
            return overlap_rate >= 0.6
            
        except Exception as e:
            logger.error(f'Keyword match error: {str(e)}')
            return False
    
    @staticmethod
    def _calculate_similarity(str1: str, str2: str) -> float:
        """计算字符串相似度"""
        try:
            if not str1 or not str2:
                return 0.0
            
            # 简单的编辑距离算法
            m, n = len(str1), len(str2)
            dp = [[0] * (n + 1) for _ in range(m + 1)]
            
            for i in range(m + 1):
                dp[i][0] = i
            for j in range(n + 1):
                dp[0][j] = j
            
            for i in range(1, m + 1):
                for j in range(1, n + 1):
                    if str1[i-1] == str2[j-1]:
                        dp[i][j] = dp[i-1][j-1]
                    else:
                        dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
            
            max_len = max(m, n)
            return 1 - dp[m][n] / max_len if max_len > 0 else 0.0
            
        except Exception as e:
            logger.error(f'Calculate similarity error: {str(e)}')
            return 0.0
    
    @staticmethod
    def get_exam_result(exam_record_id: int) -> Dict[str, Any]:
        """获取考试结果详情"""
        try:
            # 获取考试记录
            exam_record = ExamRecord.query.get(exam_record_id)
            if not exam_record:
                raise Exception('考试记录不存在')
            
            # 获取考试信息
            exam = Exam.query.get(exam_record.exam_id)
            if not exam:
                raise Exception('考试不存在')
            
            # 获取题目信息
            question_ids = exam.question_ids
            questions = Question.query.filter(Question.id.in_(question_ids)).all()
            
            # 创建题目ID到题目的映射
            question_map = {q.id: q for q in questions}
            
            # 获取用户答案
            if isinstance(exam_record.answers, str):
                # 如果是字符串，尝试解析JSON
                try:
                    parsed_answers = json.loads(exam_record.answers)
                    # 如果是字典，直接使用；如果是列表，转换为字典
                    if isinstance(parsed_answers, dict):
                        user_answers = parsed_answers
                    elif isinstance(parsed_answers, list):
                        # 将列表转换为字典，使用索引作为键
                        user_answers = {str(i): answer for i, answer in enumerate(parsed_answers)}
                    else:
                        user_answers = {}
                except (json.JSONDecodeError, TypeError):
                    user_answers = {}
            elif isinstance(exam_record.answers, dict):
                # 如果已经是字典，直接使用
                user_answers = exam_record.answers
            elif isinstance(exam_record.answers, list):
                # 如果是列表，转换为字典
                user_answers = {str(i): answer for i, answer in enumerate(exam_record.answers)}
            else:
                # 其他情况，设为空字典
                user_answers = {}
            
            # 构建结果详情
            result_details = []
            for i, question_id in enumerate(question_ids):
                question = question_map.get(question_id)
                if not question:
                    continue
                
                # 使用字符串索引作为键来获取用户答案
                user_answer = user_answers.get(str(i), '')
                correct_answer = question.answer
                
                # 判断答案是否正确
                is_correct = ExamScoringService._check_answer(question, user_answer, correct_answer)
                
                # 格式化答案显示
                from app.api.exam_scoring import format_answer_for_display
                formatted_user_answer = format_answer_for_display(user_answer, question, is_user_answer=True)
                formatted_correct_answer = format_answer_for_display(correct_answer, question, is_user_answer=False)
                
                result_details.append({
                    'question_id': question_id,
                    'question_title': question.title,
                    'question_type': question.type,
                    'question_points': question.points,
                    'user_answer': formatted_user_answer,
                    'correct_answer': formatted_correct_answer,
                    'is_correct': is_correct,
                    'explanation': question.explanation
                })
            
            # 计算考试时长
            duration = 0
            if exam_record.start_time and exam_record.submit_time:
                duration = (exam_record.submit_time - exam_record.start_time).total_seconds() / 60
                logger.info(f'计算考试时长: start_time={exam_record.start_time}, submit_time={exam_record.submit_time}, duration={duration}分钟')
            else:
                logger.warning(f'考试时间不完整: start_time={exam_record.start_time}, submit_time={exam_record.submit_time}')
            
            # 获取考试合格分数（从数据库中获取，默认为总分的60%）
            passing_score = exam.passing_score if exam.passing_score is not None else int(exam.total_points * 0.6)
            
            return {
                'exam_record_id': exam_record_id,
                'exam_id': exam.id,
                'exam_title': exam.title,
                'total_score': exam_record.score,
                'total_points': exam.total_points,
                'score_rate': round(exam_record.score / exam.total_points * 100, 2) if exam.total_points > 0 else 0,
                'correct_count': sum(1 for detail in result_details if detail['is_correct']),
                'total_questions': len(result_details),
                'start_time': exam_record.start_time.isoformat() if exam_record.start_time else None,
                'submit_time': exam_record.submit_time.isoformat() if exam_record.submit_time else None,
                'duration': duration,
                'passing_score': passing_score,
                'is_passed': (exam_record.score or 0) >= passing_score,
                'result_details': result_details
            }
            
        except Exception as e:
            logger.error(f'Get exam result error: {str(e)}')
            raise Exception(f'获取考试结果失败: {str(e)}')
    
    @staticmethod
    def get_exam_statistics(exam_id: int) -> Dict[str, Any]:
        """获取考试统计信息"""
        try:
            # 获取考试记录
            exam_records = ExamRecord.query.filter_by(exam_id=exam_id, status='submitted').all()
            
            if not exam_records:
                return {
                    'total_participants': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'lowest_score': 0,
                    'pass_rate': 0,
                    'score_distribution': {}
                }
            
            # 计算统计信息
            scores = [record.score for record in exam_records if record.score is not None]
            total_participants = len(scores)
            
            if total_participants == 0:
                return {
                    'total_participants': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'lowest_score': 0,
                    'pass_rate': 0,
                    'score_distribution': {}
                }
            
            average_score = sum(scores) / total_participants
            highest_score = max(scores)
            lowest_score = min(scores)
            
            # 计算及格率（假设60分为及格）
            pass_count = sum(1 for score in scores if score >= 60)
            pass_rate = round(pass_count / total_participants * 100, 2)
            
            # 分数分布
            score_distribution = {}
            for score in scores:
                range_key = f"{int(score//10)*10}-{int(score//10)*10+9}"
                score_distribution[range_key] = score_distribution.get(range_key, 0) + 1
            
            return {
                'total_participants': total_participants,
                'average_score': round(average_score, 2),
                'highest_score': highest_score,
                'lowest_score': lowest_score,
                'pass_rate': pass_rate,
                'score_distribution': score_distribution
            }
            
        except Exception as e:
            logger.error(f'Get exam statistics error: {str(e)}')
            raise Exception(f'获取考试统计失败: {str(e)}')
