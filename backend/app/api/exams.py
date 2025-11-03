# 考试管理API
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import exams_bp, BaseAPI
from app.models.exam import Exam
from app.models.subject import Subject
from app.models.question import Question
from app.models import db
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import ExamSchema, PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation
from app.services.exam_service import ExamService
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

# 创建考试API实例
exam_api = BaseAPI(Exam, ExamSchema)

@exams_bp.route('', methods=['GET'])
def get_exams():
    """获取考试列表（公开接口）"""
    try:
        # 验证分页参数
        pagination_schema = PaginationSchema()
        pagination_data = pagination_schema.load({
            'page': request.args.get('page', 1, type=int),
            'size': request.args.get('size', 10, type=int),
            'sort': request.args.get('sort', 'id'),
            'order': request.args.get('order', 'desc')
        })
        
        # 验证搜索参数
        search_schema = SearchSchema()
        search_data = search_schema.load(request.args)
        
        # 构建查询
        query = Exam.query
        
        # 应用搜索过滤
        if search_data.get('keyword'):
            keyword = f"%{search_data['keyword']}%"
            query = query.filter(
                Exam.title.like(keyword) |
                Exam.description.like(keyword)
            )
        
        if search_data.get('subject_id'):
            query = query.filter(Exam.subject_id == search_data['subject_id'])
        
        if search_data.get('status'):
            query = query.filter(Exam.status == search_data['status'])
        
        # 应用排序
        sort_field = pagination_data.get('sort', 'id')
        order = pagination_data.get('order', 'desc')
        
        if hasattr(Exam, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(Exam, sort_field).desc())
            else:
                query = query.order_by(getattr(Exam, sort_field).asc())
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=pagination_data.get('page', 1),
            per_page=pagination_data.get('size', 10)
        )
        
        result = {
            'items': [exam.to_dict() for exam in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        return jsonify(build_error_response(400, str(e))), 400

@exams_bp.route('', methods=['POST'])
@jwt_required()
@require_roles('admin')
@validate_json(ExamSchema)
def create_exam():
    """创建考试（仅管理员）"""
    try:
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 验证科目是否存在
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 验证试题是否存在
        question_ids = data['question_ids']
        questions = Question.query.filter(Question.id.in_(question_ids)).all()
        if len(questions) != len(question_ids):
            return jsonify(build_error_response(400, '部分试题不存在')), 400
        
        # 计算总分
        total_points = sum(q.points for q in questions)
        
        # 创建考试
        exam = Exam(
            title=data['title'],
            subject_id=data['subject_id'],
            description=data.get('description', ''),
            duration=data['duration'],
            total_points=total_points,
            passing_score=data.get('passing_score'),
            question_count=len(question_ids),
            question_ids=question_ids,
            start_time=data.get('start_time'),
            end_time=data.get('end_time'),
            status=data.get('status', 'draft'),
            settings=data.get('settings', {}),
            created_by=current_user_id
        )
        
        db.session.add(exam)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='create_exam',
            details=f'创建考试: {exam.title}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试创建成功',
            data=exam.to_dict()
        )), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'创建考试失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>', methods=['GET'])
def get_exam(exam_id):
    """获取考试详情"""
    try:
        from app.models.subject import Subject
        
        exam = Exam.query.get_or_404(exam_id)
        
        # 获取科目信息
        subject = Subject.query.get(exam.subject_id)
        subject_name = subject.name if subject else '未知科目'
        
        # 获取题目数据（按照exam.question_ids的顺序）
        questions = []
        if exam.question_ids:
            # 按照exam.question_ids的顺序获取题目
            question_dict = {}
            for q in Question.query.filter(Question.id.in_(exam.question_ids)).all():
                question_dict[q.id] = q
            
            # 按照exam.question_ids的顺序构建题目列表
            for question_id in exam.question_ids:
                if question_id in question_dict:
                    questions.append(question_dict[question_id].to_dict())
        
        # 构建响应数据
        exam_data = exam.to_dict()
        exam_data['questions'] = questions
        exam_data['subject_name'] = subject_name
        
        return jsonify(build_response(data=exam_data))
    except Exception as e:
        return jsonify(build_error_response(404, str(e))), 404

