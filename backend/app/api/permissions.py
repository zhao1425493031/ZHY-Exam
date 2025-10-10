from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.permission_service import PermissionService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
permission_bp = Blueprint('permissions', __name__, url_prefix='/api/permissions')

@permission_bp.route('/', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_permissions():
    """获取权限列表（管理员）"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        type_filter = request.args.get('type')
        status = request.args.get('status')
        
        # 构建查询参数
        params = {
            'page': page,
            'size': size
        }
        
        if type_filter:
            params['type'] = type_filter
        if status:
            params['status'] = status
        
        # 获取权限列表
        permissions = PermissionService.get_permissions(params)
        
        return jsonify(build_response(data=permissions))
        
    except Exception as e:
        logger.error(f'Get permissions error: {str(e)}')
        return jsonify(build_error_response(500, f'获取权限列表失败: {str(e)}')), 500

@permission_bp.route('/tree', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_permission_tree():
    """获取权限树（管理员）"""
    try:
        permissions = PermissionService.get_permission_tree()
        
        return jsonify(build_response(data=permissions))
        
    except Exception as e:
        logger.error(f'Get permission tree error: {str(e)}')
        return jsonify(build_error_response(500, f'获取权限树失败: {str(e)}')), 500

@permission_bp.route('/<int:permission_id>', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_permission(permission_id):
    """获取单个权限详情（管理员）"""
    try:
        permission = PermissionService.get_permission(permission_id)
        
        return jsonify(build_response(data=permission))
        
    except Exception as e:
        logger.error(f'Get permission error: {str(e)}')
        return jsonify(build_error_response(500, f'获取权限详情失败: {str(e)}')), 500

@permission_bp.route('/', methods=['POST'])
@jwt_required()
@require_roles('admin')
def create_permission():
    """创建权限（管理员）"""
    try:
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['name', 'code', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 创建权限
        permission = PermissionService.create_permission(data)
        
        return jsonify(build_response(data=permission))
        
    except Exception as e:
        logger.error(f'Create permission error: {str(e)}')
        return jsonify(build_error_response(500, f'创建权限失败: {str(e)}')), 500

@permission_bp.route('/<int:permission_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_permission(permission_id):
    """更新权限（管理员）"""
    try:
        data = request.get_json()
        
        # 更新权限
        permission = PermissionService.update_permission(permission_id, data)
        
        return jsonify(build_response(data=permission))
        
    except Exception as e:
        logger.error(f'Update permission error: {str(e)}')
        return jsonify(build_error_response(500, f'更新权限失败: {str(e)}')), 500

@permission_bp.route('/<int:permission_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_permission(permission_id):
    """删除权限（管理员）"""
    try:
        PermissionService.delete_permission(permission_id)
        
        return jsonify(build_response(data={'message': '删除权限成功'}))
        
    except Exception as e:
        logger.error(f'Delete permission error: {str(e)}')
        return jsonify(build_error_response(500, f'删除权限失败: {str(e)}')), 500

@permission_bp.route('/role/<role>', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_role_permissions(role):
    """获取角色权限（管理员）"""
    try:
        permissions = PermissionService.get_role_permissions(role)
        
        return jsonify(build_response(data=permissions))
        
    except Exception as e:
        logger.error(f'Get role permissions error: {str(e)}')
        return jsonify(build_error_response(500, f'获取角色权限失败: {str(e)}')), 500

@permission_bp.route('/role/<role>', methods=['POST'])
@jwt_required()
@require_roles('admin')
def set_role_permissions(role):
    """设置角色权限（管理员）"""
    try:
        data = request.get_json()
        permission_ids = data.get('permission_ids', [])
        
        # 设置角色权限
        PermissionService.set_role_permissions(role, permission_ids)
        
        return jsonify(build_response(data={'message': '设置角色权限成功'}))
        
    except Exception as e:
        logger.error(f'Set role permissions error: {str(e)}')
        return jsonify(build_error_response(500, f'设置角色权限失败: {str(e)}')), 500

@permission_bp.route('/role/<role>/<int:permission_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def remove_role_permission(role, permission_id):
    """移除角色权限（管理员）"""
    try:
        PermissionService.remove_role_permission(role, permission_id)
        
        return jsonify(build_response(data={'message': '移除角色权限成功'}))
        
    except Exception as e:
        logger.error(f'Remove role permission error: {str(e)}')
        return jsonify(build_error_response(500, f'移除角色权限失败: {str(e)}')), 500

@permission_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_user_permissions(user_id):
    """获取用户权限（管理员）"""
    try:
        permissions = PermissionService.get_user_permissions(user_id)
        
        return jsonify(build_response(data=permissions))
        
    except Exception as e:
        logger.error(f'Get user permissions error: {str(e)}')
        return jsonify(build_error_response(500, f'获取用户权限失败: {str(e)}')), 500

@permission_bp.route('/check', methods=['POST'])
@jwt_required()
def check_permission():
    """检查用户权限"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        permission_code = data.get('permission_code')
        if not permission_code:
            return jsonify(build_error_response(400, '缺少权限代码')), 400
        
        # 检查权限
        has_permission = PermissionService.check_user_permission(current_user_id, permission_code)
        
        return jsonify(build_response(data={'has_permission': has_permission}))
        
    except Exception as e:
        logger.error(f'Check permission error: {str(e)}')
        return jsonify(build_error_response(500, f'检查权限失败: {str(e)}')), 500

@permission_bp.route('/menu', methods=['GET'])
@jwt_required()
def get_user_menu():
    """获取用户菜单权限"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取用户菜单权限
        menu_permissions = PermissionService.get_user_menu_permissions(current_user_id)
        
        return jsonify(build_response(data=menu_permissions))
        
    except Exception as e:
        logger.error(f'Get user menu error: {str(e)}')
        return jsonify(build_error_response(500, f'获取用户菜单失败: {str(e)}')), 500

@permission_bp.route('/init', methods=['POST'])
@jwt_required()
@require_roles('admin')
def init_permissions():
    """初始化权限数据（管理员）"""
    try:
        PermissionService.init_default_permissions()
        
        return jsonify(build_response(data={'message': '初始化权限数据成功'}))
        
    except Exception as e:
        logger.error(f'Init permissions error: {str(e)}')
        return jsonify(build_error_response(500, f'初始化权限数据失败: {str(e)}')), 500
