# 装饰器工具
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

def require_roles(*roles):
    """角色权限装饰器"""
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            from app.models.user import User
            current_user_id = get_jwt_identity()
            # 将字符串ID转换为整数
            current_user = User.query.get(int(current_user_id))
            
            if not current_user or current_user.role not in roles:
                return jsonify({'message': '权限不足'}), 403
            
            # 将当前用户添加到请求上下文
            request.current_user = current_user
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_json(schema_class):
    """JSON数据验证装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from app.services.log_service import LogService
            
            try:
                data = request.get_json()
                LogService.log_info(f"[VALIDATE_JSON] 接收到原始数据: {data}", 'VALIDATION')
                
                if not data:
                    LogService.log_warning("[VALIDATE_JSON] 请求数据为空", 'VALIDATION')
                    return jsonify({'message': '请求数据不能为空'}), 400
                
                # 实例化schema并加载数据
                schema = schema_class()
                validated_data = schema.load(data)
                LogService.log_info(f"[VALIDATE_JSON] 验证通过的数据: {validated_data}", 'VALIDATION')
                
                request.validated_data = validated_data
                return f(*args, **kwargs)
            except ValidationError as e:
                LogService.log_error(f"[VALIDATE_JSON] 数据验证失败: {e.messages}", 'VALIDATION')
                LogService.log_error(f"[VALIDATE_JSON] 原始数据: {request.get_json()}", 'VALIDATION')
                LogService.log_error(f"[VALIDATE_JSON] Schema: {schema_class.__name__}", 'VALIDATION')
                return jsonify({
                    'message': '数据验证失败', 
                    'errors': e.messages
                }), 422
        return decorated_function
    return decorator

def admin_required(f):
    """管理员权限装饰器"""
    return require_roles('admin')(f)

def teacher_required(f):
    """教师权限装饰器"""
    return require_roles('admin', 'teacher')(f)
