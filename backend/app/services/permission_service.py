from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models.user import User
from app.models.permission import Permission, PermissionType, PermissionStatus
from app.models.role_permission import RolePermission
from app import db
import logging

logger = logging.getLogger(__name__)

class PermissionService:
    """权限服务"""
    
    @staticmethod
    def get_permissions(params: Dict[str, Any]) -> Dict[str, Any]:
        """获取权限列表"""
        try:
            page = params.get('page', 1)
            size = params.get('size', 10)
            type_filter = params.get('type')
            status = params.get('status')
            
            # 构建查询
            query = Permission.query
            
            if type_filter:
                query = query.filter(Permission.type == PermissionType(type_filter))
            
            if status:
                query = query.filter(Permission.status == PermissionStatus(status))
            
            # 分页查询
            pagination = query.order_by(Permission.sort_order, Permission.created_at).paginate(
                page=page, 
                per_page=size, 
                error_out=False
            )
            
            return {
                'items': [permission.to_dict() for permission in pagination.items],
                'total': pagination.total,
                'page': page,
                'size': size,
                'pages': pagination.pages
            }
            
        except Exception as e:
            logger.error(f'Get permissions error: {str(e)}')
            raise Exception(f'获取权限列表失败: {str(e)}')
    
    @staticmethod
    def get_permission_tree() -> List[Dict[str, Any]]:
        """获取权限树"""
        try:
            # 获取所有权限
            permissions = Permission.query.filter(
                Permission.status == PermissionStatus.ACTIVE
            ).order_by(Permission.sort_order, Permission.created_at).all()
            
            # 构建树形结构
            permission_dict = {}
            root_permissions = []
            
            for permission in permissions:
                permission_dict[permission.id] = permission.to_tree_dict()
            
            for permission in permissions:
                if permission.parent_id == 0:
                    root_permissions.append(permission_dict[permission.id])
                else:
                    parent = permission_dict.get(permission.parent_id)
                    if parent:
                        if 'children' not in parent:
                            parent['children'] = []
                        parent['children'].append(permission_dict[permission.id])
            
            return root_permissions
            
        except Exception as e:
            logger.error(f'Get permission tree error: {str(e)}')
            raise Exception(f'获取权限树失败: {str(e)}')
    
    @staticmethod
    def get_permission(permission_id: int) -> Dict[str, Any]:
        """获取单个权限详情"""
        try:
            permission = Permission.query.get(permission_id)
            
            if not permission:
                raise Exception('权限不存在')
            
            return permission.to_dict()
            
        except Exception as e:
            logger.error(f'Get permission error: {str(e)}')
            raise Exception(f'获取权限详情失败: {str(e)}')
    
    @staticmethod
    def create_permission(data: Dict[str, Any]) -> Dict[str, Any]:
        """创建权限"""
        try:
            # 验证必要参数
            name = data.get('name')
            code = data.get('code')
            permission_type = data.get('type')
            
            if not name or not code or not permission_type:
                raise Exception('权限名称、代码和类型不能为空')
            
            # 检查权限代码是否已存在
            existing_permission = Permission.query.filter_by(code=code).first()
            if existing_permission:
                raise Exception('权限代码已存在')
            
            # 创建权限
            permission = Permission(
                name=name,
                code=code,
                type=PermissionType(permission_type),
                parent_id=data.get('parent_id', 0),
                path=data.get('path'),
                icon=data.get('icon'),
                sort_order=data.get('sort_order', 0),
                status=PermissionStatus(data.get('status', 'active'))
            )
            
            db.session.add(permission)
            db.session.commit()
            
            return permission.to_dict()
            
        except Exception as e:
            logger.error(f'Create permission error: {str(e)}')
            raise Exception(f'创建权限失败: {str(e)}')
    
    @staticmethod
    def update_permission(permission_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新权限"""
        try:
            permission = Permission.query.get(permission_id)
            
            if not permission:
                raise Exception('权限不存在')
            
            # 更新权限信息
            if 'name' in data:
                permission.name = data['name']
            
            if 'code' in data:
                # 检查权限代码是否已存在
                existing_permission = Permission.query.filter(
                    Permission.code == data['code'],
                    Permission.id != permission_id
                ).first()
                if existing_permission:
                    raise Exception('权限代码已存在')
                permission.code = data['code']
            
            if 'type' in data:
                permission.type = PermissionType(data['type'])
            
            if 'parent_id' in data:
                permission.parent_id = data['parent_id']
            
            if 'path' in data:
                permission.path = data['path']
            
            if 'icon' in data:
                permission.icon = data['icon']
            
            if 'sort_order' in data:
                permission.sort_order = data['sort_order']
            
            if 'status' in data:
                permission.status = PermissionStatus(data['status'])
            
            db.session.commit()
            
            return permission.to_dict()
            
        except Exception as e:
            logger.error(f'Update permission error: {str(e)}')
            raise Exception(f'更新权限失败: {str(e)}')
    
    @staticmethod
    def delete_permission(permission_id: int) -> None:
        """删除权限"""
        try:
            permission = Permission.query.get(permission_id)
            
            if not permission:
                raise Exception('权限不存在')
            
            # 检查是否有子权限
            child_permissions = Permission.query.filter_by(parent_id=permission_id).all()
            if child_permissions:
                raise Exception('存在子权限，无法删除')
            
            # 检查是否有角色关联
            role_permissions = RolePermission.query.filter_by(permission_id=permission_id).all()
            if role_permissions:
                raise Exception('存在角色关联，无法删除')
            
            db.session.delete(permission)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Delete permission error: {str(e)}')
            raise Exception(f'删除权限失败: {str(e)}')
    
    @staticmethod
    def get_role_permissions(role: str) -> List[Dict[str, Any]]:
        """获取角色权限"""
        try:
            role_permissions = RolePermission.query.filter_by(role=role).all()
            
            return [rp.to_dict() for rp in role_permissions]
            
        except Exception as e:
            logger.error(f'Get role permissions error: {str(e)}')
            raise Exception(f'获取角色权限失败: {str(e)}')
    
    @staticmethod
    def set_role_permissions(role: str, permission_ids: List[int]) -> None:
        """设置角色权限"""
        try:
            # 删除现有权限
            RolePermission.query.filter_by(role=role).delete()
            
            # 添加新权限
            for permission_id in permission_ids:
                role_permission = RolePermission(
                    role=role,
                    permission_id=permission_id
                )
                db.session.add(role_permission)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Set role permissions error: {str(e)}')
            raise Exception(f'设置角色权限失败: {str(e)}')
    
    @staticmethod
    def remove_role_permission(role: str, permission_id: int) -> None:
        """移除角色权限"""
        try:
            role_permission = RolePermission.query.filter_by(
                role=role, 
                permission_id=permission_id
            ).first()
            
            if role_permission:
                db.session.delete(role_permission)
                db.session.commit()
            
        except Exception as e:
            logger.error(f'Remove role permission error: {str(e)}')
            raise Exception(f'移除角色权限失败: {str(e)}')
    
    @staticmethod
    def get_user_permissions(user_id: int) -> List[Dict[str, Any]]:
        """获取用户权限"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                raise Exception('用户不存在')
            
            # 获取用户角色权限
            role_permissions = RolePermission.query.filter_by(role=user.role).all()
            
            return [rp.to_dict() for rp in role_permissions]
            
        except Exception as e:
            logger.error(f'Get user permissions error: {str(e)}')
            raise Exception(f'获取用户权限失败: {str(e)}')
    
    @staticmethod
    def check_user_permission(user_id: int, permission_code: str) -> bool:
        """检查用户权限"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                return False
            
            # 管理员拥有所有权限
            if user.role == 'admin':
                return True
            
            # 检查用户角色是否有该权限
            permission = Permission.query.filter_by(code=permission_code).first()
            if not permission:
                return False
            
            role_permission = RolePermission.query.filter_by(
                role=user.role,
                permission_id=permission.id
            ).first()
            
            return role_permission is not None
            
        except Exception as e:
            logger.error(f'Check user permission error: {str(e)}')
            return False
    
    @staticmethod
    def get_user_menu_permissions(user_id: int) -> List[Dict[str, Any]]:
        """获取用户菜单权限"""
        try:
            user = User.query.get(user_id)
            
            if not user:
                return []
            
            # 管理员拥有所有菜单权限
            if user.role == 'admin':
                permissions = Permission.query.filter(
                    Permission.type == PermissionType.MENU,
                    Permission.status == PermissionStatus.ACTIVE
                ).order_by(Permission.sort_order).all()
            else:
                # 获取用户角色权限
                role_permissions = RolePermission.query.filter_by(role=user.role).all()
                permission_ids = [rp.permission_id for rp in role_permissions]
                
                permissions = Permission.query.filter(
                    Permission.id.in_(permission_ids),
                    Permission.type == PermissionType.MENU,
                    Permission.status == PermissionStatus.ACTIVE
                ).order_by(Permission.sort_order).all()
            
            # 构建菜单树
            menu_dict = {}
            root_menus = []
            
            for permission in permissions:
                menu_dict[permission.id] = permission.to_tree_dict()
            
            for permission in permissions:
                if permission.parent_id == 0:
                    root_menus.append(menu_dict[permission.id])
                else:
                    parent = menu_dict.get(permission.parent_id)
                    if parent:
                        if 'children' not in parent:
                            parent['children'] = []
                        parent['children'].append(menu_dict[permission.id])
            
            return root_menus
            
        except Exception as e:
            logger.error(f'Get user menu permissions error: {str(e)}')
            return []
    
    @staticmethod
    def init_default_permissions() -> None:
        """初始化默认权限"""
        try:
            # 检查是否已初始化
            existing_permissions = Permission.query.count()
            if existing_permissions > 0:
                return
            
            # 默认权限数据
            default_permissions = [
                # 菜单权限
                {'name': '用户管理', 'code': 'user_management', 'type': 'menu', 'path': '/admin/users', 'icon': 'User', 'sort_order': 1},
                {'name': '科目管理', 'code': 'subject_management', 'type': 'menu', 'path': '/admin/subjects', 'icon': 'Book', 'sort_order': 2},
                {'name': '试题管理', 'code': 'question_management', 'type': 'menu', 'path': '/admin/questions', 'icon': 'QuestionFilled', 'sort_order': 3},
                {'name': '考试管理', 'code': 'exam_management', 'type': 'menu', 'path': '/admin/exams', 'icon': 'Document', 'sort_order': 4},
                {'name': '权限管理', 'code': 'permission_management', 'type': 'menu', 'path': '/admin/permissions', 'icon': 'Lock', 'sort_order': 5},
                {'name': '系统设置', 'code': 'system_settings', 'type': 'menu', 'path': '/admin/settings', 'icon': 'Setting', 'sort_order': 6},
                
                # 按钮权限
                {'name': '创建用户', 'code': 'user_create', 'type': 'button', 'parent_id': 1, 'sort_order': 1},
                {'name': '编辑用户', 'code': 'user_edit', 'type': 'button', 'parent_id': 1, 'sort_order': 2},
                {'name': '删除用户', 'code': 'user_delete', 'type': 'button', 'parent_id': 1, 'sort_order': 3},
                {'name': '创建科目', 'code': 'subject_create', 'type': 'button', 'parent_id': 2, 'sort_order': 1},
                {'name': '编辑科目', 'code': 'subject_edit', 'type': 'button', 'parent_id': 2, 'sort_order': 2},
                {'name': '删除科目', 'code': 'subject_delete', 'type': 'button', 'parent_id': 2, 'sort_order': 3},
                
                # API权限
                {'name': '用户API', 'code': 'user_api', 'type': 'api', 'path': '/api/users', 'sort_order': 1},
                {'name': '科目API', 'code': 'subject_api', 'type': 'api', 'path': '/api/subjects', 'sort_order': 2},
                {'name': '试题API', 'code': 'question_api', 'type': 'api', 'path': '/api/questions', 'sort_order': 3},
                {'name': '考试API', 'code': 'exam_api', 'type': 'api', 'path': '/api/exams', 'sort_order': 4},
            ]
            
            # 创建权限
            for perm_data in default_permissions:
                permission = Permission(
                    name=perm_data['name'],
                    code=perm_data['code'],
                    type=PermissionType(perm_data['type']),
                    parent_id=perm_data.get('parent_id', 0),
                    path=perm_data.get('path'),
                    icon=perm_data.get('icon'),
                    sort_order=perm_data.get('sort_order', 0)
                )
                db.session.add(permission)
            
            db.session.commit()
            
            # 设置管理员权限
            admin_permissions = Permission.query.all()
            for permission in admin_permissions:
                role_permission = RolePermission(
                    role='admin',
                    permission_id=permission.id
                )
                db.session.add(role_permission)
            
            # 设置普通用户权限
            user_permissions = Permission.query.filter(
                Permission.code.in_(['subject_management', 'question_management', 'exam_management'])
            ).all()
            for permission in user_permissions:
                role_permission = RolePermission(
                    role='user',
                    permission_id=permission.id
                )
                db.session.add(role_permission)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Init default permissions error: {str(e)}')
            raise Exception(f'初始化默认权限失败: {str(e)}')
