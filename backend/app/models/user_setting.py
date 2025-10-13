from app import db
from datetime import datetime
from sqlalchemy import JSON

class UserSetting(db.Model):
    """用户设置模型"""
    __tablename__ = 'user_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # 通知设置
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)
    system_notifications = db.Column(db.Boolean, default=True, nullable=False)
    exam_notifications = db.Column(db.Boolean, default=True, nullable=False)
    score_notifications = db.Column(db.Boolean, default=True, nullable=False)
    announcement_notifications = db.Column(db.Boolean, default=True, nullable=False)
    
    # 其他设置
    theme = db.Column(db.String(20), default='light', nullable=False)
    language = db.Column(db.String(10), default='zh', nullable=False)
    timezone = db.Column(db.String(50), default='Asia/Shanghai', nullable=False)
    
    # 扩展设置（JSON格式）
    extra_settings = db.Column(JSON, default={})
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # 关系（不使用外键）
    # user = db.relationship('User', backref=db.backref('settings', uselist=False))
    
    def __repr__(self):
        return f'<UserSetting {self.user_id}>'
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'email_notifications': self.email_notifications,
            'system_notifications': self.system_notifications,
            'exam_notifications': self.exam_notifications,
            'score_notifications': self.score_notifications,
            'announcement_notifications': self.announcement_notifications,
            'theme': self.theme,
            'language': self.language,
            'timezone': self.timezone,
            'extra_settings': self.extra_settings or {},
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def get_or_create_settings(user_id: int):
        """获取或创建用户设置"""
        settings = UserSetting.query.filter_by(user_id=user_id).first()
        if not settings:
            settings = UserSetting(user_id=user_id)
            db.session.add(settings)
            db.session.commit()
        return settings
    
    @staticmethod
    def update_notification_settings(user_id: int, settings_data: dict):
        """更新用户通知设置"""
        settings = UserSetting.get_or_create_settings(user_id)
        
        # 更新通知设置
        if 'email_notifications' in settings_data:
            settings.email_notifications = bool(settings_data['email_notifications'])
        if 'system_notifications' in settings_data:
            settings.system_notifications = bool(settings_data['system_notifications'])
        if 'exam_notifications' in settings_data:
            settings.exam_notifications = bool(settings_data['exam_notifications'])
        if 'score_notifications' in settings_data:
            settings.score_notifications = bool(settings_data['score_notifications'])
        if 'announcement_notifications' in settings_data:
            settings.announcement_notifications = bool(settings_data['announcement_notifications'])
        
        # 更新其他设置
        if 'theme' in settings_data:
            settings.theme = settings_data['theme']
        if 'language' in settings_data:
            settings.language = settings_data['language']
        if 'timezone' in settings_data:
            settings.timezone = settings_data['timezone']
        
        # 更新扩展设置
        if 'extra_settings' in settings_data:
            extra_settings = settings.extra_settings or {}
            extra_settings.update(settings_data['extra_settings'])
            settings.extra_settings = extra_settings
        
        db.session.commit()
        return settings
    
    @staticmethod
    def get_notification_settings(user_id: int):
        """获取用户通知设置"""
        settings = UserSetting.get_or_create_settings(user_id)
        return {
            'email_notifications': settings.email_notifications,
            'system_notifications': settings.system_notifications,
            'exam_notifications': settings.exam_notifications,
            'score_notifications': settings.score_notifications,
            'announcement_notifications': settings.announcement_notifications
        }
