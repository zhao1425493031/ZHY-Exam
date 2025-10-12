# 认证API
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.api import auth_bp
from app.models.user import User
from app.models import db
from app.utils.decorators import validate_json
from app.utils.validators import UserSchema, LoginSchema, ChangePasswordSchema, ProfileUpdateSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation

@auth_bp.route('/register', methods=['POST'])
@validate_json(UserSchema)
def register():
    """用户注册"""
    try:
        data = request.validated_data
        
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
            user_id=user.id,
            operation='register',
            details=f'用户注册: {user.username}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='注册成功',
            data={'user_id': user.id, 'username': user.username}
        )), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'注册失败: {str(e)}')), 500

@auth_bp.route('/login', methods=['POST'])
@validate_json(LoginSchema)
def login():
    """用户登录"""
    try:
        data = request.validated_data
        
        # 查找用户
        user = User.query.filter_by(username=data['username']).first()
        if not user or not user.check_password(data['password']):
            return jsonify(build_error_response(401, '用户名或密码错误')), 401
        
        # 检查用户状态
        if user.status != 'active':
            return jsonify(build_error_response(403, '账户已被禁用')), 403
        
        # 生成JWT token
        access_token = create_access_token(identity=str(user.id))
        
        # 记录操作日志
        log_operation(
            user_id=user.id,
            operation='login',
            details=f'用户登录: {user.username}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='登录成功',
            data={
                'token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'real_name': user.real_name,
                    'role': user.role,
                    'status': user.status,
                    'avatar_url': user.avatar_url,
                    'phone': user.phone
                }
            }
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'登录失败: {str(e)}')), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户登出"""
    try:
        user_id = get_jwt_identity()
        
        # 记录操作日志
        log_operation(
            user_id=user_id,
            operation='logout',
            details='用户登出',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='登出成功'))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'登出失败: {str(e)}')), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        
        return jsonify(build_response(data={
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'real_name': user.real_name,
            'role': user.role,
            'status': user.status,
            'avatar_url': user.avatar_url,
            'phone': user.phone,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'获取用户信息失败: {str(e)}')), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
@validate_json(ProfileUpdateSchema)
def update_profile():
    """更新用户信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        data = request.validated_data
        
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
            if key == 'password':
                # 特殊处理密码字段
                if value:  # 只有当密码不为空时才更新
                    user.set_password(value)
            elif hasattr(user, key):
                setattr(user, key, value)
        
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=user_id,
            operation='update_profile',
            details='更新用户信息',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='更新成功',
            data=user.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新用户信息失败: {str(e)}')), 500

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
@validate_json(ChangePasswordSchema)
def change_password():
    """修改密码"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        data = request.validated_data
        
        # 验证旧密码
        if not user.check_password(data['old_password']):
            return jsonify(build_error_response(400, '旧密码错误')), 400
        
        # 设置新密码
        user.set_password(data['new_password'])
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=user_id,
            operation='change_password',
            details='修改密码',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='密码修改成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(build_error_response(500, f'密码修改失败: {str(e)}')), 500

@auth_bp.route('/check-username', methods=['POST'])
def check_username():
    """检查用户名是否可用"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        
        if not username:
            return jsonify(build_error_response(400, '用户名不能为空')), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify(build_response(data={'available': False, 'message': '用户名已存在'}))
        else:
            return jsonify(build_response(data={'available': True, 'message': '用户名可用'}))
            
    except Exception as e:
        return jsonify(build_error_response(500, f'检查用户名失败: {str(e)}')), 500

@auth_bp.route('/check-email', methods=['POST'])
def check_email():
    """检查邮箱是否可用"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        
        if not email:
            return jsonify(build_error_response(400, '邮箱不能为空')), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify(build_response(data={'available': False, 'message': '邮箱已存在'}))
        else:
            return jsonify(build_response(data={'available': True, 'message': '邮箱可用'}))
            
    except Exception as e:
        return jsonify(build_error_response(500, f'检查邮箱失败: {str(e)}')), 500
