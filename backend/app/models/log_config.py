"""
日志配置模型
"""
from datetime import datetime
from app import db


class LogConfig(db.Model):
    """日志配置模型"""
    __tablename__ = 'log_configs'
    
    id = db.Column(db.Integer, primary_key=True)
    config_key = db.Column(db.String(100), unique=True, nullable=False, comment='配置键')
    config_value = db.Column(db.Text, nullable=False, comment='配置值')
    description = db.Column(db.Text, comment='配置描述')
    is_active = db.Column(db.Boolean, default=True, comment='是否启用')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'config_key': self.config_key,
            'config_value': self.config_value,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<LogConfig {self.config_key}>'


class SystemLog(db.Model):
    """系统日志模型"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    log_level = db.Column(db.Enum('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), nullable=False, comment='日志级别')
    module = db.Column(db.String(100), nullable=False, comment='模块名称')
    message = db.Column(db.Text, nullable=False, comment='日志消息')
    user_id = db.Column(db.Integer, comment='操作用户ID')
    ip_address = db.Column(db.String(45), comment='IP地址')
    user_agent = db.Column(db.Text, comment='用户代理')
    request_data = db.Column(db.JSON, comment='请求数据')
    response_data = db.Column(db.JSON, comment='响应数据')
    execution_time = db.Column(db.Numeric(10, 3), comment='执行时间(秒)')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'log_level': self.log_level,
            'module': self.module,
            'message': self.message,
            'user_id': self.user_id,
            'user_name': None,  # 延迟加载用户名
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'request_data': self.request_data,
            'response_data': self.response_data,
            'execution_time': float(self.execution_time) if self.execution_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<SystemLog {self.log_level}:{self.module}>'
