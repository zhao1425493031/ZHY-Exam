"""
系统配置模型
"""
from datetime import datetime
from app import db


class SystemConfig(db.Model):
    """系统配置模型"""
    __tablename__ = 'system_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(100), unique=True, nullable=False, comment='配置键')
    config_value = db.Column(db.Text, comment='配置值')
    config_type = db.Column(db.Enum('string', 'number', 'boolean', 'json'), default='string', comment='配置类型')
    description = db.Column(db.Text, comment='配置描述')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'config_type': self.config_type,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<SystemConfig {self.config_key}>'
