# 试题管理API
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import questions_bp, BaseAPI
from app.models.question import Question
from app.models.subject import Subject
from app.models import db
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import QuestionSchema, PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation
from app.services.question_import_export_service import QuestionImportExportService

# 创建试题API实例
question_api = BaseAPI(Question, QuestionSchema)

@questions_bp.route('', methods=['GET'])
@jwt_required()
def get_questions():
    """获取试题列表"""
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
        query = Question.query
        
        # 应用搜索过滤
        if search_data.get('keyword'):
            keyword = f"%{search_data['keyword']}%"
            query = query.filter(
                Question.title.like(keyword) |
                Question.content.like(keyword)
            )
        
        if search_data.get('subject_id'):
            query = query.filter(Question.subject_id == search_data['subject_id'])
        
        if search_data.get('type'):
            query = query.filter(Question.type == search_data['type'])
        
        if search_data.get('difficulty'):
            query = query.filter(Question.difficulty == search_data['difficulty'])
        
        if search_data.get('status'):
            query = query.filter(Question.status == search_data['status'])
        
        # 应用排序
        sort_field = pagination_data.get('sort', 'id')
        order = pagination_data.get('order', 'desc')
        
        if hasattr(Question, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(Question, sort_field).desc())
            else:
                query = query.order_by(getattr(Question, sort_field).asc())
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=pagination_data.get('page', 1),
            per_page=pagination_data.get('size', 10)
        )
        
        result = {
            'items': [question.to_dict() for question in pagination.items],
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

@questions_bp.route('', methods=['POST'])
@jwt_required()
@require_roles('admin')
@validate_json(QuestionSchema)
def create_question():
    """创建试题（仅管理员）"""
    try:
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 验证科目是否存在
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 创建试题
        question = Question(
            subject_id=data['subject_id'],
            type=data['type'],
            title=data['title'],
            content=data.get('content', ''),
            options=data.get('options', []),
            answer=data['answer'],
            explanation=data.get('explanation', ''),
            difficulty=data.get('difficulty', 'medium'),
            tags=data.get('tags', []),
            points=data.get('points', 1),
            status=data.get('status', 'draft'),
            created_by=current_user_id
        )
        
        db.session.add(question)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='create_question',
            details=f'创建试题: {question.title[:50]}...',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='试题创建成功',
            data=question.to_dict()
        )), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'创建试题失败: {str(e)}')), 500

@questions_bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_question(question_id):
    """获取试题详情"""
    try:
        question = Question.query.get_or_404(question_id)
        return jsonify(build_response(data=question.to_dict()))
    except Exception as e:
        return jsonify(build_error_response(404, str(e))), 404

