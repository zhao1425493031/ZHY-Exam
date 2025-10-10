from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

class RolePermission(db.Model):
    """角色权限关联模型"""
    __tablename__ = 'role_permissions'
    
    id = Column(Integer, primary_key=True)
    role = Column(String(50), nullable=False, comment='角色')
    permission_id = Column(Integer, ForeignKey('permissions.id'), nullable=False, comment='权限ID')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    
    # 关系
    permission = relationship('Permission', backref='role_permissions')
    
    # 唯一约束
    __table_args__ = (
        UniqueConstraint('role', 'permission_id', name='unique_role_permission'),
    )
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'role': self.role,
            'permission_id': self.permission_id,
            'permission_name': self.permission.name if self.permission else '',
            'permission_code': self.permission.code if self.permission else '',
            'permission_type': self.permission.type.value if self.permission and self.permission.type else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<RolePermission {self.role}: {self.permission_id}>'
