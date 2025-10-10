# 科目管理API
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import subjects_bp, BaseAPI
from app.models.subject import Subject
from app.models import db
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import SubjectSchema, PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation

# 创建科目API实例
subject_api = BaseAPI(Subject, SubjectSchema)

@subjects_bp.route('', methods=['GET'])
def get_subjects():
    """获取科目列表"""
    try:
        # 验证所有参数（包括分页和搜索参数）
        search_schema = SearchSchema()
        all_data = search_schema.load(request.args)
        
        # 构建查询
        query = Subject.query
        
        # 应用搜索过滤
        if all_data.get('keyword'):
            keyword = f"%{all_data['keyword']}%"
            query = query.filter(
                Subject.name.like(keyword) |
                Subject.code.like(keyword) |
                Subject.description.like(keyword)
            )
        
        if all_data.get('status'):
            query = query.filter(Subject.status == all_data['status'])
        
        if all_data.get('category'):
            query = query.filter(Subject.category == all_data['category'])
        
        # 应用排序
        sort_field = all_data.get('sort', 'id')
        order = all_data.get('order', 'desc')
        
        if hasattr(Subject, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(Subject, sort_field).desc())
            else:
                query = query.order_by(getattr(Subject, sort_field).asc())
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=all_data.get('page', 1),
            per_page=all_data.get('size', 10)
        )
        
        result = {
            'items': [subject.to_dict() for subject in pagination.items],
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

@subjects_bp.route('', methods=['POST'])
@jwt_required()
@require_roles('admin')
@validate_json(SubjectSchema)
def create_subject():
    """创建科目（仅管理员）"""
    try:
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 检查科目代码是否已存在
        if Subject.query.filter_by(code=data['code']).first():
            return jsonify(build_error_response(400, '科目代码已存在')), 400
        
        # 创建科目
        subject = Subject(
            name=data['name'],
            code=data['code'],
            description=data.get('description', ''),
            category=data.get('category', ''),
            status=data.get('status', 'active'),
            created_by=current_user_id
        )
        
        db.session.add(subject)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='create_subject',
            details=f'创建科目: {subject.name} ({subject.code})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='科目创建成功',
            data=subject.to_dict()
        )), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'创建科目失败: {str(e)}')), 500

@subjects_bp.route('/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_subject(subject_id):
    """获取科目详情"""
    try:
        subject = Subject.query.get_or_404(subject_id)
        return jsonify(build_response(data=subject.to_dict()))
    except Exception as e:
        return jsonify(build_error_response(404, str(e))), 404

@subjects_bp.route('/<int:subject_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
@validate_json(SubjectSchema)
def update_subject(subject_id):
    """更新科目信息（仅管理员）"""
    try:
        subject = Subject.query.get_or_404(subject_id)
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 检查科目代码是否已被其他科目使用
        if 'code' in data and data['code'] != subject.code:
            if Subject.query.filter_by(code=data['code']).first():
                return jsonify(build_error_response(400, '科目代码已存在')), 400
        
        # 更新科目信息
        for key, value in data.items():
            if hasattr(subject, key):
                setattr(subject, key, value)
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_subject',
            details=f'更新科目: {subject.name} ({subject.code})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='科目更新成功',
            data=subject.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新科目失败: {str(e)}')), 500

@subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_subject(subject_id):
    """删除科目（仅管理员）"""
    try:
        subject = Subject.query.get_or_404(subject_id)
        current_user_id = get_jwt_identity()
        
        # TODO: 检查是否有试题或考试关联此科目
        # 这里可以添加关联检查逻辑
        
        name = subject.name
        code = subject.code
        db.session.delete(subject)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='delete_subject',
            details=f'删除科目: {name} ({code})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='科目删除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'删除科目失败: {str(e)}')), 500

@subjects_bp.route('/<int:subject_id>/status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_subject_status(subject_id):
    """更新科目状态（仅管理员）"""
    try:
        subject = Subject.query.get_or_404(subject_id)
        data = request.get_json()
        status = data.get('status')
        current_user_id = get_jwt_identity()
        
        if status not in ['active', 'inactive']:
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        old_status = subject.status
        subject.status = status
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_subject_status',
            details=f'修改科目状态: {subject.name} ({old_status} -> {status})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='科目状态更新成功',
            data={'status': subject.status}
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新科目状态失败: {str(e)}')), 500

@subjects_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """获取科目分类列表"""
    try:
        categories = db.session.query(Subject.category).filter(
            Subject.category.isnot(None),
            Subject.category != ''
        ).distinct().all()
        
        category_list = [cat[0] for cat in categories if cat[0]]
        
        return jsonify(build_response(data=category_list))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取科目分类失败: {str(e)}')), 500

@subjects_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_subject_stats():
    """获取科目统计信息（仅管理员）"""
    try:
        total_subjects = Subject.query.count()
        active_subjects = Subject.query.filter_by(status='active').count()
        inactive_subjects = Subject.query.filter_by(status='inactive').count()
        
        # 获取分类统计
        categories = db.session.query(Subject.category).filter(
            Subject.category.isnot(None),
            Subject.category != ''
        ).distinct().count()
        
        stats = {
            'total': total_subjects,
            'active': active_subjects,
            'inactive': inactive_subjects,
            'categories': categories
        }
        
        return jsonify(build_response(data=stats))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取科目统计失败: {str(e)}')), 500