@questions_bp.route('/<int:question_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
@validate_json(QuestionSchema)
def update_question(question_id):
    """更新试题信息（仅管理员）"""
    try:
        question = Question.query.get_or_404(question_id)
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 验证科目是否存在
        if 'subject_id' in data:
            subject = Subject.query.get(data['subject_id'])
            if not subject:
                return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 更新试题信息
        for key, value in data.items():
            if hasattr(question, key):
                setattr(question, key, value)
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_question',
            details=f'更新试题: {question.title[:50]}...',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='试题更新成功',
            data=question.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新试题失败: {str(e)}')), 500

@questions_bp.route('/<int:question_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_question(question_id):
    """删除试题（仅管理员）"""
    try:
        question = Question.query.get_or_404(question_id)
        current_user_id = get_jwt_identity()
        
        # TODO: 检查是否有考试关联此试题
        # 这里可以添加关联检查逻辑
        
        title = question.title
        db.session.delete(question)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='delete_question',
            details=f'删除试题: {title[:50]}...',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='试题删除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'删除试题失败: {str(e)}')), 500

@questions_bp.route('/<int:question_id>/status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_question_status(question_id):
    """更新试题状态（仅管理员）"""
    try:
        question = Question.query.get_or_404(question_id)
        data = request.get_json()
        status = data.get('status')
        current_user_id = get_jwt_identity()
        
        if status not in ['draft', 'published', 'archived']:
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        old_status = question.status
        question.status = status
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_question_status',
            details=f'修改试题状态: {question.title[:30]}... ({old_status} -> {status})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='试题状态更新成功',
            data={'status': question.status}
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新试题状态失败: {str(e)}')), 500

@questions_bp.route('/types', methods=['GET'])
@jwt_required()
def get_question_types():
    """获取试题类型列表"""
    try:
        types = [
            {'value': 'single', 'label': '单选题'},
            {'value': 'multiple', 'label': '多选题'},
            {'value': 'judge', 'label': '判断题'},
            {'value': 'fill', 'label': '填空题'},
            {'value': 'essay', 'label': '简答题'}
        ]
        
        return jsonify(build_response(data=types))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取试题类型失败: {str(e)}')), 500

@questions_bp.route('/difficulties', methods=['GET'])
@jwt_required()
def get_question_difficulties():
    """获取试题难度列表"""
    try:
        difficulties = [
            {'value': 'easy', 'label': '简单'},
            {'value': 'medium', 'label': '中等'},
            {'value': 'hard', 'label': '困难'}
        ]
        
        return jsonify(build_response(data=difficulties))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取试题难度失败: {str(e)}')), 500

@questions_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_question_stats():
    """获取试题统计信息（仅管理员）"""
    try:
        total_questions = Question.query.count()
        draft_questions = Question.query.filter_by(status='draft').count()
        published_questions = Question.query.filter_by(status='published').count()
        archived_questions = Question.query.filter_by(status='archived').count()
        
        # 按类型统计
        type_stats = {}
        for qtype in ['single', 'multiple', 'judge', 'fill', 'essay']:
            count = Question.query.filter_by(type=qtype).count()
            type_stats[qtype] = count
        
        # 按难度统计
        difficulty_stats = {}
        for difficulty in ['easy', 'medium', 'hard']:
            count = Question.query.filter_by(difficulty=difficulty).count()
            difficulty_stats[difficulty] = count
        
        stats = {
            'total': total_questions,
            'draft': draft_questions,
            'published': published_questions,
            'archived': archived_questions,
            'by_type': type_stats,
            'by_difficulty': difficulty_stats
        }
        
@questions_bp.route('/import', methods=['POST'])
@jwt_required()
@require_roles('admin')
def import_questions():
    """批量导入试题（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify(build_error_response(400, '请选择要导入的文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(build_error_response(400, '请选择要导入的文件')), 400
        
        # 获取科目ID
        subject_id = request.form.get('subject_id')
        if not subject_id:
            return jsonify(build_error_response(400, '请选择科目')), 400
        
        try:
            subject_id = int(subject_id)
        except ValueError:
            return jsonify(build_error_response(400, '无效的科目ID')), 400
        
        # 验证科目是否存在
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 执行导入
        result = QuestionImportExportService.import_questions_from_excel(
            file, subject_id, current_user_id
        )
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='import_questions',
            details=f'批量导入试题到科目 {subject.name}: 成功{result["success_count"]}题，失败{result["error_count"]}题',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message=f'导入完成：成功{result["success_count"]}题，失败{result["error_count"]}题',
            data=result
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'导入试题失败: {str(e)}')), 500

@questions_bp.route('/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_questions():
    """导出试题（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取参数
        subject_id = request.args.get('subject_id', type=int)
        question_ids = request.args.get('question_ids')
        
        # 处理试题ID列表
        if question_ids:
            try:
                question_ids = [int(id) for id in question_ids.split(',')]
            except ValueError:
                return jsonify(build_error_response(400, '无效的试题ID列表')), 400
        
        # 执行导出
        file_response = QuestionImportExportService.export_questions_to_excel(
            subject_id=subject_id,
            question_ids=question_ids
        )
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='export_questions',
            details=f'导出试题: 科目ID={subject_id}, 试题数量={len(question_ids) if question_ids else "全部"}',
            ip=get_client_ip(request)
        )
        
        return file_response
        
    except Exception as e:
        return jsonify(build_error_response(500, f'导出试题失败: {str(e)}')), 500

@questions_bp.route('/import-template', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_import_template():
    """获取导入模板（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        # 生成模板文件
        file_response = QuestionImportExportService.get_import_template()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='download_import_template',
            details='下载试题导入模板',
            ip=get_client_ip(request)
        )
        
        return file_response
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取模板失败: {str(e)}')), 500

@questions_bp.route('/batch-delete', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def batch_delete_questions():
    """批量删除试题（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        question_ids = data.get('ids')
        if not isinstance(question_ids, list) or not question_ids:
            return jsonify(build_error_response(400, '请提供要删除的试题ID列表')), 400
        
        # 检查试题是否存在
        questions = Question.query.filter(Question.id.in_(question_ids)).all()
        if len(questions) != len(question_ids):
            return jsonify(build_error_response(400, '部分试题不存在')), 400
        
        # TODO: 检查是否有考试关联这些试题
        # 这里可以添加关联检查逻辑
        
        # 删除试题
        deleted_count = Question.query.filter(Question.id.in_(question_ids)).delete(synchronize_session=False)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='batch_delete_questions',
            details=f'批量删除试题ID: {question_ids}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message=f'成功删除 {deleted_count} 个试题'
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'批量删除试题失败: {str(e)}')), 500

@questions_bp.route('/batch-update-status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def batch_update_question_status():
    """批量更新试题状态（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        question_ids = data.get('ids')
        status = data.get('status')
        
        if not isinstance(question_ids, list) or not question_ids:
            return jsonify(build_error_response(400, '请提供要更新的试题ID列表')), 400
        
        if status not in ['draft', 'published', 'archived']:
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        # 更新试题状态
        updated_count = Question.query.filter(Question.id.in_(question_ids)).update(
            {'status': status}, synchronize_session=False
        )
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='batch_update_question_status',
            details=f'批量更新试题状态: {question_ids} -> {status}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message=f'成功更新 {updated_count} 个试题状态'
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'批量更新试题状态失败: {str(e)}')), 500
