# 用户管理API
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import users_bp, BaseAPI
from app.models.user import User
from app.models import db
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import UserSchema, UserUpdateSchema, PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation

# 创建用户API实例
user_api = BaseAPI(User, UserUpdateSchema)

@users_bp.route('', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_users():
    """获取用户列表（仅管理员）"""
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
        query = User.query
        
        # 应用搜索过滤
        if search_data.get('keyword'):
            keyword = f"%{search_data['keyword']}%"
            query = query.filter(
                User.username.like(keyword) |
                User.real_name.like(keyword) |
                User.email.like(keyword)
            )
        
        if search_data.get('role'):
            query = query.filter(User.role == search_data['role'])
        
        if search_data.get('status'):
            query = query.filter(User.status == search_data['status'])
        
        # 应用排序
        sort_field = pagination_data.get('sort', 'id')
        order = pagination_data.get('order', 'desc')
        
        if hasattr(User, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(User, sort_field).desc())
            else:
                query = query.order_by(getattr(User, sort_field).asc())
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=pagination_data.get('page', 1),
            per_page=pagination_data.get('size', 10)
        )
        
        result = {
            'items': [user.to_dict() for user in pagination.items],
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

@users_bp.route('', methods=['POST'])
@jwt_required()
@require_roles('admin')
@validate_json(UserSchema)
def create_user():
    """创建用户（仅管理员）"""
    try:
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify(build_error_response(400, '用户名已存在')), 400
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=data['email']).first():
            return jsonify(build_error_response(400, '邮箱已存在')), 400
        
        # 创建用户
        user = User(
            username=data['username'],
            email=data['email'],
            real_name=data.get('real_name', ''),
            role=data.get('role', 'user'),
            phone=data.get('phone', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='create_user',
            details=f'创建用户: {user.username}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='用户创建成功',
            data=user.to_dict()
        )), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'创建用户失败: {str(e)}')), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_user(user_id):
    """获取用户详情（仅管理员）"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(build_response(data=user.to_dict()))
    except Exception as e:
        return jsonify(build_error_response(404, str(e))), 404

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
@validate_json(UserUpdateSchema)
def update_user(user_id):
    """更新用户信息（仅管理员）"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        # 检查用户名是否已被其他用户使用
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return jsonify(build_error_response(400, '用户名已存在')), 400
        
        # 检查邮箱是否已被其他用户使用
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify(build_error_response(400, '邮箱已存在')), 400
        
        # 更新用户信息
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_user',
            details=f'更新用户: {user.username}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='用户更新成功',
            data=user.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新用户失败: {str(e)}')), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_user(user_id):
    """删除用户（仅管理员）"""
    try:
        user = User.query.get_or_404(user_id)
        current_user_id = get_jwt_identity()
        
        # 不能删除自己
        if user_id == current_user_id:
            return jsonify(build_error_response(400, '不能删除自己')), 400
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='delete_user',
            details=f'删除用户: {username}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='用户删除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'删除用户失败: {str(e)}')), 500

@users_bp.route('/batch', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def batch_delete_users():
    """批量删除用户（仅管理员）"""
    try:
        data = request.get_json()
        user_ids = data.get('ids', [])
        current_user_id = get_jwt_identity()
        
        if not user_ids:
            return jsonify(build_error_response(400, '请选择要删除的用户')), 400
        
        # 不能删除自己
        if current_user_id in user_ids:
            return jsonify(build_error_response(400, '不能删除自己')), 400
        
        # 查找用户
        users = User.query.filter(User.id.in_(user_ids)).all()
        if not users:
            return jsonify(build_error_response(404, '用户不存在')), 404
        
        usernames = [user.username for user in users]
        
        # 删除用户
        for user in users:
            db.session.delete(user)
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='batch_delete_users',
            details=f'批量删除用户: {", ".join(usernames)}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message=f'成功删除 {len(users)} 个用户'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'批量删除用户失败: {str(e)}')), 500

@users_bp.route('/<int:user_id>/status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_user_status(user_id):
    """更新用户状态（仅管理员）"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        status = data.get('status')
        current_user_id = get_jwt_identity()
        
        if status not in ['active', 'inactive', 'banned']:
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        # 不能修改自己的状态
        if user_id == current_user_id:
            return jsonify(build_error_response(400, '不能修改自己的状态')), 400
        
        old_status = user.status
        user.status = status
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_user_status',
            details=f'修改用户状态: {user.username} ({old_status} -> {status})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='用户状态更新成功',
            data={'status': user.status}
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新用户状态失败: {str(e)}')), 500

@users_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_user_stats():
    """获取用户统计信息（仅管理员）"""
    try:
        total_users = User.query.count()
        active_users = User.query.filter_by(status='active').count()
        inactive_users = User.query.filter_by(status='inactive').count()
        banned_users = User.query.filter_by(status='banned').count()
        admin_users = User.query.filter_by(role='admin').count()
        normal_users = User.query.filter_by(role='user').count()
        
        stats = {
            'total': total_users,
            'active': active_users,
            'inactive': inactive_users,
            'banned': banned_users,
            'admin': admin_users,
            'user': normal_users
        }
        
        return jsonify(build_response(data=stats))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取用户统计失败: {str(e)}')), 500



