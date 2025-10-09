# 用户模型
from app.models import BaseModel, db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String, Enum, Boolean, Text

class User(BaseModel):
    """用户模型"""
    __tablename__ = 'users'
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    real_name = Column(String(50))
    role = Column(Enum('admin', 'user', name='user_role'), 
                  default='user', nullable=False)
    status = Column(Enum('active', 'inactive', 'banned', name='user_status'), 
                    default='active', nullable=False)
    avatar_url = Column(String(255))
    phone = Column(String(20))
    
    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'real_name': self.real_name,
            'role': self.role,
            'status': self.status,
            'avatar_url': self.avatar_url,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_sensitive:
            data['password_hash'] = self.password_hash
            
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'
