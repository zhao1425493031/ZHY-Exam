# 考试记录API
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import exam_records_bp, BaseAPI
from app.models.exam_record import ExamRecord
from app.models.exam import Exam
from app.models.question import Question
from app.models import db
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import ExamRecordSchema, PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation
from datetime import datetime

# 创建考试记录API实例
exam_record_api = BaseAPI(ExamRecord, ExamRecordSchema)

@exam_records_bp.route('', methods=['GET'])
@jwt_required()
def get_exam_records():
    """获取考试记录列表"""
    try:
        current_user_id = get_jwt_identity()
        
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
        query = ExamRecord.query.filter_by(user_id=current_user_id)
        
        # 应用搜索过滤
        if search_data.get('exam_id'):
            query = query.filter(ExamRecord.exam_id == search_data['exam_id'])
        
        if search_data.get('status'):
            query = query.filter(ExamRecord.status == search_data['status'])
        
        # 应用排序
        sort_field = pagination_data.get('sort', 'id')
        order = pagination_data.get('order', 'desc')
        
        if hasattr(ExamRecord, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(ExamRecord, sort_field).desc())
            else:
                query = query.order_by(getattr(ExamRecord, sort_field).asc())
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=pagination_data.get('page', 1),
            per_page=pagination_data.get('size', 10)
        )
        
        result = {
            'items': [record.to_dict() for record in pagination.items],
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

@exam_records_bp.route('/<int:record_id>', methods=['GET'])
@jwt_required()
def get_exam_record(record_id):
    """获取考试记录详情"""
    try:
        current_user_id = get_jwt_identity()
        record = ExamRecord.query.filter_by(id=record_id, user_id=current_user_id).first_or_404()
        
        # 获取考试信息
        exam = Exam.query.get(record.exam_id)
        
        result = record.to_dict()
        result['exam'] = exam.to_dict() if exam else None
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        return jsonify(build_error_response(404, str(e))), 404

@exam_records_bp.route('/<int:record_id>/answers', methods=['GET'])
@jwt_required()
def get_exam_answers(record_id):
    """获取考试答案详情"""
    try:
        current_user_id = get_jwt_identity()
        record = ExamRecord.query.filter_by(id=record_id, user_id=current_user_id).first_or_404()
        
        # 获取考试信息
        exam = Exam.query.get(record.exam_id)
        if not exam:
            return jsonify(build_error_response(404, '考试不存在')), 404
        
        # 获取试题信息
        questions = Question.query.filter(Question.id.in_(exam.question_ids)).all()
        
        # 构建答案详情
        answer_details = []
        for question in questions:
            user_answer = record.answers.get(str(question.id), '')
            correct_answer = question.answer
            
            answer_detail = {
                'question_id': question.id,
                'title': question.title,
                'type': question.type,
                'options': question.options,
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': user_answer == correct_answer,
                'points': question.points,
                'explanation': question.explanation
            }
            answer_details.append(answer_detail)
        
        result = {
            'record': record.to_dict(),
            'exam': exam.to_dict(),
            'answers': answer_details
        }
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取考试答案失败: {str(e)}')), 500

@exam_records_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_exam_record_stats():
    """获取考试记录统计信息"""
    try:
        current_user_id = get_jwt_identity()
        
        # 基础统计
        total_records = ExamRecord.query.filter_by(user_id=current_user_id).count()
        submitted_records = ExamRecord.query.filter_by(user_id=current_user_id, status='submitted').count()
        in_progress_records = ExamRecord.query.filter_by(user_id=current_user_id, status='in_progress').count()
        timeout_records = ExamRecord.query.filter_by(user_id=current_user_id, status='timeout').count()
        
        # 分数统计
        submitted_with_score = ExamRecord.query.filter_by(
            user_id=current_user_id, 
            status='submitted'
        ).filter(ExamRecord.score.isnot(None)).all()
        
        if submitted_with_score:
            scores = [float(record.score) for record in submitted_with_score]
            avg_score = sum(scores) / len(scores)
            max_score = max(scores)
            min_score = min(scores)
        else:
            avg_score = 0
            max_score = 0
            min_score = 0
        
        stats = {
            'total': total_records,
            'submitted': submitted_records,
            'in_progress': in_progress_records,
            'timeout': timeout_records,
            'avg_score': round(avg_score, 2),
            'max_score': max_score,
            'min_score': min_score
        }
        
        return jsonify(build_response(data=stats))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取考试记录统计失败: {str(e)}')), 500

@exam_records_bp.route('/wrong-answers', methods=['GET'])
@jwt_required()
def get_wrong_answers():
    """获取错题记录"""
    try:
        current_user_id = get_jwt_identity()
        
        # 验证分页参数
        pagination_schema = PaginationSchema()
        pagination_data = pagination_schema.load({
            'page': request.args.get('page', 1, type=int),
            'size': request.args.get('size', 10, type=int),
            'sort': request.args.get('sort', 'id'),
            'order': request.args.get('order', 'desc')
        })
        
        # 获取已提交的考试记录
        submitted_records = ExamRecord.query.filter_by(
            user_id=current_user_id,
            status='submitted'
        ).all()
        
        wrong_answers = []
        for record in submitted_records:
            exam = Exam.query.get(record.exam_id)
            if not exam:
                continue
            
            # 获取试题信息
            questions = Question.query.filter(Question.id.in_(exam.question_ids)).all()
            
            for question in questions:
                user_answer = record.answers.get(str(question.id), '')
                correct_answer = question.answer
                
                if user_answer != correct_answer:
                    wrong_answer = {
                        'record_id': record.id,
                        'exam_id': exam.id,
                        'exam_title': exam.title,
                        'question_id': question.id,
                        'question_title': question.title,
                        'question_type': question.type,
                        'user_answer': user_answer,
                        'correct_answer': correct_answer,
                        'explanation': question.explanation,
                        'submit_time': record.submit_time.isoformat() if record.submit_time else None
                    }
                    wrong_answers.append(wrong_answer)
        
        # 分页处理
        total = len(wrong_answers)
        page = pagination_data.get('page', 1)
        per_page = pagination_data.get('size', 10)
        start = (page - 1) * per_page
        end = start + per_page
        
        paginated_wrong_answers = wrong_answers[start:end]
        
        result = {
            'items': paginated_wrong_answers,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page,
            'per_page': per_page,
            'has_next': end < total,
            'has_prev': page > 1
        }
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取错题记录失败: {str(e)}')), 500

@exam_records_bp.route('/admin', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_all_exam_records():
    """获取所有考试记录（仅管理员）"""
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
        query = ExamRecord.query
        
        # 应用搜索过滤
        if search_data.get('exam_id'):
            query = query.filter(ExamRecord.exam_id == search_data['exam_id'])
        
        if search_data.get('user_id'):
            query = query.filter(ExamRecord.user_id == search_data['user_id'])
        
        if search_data.get('status'):
            query = query.filter(ExamRecord.status == search_data['status'])
        
        # 应用排序
        sort_field = pagination_data.get('sort', 'id')
        order = pagination_data.get('order', 'desc')
        
        if hasattr(ExamRecord, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(ExamRecord, sort_field).desc())
            else:
                query = query.order_by(getattr(ExamRecord, sort_field).asc())
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=pagination_data.get('page', 1),
            per_page=pagination_data.get('size', 10)
        )
        
        result = {
            'items': [record.to_dict() for record in pagination.items],
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
