from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

class PermissionType(enum.Enum):
    """权限类型枚举"""
    MENU = 'menu'        # 菜单权限
    BUTTON = 'button'    # 按钮权限
    API = 'api'          # API权限
    DATA = 'data'        # 数据权限

class PermissionStatus(enum.Enum):
    """权限状态枚举"""
    ACTIVE = 'active'      # 启用
    INACTIVE = 'inactive'  # 禁用

class Permission(db.Model):
    """权限模型"""
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, comment='权限名称')
    code = Column(String(100), unique=True, nullable=False, comment='权限代码')
    type = Column(Enum(PermissionType), nullable=False, comment='权限类型')
    parent_id = Column(Integer, ForeignKey('permissions.id'), default=0, comment='父权限ID')
    path = Column(String(200), comment='路径')
    icon = Column(String(100), comment='图标')
    sort_order = Column(Integer, default=0, comment='排序')
    status = Column(Enum(PermissionStatus), nullable=False, default=PermissionStatus.ACTIVE, comment='状态')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    parent = relationship('Permission', remote_side=[id], backref='children')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'type': self.type.value if self.type else None,
            'parent_id': self.parent_id,
            'path': self.path,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'status': self.status.value if self.status else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'children': [child.to_dict() for child in self.children] if self.children else []
        }
    
    def to_tree_dict(self):
        """转换为树形结构字典"""
        return {
            'id': self.id,
            'label': self.name,
            'value': self.id,
            'code': self.code,
            'type': self.type.value if self.type else None,
            'parent_id': self.parent_id,
            'path': self.path,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'status': self.status.value if self.status else None,
            'children': [child.to_tree_dict() for child in self.children] if self.children else []
        }
    
    def is_active(self):
        """检查是否启用"""
        return self.status == PermissionStatus.ACTIVE
    
    def get_type_label(self):
        """获取类型标签"""
        labels = {
            PermissionType.MENU: '菜单权限',
            PermissionType.BUTTON: '按钮权限',
            PermissionType.API: 'API权限',
            PermissionType.DATA: '数据权限'
        }
        return labels.get(self.type, '未知类型')
    
    def get_status_label(self):
        """获取状态标签"""
        labels = {
            PermissionStatus.ACTIVE: '启用',
            PermissionStatus.INACTIVE: '禁用'
        }
        return labels.get(self.status, '未知状态')
    
    def __repr__(self):
        return f'<Permission {self.id}: {self.name}>'
