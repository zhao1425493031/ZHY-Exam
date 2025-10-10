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
@jwt_required()
def get_exam(exam_id):
    """获取考试详情"""
    try:
        exam = Exam.query.get_or_404(exam_id)
        return jsonify(build_response(data=exam.to_dict()))
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
        
        # 获取试题详情
        questions = Question.query.filter(Question.id.in_(exam.question_ids)).all()
        
        # 构建试题数据（不包含答案）
        question_data = []
        for question in questions:
            q_data = question.to_dict()
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
        
        # TODO: 检查用户是否已经参加过此考试
        # 这里可以添加重复考试检查逻辑
        
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
        exam = Exam.query.get_or_404(exam_id)
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        answers = data.get('answers', {})
        
        # TODO: 实现考试提交逻辑
        # 1. 创建考试记录
        # 2. 计算分数
        # 3. 记录错题
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='submit_exam',
            details=f'提交考试: {exam.title}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='考试提交成功',
            data={'exam_id': exam.id}
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'提交考试失败: {str(e)}')), 500

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

@exams_bp.route('/<int:exam_id>/check-availability', methods=['GET'])
@jwt_required()
def check_exam_availability(exam_id):
    """检查考试可用性"""
    try:
        current_user_id = get_jwt_identity()
        
        available, message = ExamService.check_exam_availability(exam_id, current_user_id)
        
        return jsonify(build_response(
            message=message,
            data={'available': available}
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'检查考试可用性失败: {str(e)}')), 500

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