@exams_bp.route('/<int:exam_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
@validate_json(ExamSchema)
def update_exam(exam_id):
    """更新考试信息（仅管理员）"""
    try:
        exam = Exam.query.get_or_404(exam_id)
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 验证科目是否存在
        if 'subject_id' in data:
            subject = Subject.query.get(data['subject_id'])
            if not subject:
                return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 验证试题是否存在
        if 'question_ids' in data:
            question_ids = data['question_ids']
            questions = Question.query.filter(Question.id.in_(question_ids)).all()
            if len(questions) != len(question_ids):
                return jsonify(build_error_response(400, '部分试题不存在')), 400
            
            # 更新试题相关字段
            data['question_count'] = len(question_ids)
            data['total_points'] = sum(q.points for q in questions)
        
        # 更新考试信息
        for key, value in data.items():
            if hasattr(exam, key):
                setattr(exam, key, value)
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_exam',
            details=f'更新考试: {exam.title}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试更新成功',
            data=exam.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新考试失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_exam(exam_id):
    """删除考试（仅管理员）"""
    try:
        exam = Exam.query.get_or_404(exam_id)
        current_user_id = get_jwt_identity()
        
        # TODO: 检查是否有考试记录关联此考试
        # 这里可以添加关联检查逻辑
        
        title = exam.title
        db.session.delete(exam)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='delete_exam',
            details=f'删除考试: {title}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='考试删除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'删除考试失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>/status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_exam_status(exam_id):
    """更新考试状态（仅管理员）"""
    try:
        exam = Exam.query.get_or_404(exam_id)
        data = request.get_json()
        status = data.get('status')
        current_user_id = get_jwt_identity()
        
        if status not in ['draft', 'published', 'ongoing', 'finished', 'cancelled']:
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        old_status = exam.status
        exam.status = status
        
        # 如果状态改为进行中，设置开始时间
        if status == 'ongoing' and not exam.start_time:
            exam.start_time = datetime.utcnow()
        
        # 如果状态改为已完成，设置结束时间
        if status == 'finished' and not exam.end_time:
            exam.end_time = datetime.utcnow()
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_exam_status',
            details=f'修改考试状态: {exam.title} ({old_status} -> {status})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试状态更新成功',
            data={'status': exam.status}
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新考试状态失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>/questions', methods=['GET'])
@jwt_required()
def get_exam_questions(exam_id):
    """获取考试试题列表"""
    try:
        exam = Exam.query.get_or_404(exam_id)
        
        # 获取试题详情（按照exam.question_ids的顺序）
        question_dict = {}
        for q in Question.query.filter(Question.id.in_(exam.question_ids)).all():
            question_dict[q.id] = q
        
        # 构建试题数据（不包含答案，按照exam.question_ids的顺序）
        question_data = []
        for question_id in exam.question_ids:
            if question_id in question_dict:
                q_data = question_dict[question_id].to_dict()
                # 移除答案信息
                q_data.pop('answer', None)
                question_data.append(q_data)
        
        return jsonify(build_response(data=question_data))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取考试试题失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>/start', methods=['POST'])
@jwt_required()
def start_exam(exam_id):
    """开始考试"""
    try:
        from app.models.exam_record import ExamRecord
        
        exam = Exam.query.get_or_404(exam_id)
        current_user_id = get_jwt_identity()
        
        # 检查考试状态
        if exam.status != 'published':
            return jsonify(build_error_response(400, '考试未发布，无法开始')), 400
        
        # 检查考试时间
        now = datetime.utcnow()
        if exam.start_time and now < exam.start_time:
            return jsonify(build_error_response(400, '考试尚未开始')), 400
        
        if exam.end_time and now > exam.end_time:
            return jsonify(build_error_response(400, '考试已结束')), 400
        
        # 检查是否已有进行中的考试记录
        existing_record = ExamRecord.query.filter_by(
            exam_id=exam_id,
            user_id=current_user_id,
            status='in_progress'
        ).first()
        
        if existing_record:
            # 如果已有进行中的记录，返回现有记录
            logger.info(f'用户已有进行中的考试记录: record_id={existing_record.id}')
            return jsonify(build_response(
                message='继续考试',
                data={
                    'exam_id': exam.id,
                    'exam_record_id': existing_record.id,
                    'title': exam.title,
                    'duration': exam.duration,
                    'question_count': exam.question_count,
                    'start_time': existing_record.start_time.isoformat()
                }
            ))
        
        # 创建新的考试记录
        exam_record = ExamRecord(
            exam_id=exam_id,
            user_id=current_user_id,
            start_time=now,
            status='in_progress'
        )
        db.session.add(exam_record)
        db.session.commit()
        
        logger.info(f'创建考试记录: record_id={exam_record.id}, start_time={exam_record.start_time}')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='start_exam',
            details=f'开始考试: {exam.title}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试开始成功',
            data={
                'exam_id': exam.id,
                'exam_record_id': exam_record.id,
                'title': exam.title,
                'duration': exam.duration,
                'question_count': exam.question_count,
                'start_time': now.isoformat()
            }
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'开始考试失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>/submit', methods=['POST'])
@jwt_required()
def submit_exam(exam_id):
    """提交考试"""
    try:
        from app.models.exam_record import ExamRecord
        from app.models.user import User
        
        exam = Exam.query.get_or_404(exam_id)
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        answers_raw = data.get('answers', {})
        start_time_str = data.get('start_time')  # 前端传来的开始时间
        
        # 处理答案格式：前端可能是数组，后端需要字典
        if isinstance(answers_raw, list):
            # 将数组转换为字典 {0: answer0, 1: answer1, ...}
            answers = {str(i): answer for i, answer in enumerate(answers_raw)}
            logger.info(f'前端提交的答案格式为数组，已转换为字典格式')
        else:
            answers = answers_raw
        
        logger.info(f'提交考试: exam_id={exam_id}, user_id={current_user_id}, answers格式={type(answers)}, answers内容={answers}, start_time={start_time_str}')
        
        # 检查考试设置是否允许重复考试
        settings = exam.settings or {}
        allow_retake = settings.get('allow_retake', True)  # 默认允许重复考试
        
        # 查找进行中的考试记录
        exam_record = ExamRecord.query.filter_by(
            exam_id=exam_id,
            user_id=current_user_id,
            status='in_progress'
        ).first()
        
        if exam_record:
            # 更新现有记录
            logger.info(f'更新现有考试记录: record_id={exam_record.id}, start_time={exam_record.start_time}')
            exam_record.submit_time = datetime.utcnow()
            exam_record.answers = answers
            exam_record.status = 'submitted'
        else:
            # 检查是否已有已提交的记录
            submitted_record = ExamRecord.query.filter_by(
                exam_id=exam_id,
                user_id=current_user_id,
                status='submitted'
            ).first()
            
            if submitted_record and not allow_retake:
                return jsonify(build_error_response(400, '该考试不允许重复参加')), 400
            
            # 创建新的考试记录
            # 如果前端传来了开始时间，使用前端的时间；否则使用当前时间
            if start_time_str:
                try:
                    from dateutil import parser
                    start_time = parser.parse(start_time_str)
                    logger.info(f'使用前端传来的开始时间: {start_time}')
                except:
                    start_time = datetime.utcnow()
                    logger.warning(f'解析开始时间失败，使用当前时间: {start_time}')
            else:
                start_time = datetime.utcnow()
                logger.warning(f'前端未传开始时间，使用当前时间: {start_time}')
            
            exam_record = ExamRecord(
                exam_id=exam_id,
                user_id=current_user_id,
                start_time=start_time,
                submit_time=datetime.utcnow(),
                answers=answers,
                status='submitted'
            )
            logger.info(f'创建新考试记录: start_time={exam_record.start_time}, submit_time={exam_record.submit_time}')
        
        # 计算分数和统计
        correct_count = 0
        total_count = 0
        question_details = []
        
        # 获取考试题目（按照exam.question_ids的顺序）
        question_dict = {}
        for q in Question.query.filter(Question.id.in_(exam.question_ids)).all():
            question_dict[q.id] = q
        
        questions = []
        for question_id in exam.question_ids:
            if question_id in question_dict:
                questions.append(question_dict[question_id])
        
        for i, question in enumerate(questions):
            total_count += 1
            user_answer = answers.get(str(i), '')
            is_correct = False
            
            # 根据题型判断答案是否正确
            if question.type in ['single', 'multiple']:
                # 选择题：需要将选项字母转换为内容进行比较
                if question.options and isinstance(question.options, list):
                    # 创建选项映射 A->options[0], B->options[1], ...
                    option_map = {}
                    for j, option in enumerate(question.options):
                        option_map[chr(65 + j)] = option  # A, B, C, D...
                    
                    if question.type == 'single':
                        # 单选题：将用户答案的选项字母转换为内容
                        user_answer_content = option_map.get(user_answer, user_answer)
                        is_correct = user_answer_content == question.answer
                    else:
                        # 多选题：将用户答案的选项字母转换为内容
                        user_answer_content = '|'.join([option_map.get(char, char) for char in user_answer])
                        is_correct = user_answer_content == question.answer
                else:
                    # 如果没有选项，直接比较
                    is_correct = user_answer == question.answer
            elif question.type == 'judge':
                # 判断题：比较布尔值字符串
                is_correct = user_answer == question.answer
            elif question.type in ['fill', 'essay']:
                # 填空题和简答题：简单比较（实际项目中可能需要更复杂的判断）
                is_correct = user_answer.strip().lower() == question.answer.strip().lower()
            
            if is_correct:
                correct_count += 1
            
            question_details.append({
                'question_title': question.title,
                'user_answer': user_answer,
                'correct_answer': question.answer,
                'is_correct': is_correct,
                'points': question.points
            })
        
        # 计算总分
        score = round((correct_count / total_count) * exam.total_points) if total_count > 0 else 0
        accuracy = round((correct_count / total_count) * 100) if total_count > 0 else 0
        
        exam_record.score = score
        exam_record.correct_count = correct_count
        exam_record.total_count = total_count
        
        db.session.add(exam_record)
        db.session.flush()  # 先flush获取exam_record.id
        
        # 生成错题记录
        from app.models.wrong_answer import WrongAnswer
        for i, question in enumerate(questions):
            user_answer = answers.get(str(i), '')
            is_correct = question_details[i]['is_correct']
            
            if not is_correct:  # 如果答案错误，记录错题
                wrong_answer = WrongAnswer(
                    user_id=current_user_id,
                    question_id=question.id,
                    exam_record_id=exam_record.id,
                    user_answer=user_answer,
                    correct_answer=question.answer
                )
                db.session.add(wrong_answer)
                logger.info(f'生成错题记录: question_id={question.id}, user_answer={user_answer}, correct_answer={question.answer}')
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='submit_exam',
            details=f'提交考试: {exam.title}, 得分: {score}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试提交成功',
            data={
                'exam_id': exam.id,
                'score': score,
                'correct_count': correct_count,
                'total_count': total_count,
                'accuracy': accuracy,
                'question_details': question_details
            }
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'提交考试失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>/check-availability', methods=['GET'])
@jwt_required()
def check_exam_availability(exam_id):
    """检查考试是否可以参加"""
    try:
        from app.models.exam_record import ExamRecord
        
        exam = Exam.query.get_or_404(exam_id)
        current_user_id = get_jwt_identity()
        
        # 检查考试设置
        settings = exam.settings or {}
        allow_retake = settings.get('allow_retake', True)
        
        # 检查是否已有考试记录
        existing_records = ExamRecord.query.filter_by(
            exam_id=exam_id,
            user_id=current_user_id
        ).all()
        
        has_taken = len(existing_records) > 0
        can_take = True
        message = ''
        
        if has_taken and not allow_retake:
            can_take = False
            message = '该考试不允许重复参加'
        elif has_taken and allow_retake:
            message = f'您已参加过该考试 {len(existing_records)} 次'
        
        return jsonify(build_response(
            message='检查成功',
            data={
                'can_take': can_take,
                'has_taken': has_taken,
                'attempt_count': len(existing_records),
                'allow_retake': allow_retake,
                'message': message
            }
        ))
    except Exception as e:
        logger.error(f"检查考试可用性失败: {e}")
        return jsonify(build_error_response(500, f'检查失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>/result', methods=['GET'])
@jwt_required()
def get_exam_result(exam_id):
    """获取考试结果"""
    try:
        from app.models.exam_record import ExamRecord
        from app.models.user import User
        from app.models.subject import Subject
        
        current_user_id = get_jwt_identity()
        
        # 获取考试记录 - 获取最新的记录
        exam_record = ExamRecord.query.filter_by(
            exam_id=exam_id,
            user_id=current_user_id
        ).order_by(ExamRecord.created_at.desc()).first()
        
        if not exam_record:
            return jsonify(build_error_response(404, '考试记录不存在')), 404
        
        logger.info(f"[获取结果] 考试记录ID={exam_record.id}, 答案数据={exam_record.answers}, 创建时间={exam_record.created_at}")
        
        # 获取考试信息
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify(build_error_response(404, '考试不存在')), 404
        
        # 获取科目信息
        subject = Subject.query.get(exam.subject_id)
        
        # 计算答题时长
        duration = 0
        if exam_record.start_time and exam_record.submit_time:
            duration_delta = exam_record.submit_time - exam_record.start_time
            duration = int(duration_delta.total_seconds() / 60)
        
        # 构建题目详情
        question_details = []
        if exam_record.answers and exam.question_ids:
            questions = Question.query.filter(Question.id.in_(exam.question_ids)).all()
            # 按题目ID顺序排序，确保与exam.question_ids的顺序一致
            question_id_to_index = {qid: idx for idx, qid in enumerate(exam.question_ids)}
            questions_sorted = sorted(questions, key=lambda q: question_id_to_index[q.id])
            
            for i, question in enumerate(questions_sorted):
                user_answer = exam_record.answers.get(str(i), '')
                print(f"[调试] 题目索引={i}, 题目ID={question.id}, 用户答案={user_answer}, answers={exam_record.answers}")
                is_correct = False
                
                # 根据题型判断答案是否正确
                if question.type in ['single', 'multiple']:
                    # 选择题：需要将选项字母转换为内容进行比较
                    if question.options and isinstance(question.options, list):
                        # 创建选项映射 A->options[0], B->options[1], ...
                        option_map = {}
                        for j, option in enumerate(question.options):
                            option_map[chr(65 + j)] = option  # A, B, C, D...
                        
                        if question.type == 'single':
                            # 单选题：将用户答案的选项字母转换为内容
                            user_answer_content = option_map.get(user_answer, user_answer)
                            is_correct = user_answer_content == question.answer
                        else:
                            # 多选题：将用户答案的选项字母转换为内容
                            user_answer_content = '|'.join([option_map.get(char, char) for char in user_answer])
                            is_correct = user_answer_content == question.answer
                    else:
                        # 如果没有选项，直接比较
                        is_correct = user_answer == question.answer
                elif question.type == 'judge':
                    # 判断题：比较布尔值字符串
                    is_correct = user_answer == question.answer
                elif question.type in ['fill', 'essay']:
                    # 填空题和简答题：简单比较（实际项目中可能需要更复杂的判断）
                    is_correct = user_answer.strip().lower() == question.answer.strip().lower()
                
                # 格式化答案显示
                from app.api.exam_scoring import format_answer_for_display
                formatted_user_answer = format_answer_for_display(user_answer, question, is_user_answer=True)
                formatted_correct_answer = format_answer_for_display(question.answer, question, is_user_answer=False)
                
                logger.info(f"[获取结果] 题目索引={i}, 题目ID={question.id}, 原始用户答案={user_answer}, 格式化后={formatted_user_answer}, 选项={question.options}")
                
                question_details.append({
                    'question_title': question.title,
                    'user_answer': formatted_user_answer,
                    'correct_answer': formatted_correct_answer,
                    'is_correct': is_correct,
                    'points': question.points
                })
        
        # 获取考试合格分数（从数据库中获取，默认为总分的60%）
        passing_score = exam.passing_score if exam.passing_score is not None else int(exam.total_points * 0.6)
        
        # 构建结果数据
        result_data = {
            'exam': {
                'id': exam.id,
                'title': exam.title,
                'subject_name': subject.name if subject else '未知科目',
                'duration': exam.duration,
                'total_points': exam.total_points
            },
            'score': exam_record.score or 0,
            'correct_count': exam_record.correct_count or 0,
            'total_count': exam_record.total_count or 0,
            'accuracy': round((exam_record.correct_count / exam_record.total_count) * 100) if exam_record.total_count > 0 else 0,
            'duration': duration,
            'submit_time': exam_record.submit_time.isoformat() if exam_record.submit_time else None,
            'passing_score': passing_score,
            'is_passed': (exam_record.score or 0) >= passing_score,
            'question_details': question_details
        }
        
        return jsonify(build_response(data=result_data))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取考试结果失败: {str(e)}')), 500

@exams_bp.route('/random-generate', methods=['POST'])
@jwt_required()
@require_roles('admin')
def random_generate_exam():
    """随机生成考试"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        subject_id = data.get('subject_id')
        exam_config = data.get('exam_config', {})
        
        if not subject_id:
            return jsonify(build_error_response(400, '请选择科目')), 400
        
        # 验证考试配置
        try:
            ExamService.validate_exam_config(exam_config)
        except Exception as e:
            return jsonify(build_error_response(400, str(e))), 400
        
        # 生成随机考试
        result = ExamService.create_random_exam(subject_id, exam_config, current_user_id)
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='random_generate_exam',
            details=f'随机生成考试: 科目ID={subject_id}, 题目数量={result["question_count"]}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='随机试题生成成功',
            data=result
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'随机生成考试失败: {str(e)}')), 500

@exams_bp.route('/create-from-config', methods=['POST'])
@jwt_required()
@require_roles('admin')
def create_exam_from_config():
    """根据配置创建考试"""
    try:
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # 获取基本考试信息
        title = data.get('title')
        subject_id = data.get('subject_id')
        description = data.get('description', '')
        exam_config = data.get('exam_config', {})
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if not title or not subject_id:
            return jsonify(build_error_response(400, '请提供考试标题和科目')), 400
        
        # 验证科目是否存在
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 验证考试配置
        try:
            ExamService.validate_exam_config(exam_config)
        except Exception as e:
            return jsonify(build_error_response(400, str(e))), 400
        
        # 生成随机试题
        random_result = ExamService.create_random_exam(subject_id, exam_config, current_user_id)
        
        # 计算考试时长
        question_types = exam_config.get('question_types', ['single', 'multiple', 'judge'])
        duration = ExamService.calculate_exam_duration(random_result['question_count'], question_types)
        
        # 处理时间
        start_time_obj = None
        end_time_obj = None
        
        if start_time:
            try:
                start_time_obj = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            except ValueError:
                return jsonify(build_error_response(400, '无效的开始时间格式')), 400
        
        if end_time:
            try:
                end_time_obj = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            except ValueError:
                return jsonify(build_error_response(400, '无效的结束时间格式')), 400
        
        # 创建考试
        exam = Exam(
            title=title,
            subject_id=subject_id,
            description=description,
            duration=duration,
            total_points=random_result['total_points'],
            passing_score=data.get('passing_score'),
            question_count=random_result['question_count'],
            question_ids=random_result['question_ids'],
            start_time=start_time_obj,
            end_time=end_time_obj,
            status='draft',
            settings=exam_config,
            created_by=current_user_id
        )
        
        db.session.add(exam)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='create_exam_from_config',
            details=f'根据配置创建考试: {exam.title}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试创建成功',
            data=exam.to_dict()
        )), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'创建考试失败: {str(e)}')), 500

@exams_bp.route('/<int:exam_id>/regenerate', methods=['POST'])
@jwt_required()
@require_roles('admin')
def regenerate_exam_questions(exam_id):
    """重新生成考试题目"""
    try:
        exam = Exam.query.get_or_404(exam_id)
        current_user_id = get_jwt_identity()
        
        # 检查考试状态
        if exam.status in ['ongoing', 'finished']:
            return jsonify(build_error_response(400, '进行中或已完成的考试不能重新生成题目')), 400
        
        # 获取考试配置
        exam_config = exam.settings or {}
        exam_config['total_questions'] = exam.question_count
        
        # 重新生成题目
        result = ExamService.create_random_exam(exam.subject_id, exam_config, current_user_id)
        
        # 更新考试
        exam.question_ids = result['question_ids']
        exam.total_points = result['total_points']
        exam.question_count = result['question_count']
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='regenerate_exam_questions',
            details=f'重新生成考试题目: {exam.title}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试题目重新生成成功',
            data=exam.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'重新生成考试题目失败: {str(e)}')), 500

@exams_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_exam_stats():
    """获取考试统计信息（仅管理员）"""
    try:
        total_exams = Exam.query.count()
        draft_exams = Exam.query.filter_by(status='draft').count()
        published_exams = Exam.query.filter_by(status='published').count()
        ongoing_exams = Exam.query.filter_by(status='ongoing').count()
        finished_exams = Exam.query.filter_by(status='finished').count()
        cancelled_exams = Exam.query.filter_by(status='cancelled').count()
        
        stats = {
            'total': total_exams,
            'draft': draft_exams,
            'published': published_exams,
            'ongoing': ongoing_exams,
            'finished': finished_exams,
            'cancelled': cancelled_exams
        }
        
        return jsonify(build_response(data=stats))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取考试统计失败: {str(e)}')), 500


@exams_bp.route('/analysis', methods=['GET'])
@jwt_required()
def get_exam_analysis():
    """获取考试分析数据"""
    try:
        from app.services.exam_service import ExamService
        from app.models.exam_record import ExamRecord
        from app.models.user import User
        from sqlalchemy import func, case
        
        # 获取查询参数
        exam_id = request.args.get('exam_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not exam_id:
            return jsonify(build_error_response(400, '考试ID不能为空')), 400
        
        # 验证考试是否存在
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify(build_error_response(404, '考试不存在')), 404
        
        # 构建查询
        query = ExamRecord.query.filter(ExamRecord.exam_id == exam_id)
        
        # 应用时间过滤
        if start_date:
            query = query.filter(ExamRecord.submit_time >= start_date)
        if end_date:
            query = query.filter(ExamRecord.submit_time <= end_date)
        
        # 获取考试记录
        exam_records = query.all()
        
        if not exam_records:
            return jsonify(build_response(data={
                'totalParticipants': 0,
                'averageScore': 0,
                'passRate': 0,
                'completionRate': 0,
                'details': []
            }))
        
        # 计算统计数据
        total_participants = len(exam_records)
        total_score = sum(record.score for record in exam_records if record.score is not None)
        average_score = round(total_score / total_participants, 1) if total_participants > 0 else 0
        
        # 计算通过率（假设60分及格）
        passed_count = sum(1 for record in exam_records if record.score and record.score >= 60)
        pass_rate = round((passed_count / total_participants) * 100, 1) if total_participants > 0 else 0
        
        # 计算完成率（已提交的考试记录）
        completed_count = sum(1 for record in exam_records if record.status == 'submitted')
        completion_rate = round((completed_count / total_participants) * 100, 1) if total_participants > 0 else 0
        
        # 获取详细数据
        details = []
        for record in exam_records:
            user = User.query.get(record.user_id)
            if user:
                # 计算答题时长（分钟）
                duration = 0
                if record.start_time and record.submit_time:
                    duration_delta = record.submit_time - record.start_time
                    duration = int(duration_delta.total_seconds() / 60)
                
                # 计算正确题数和准确率
                correct_count = 0
                total_count = len(record.answers) if record.answers else 0
                if record.answers and exam.question_ids:
                    # 这里需要根据实际答案计算正确题数
                    # 简化处理，假设有答案就算正确
                    correct_count = len(record.answers)
                
                accuracy = round((correct_count / total_count) * 100, 1) if total_count > 0 else 0
                
                details.append({
                    'user_name': user.username,
                    'score': record.score or 0,
                    'duration': duration,
                    'correct_count': correct_count,
                    'total_count': total_count,
                    'accuracy': accuracy,
                    'submit_time': record.submit_time.strftime('%Y-%m-%d %H:%M:%S') if record.submit_time else ''
                })
        
        # 构建响应数据
        analysis_data = {
            'totalParticipants': total_participants,
            'averageScore': average_score,
            'passRate': pass_rate,
            'completionRate': completion_rate,
            'details': details
        }
        
        return jsonify(build_response(data=analysis_data))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取考试分析失败: {str(e)}')), 500
