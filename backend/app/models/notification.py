from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

class NotificationType(enum.Enum):
    """通知类型枚举"""
    SYSTEM = 'system'  # 系统通知
    EXAM = 'exam'      # 考试通知
    SCORE = 'score'    # 成绩通知
    ANNOUNCEMENT = 'announcement'  # 公告通知

class Notification(db.Model):
    """通知模型"""
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='用户ID')
    title = Column(String(200), nullable=False, comment='通知标题')
    content = Column(Text, comment='通知内容')
    type = Column(Enum(NotificationType), nullable=False, default=NotificationType.SYSTEM, comment='通知类型')
    is_read = Column(Boolean, default=False, comment='是否已读')
    read_at = Column(DateTime, comment='阅读时间')
    related_id = Column(Integer, comment='关联记录ID')
    related_type = Column(String(50), comment='关联记录类型')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    user = relationship('User', backref='notifications')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'type': self.type.value if self.type else None,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'related_id': self.related_id,
            'related_type': self.related_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def mark_as_read(self):
        """标记为已读"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Notification {self.id}: {self.title}>'
