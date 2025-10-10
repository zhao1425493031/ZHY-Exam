from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

class AnnouncementType(enum.Enum):
    """公告类型枚举"""
    SYSTEM = 'system'      # 系统公告
    EXAM = 'exam'          # 考试公告
    MAINTENANCE = 'maintenance'  # 维护公告

class AnnouncementPriority(enum.Enum):
    """公告优先级枚举"""
    LOW = 'low'        # 低优先级
    MEDIUM = 'medium'  # 中优先级
    HIGH = 'high'      # 高优先级

class AnnouncementStatus(enum.Enum):
    """公告状态枚举"""
    DRAFT = 'draft'         # 草稿
    PUBLISHED = 'published' # 已发布
    ARCHIVED = 'archived'   # 已归档

class Announcement(db.Model):
    """公告模型"""
    __tablename__ = 'announcements'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False, comment='公告标题')
    content = Column(Text, nullable=False, comment='公告内容')
    type = Column(Enum(AnnouncementType), nullable=False, default=AnnouncementType.SYSTEM, comment='公告类型')
    priority = Column(Enum(AnnouncementPriority), nullable=False, default=AnnouncementPriority.MEDIUM, comment='优先级')
    status = Column(Enum(AnnouncementStatus), nullable=False, default=AnnouncementStatus.DRAFT, comment='状态')
    publish_time = Column(DateTime, comment='发布时间')
    expire_time = Column(DateTime, comment='过期时间')
    view_count = Column(Integer, default=0, comment='查看次数')
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False, comment='创建者ID')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    creator = relationship('User', backref='created_announcements')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'type': self.type.value if self.type else None,
            'priority': self.priority.value if self.priority else None,
            'status': self.status.value if self.status else None,
            'publish_time': self.publish_time.isoformat() if self.publish_time else None,
            'expire_time': self.expire_time.isoformat() if self.expire_time else None,
            'view_count': self.view_count,
            'created_by': self.created_by,
            'creator_name': self.creator.username if self.creator else '',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_expired': self.is_expired(),
            'is_published': self.status == AnnouncementStatus.PUBLISHED
        }
    
    def is_expired(self):
        """检查是否过期"""
        if not self.expire_time:
            return False
        return datetime.utcnow() > self.expire_time
    
    def is_published(self):
        """检查是否已发布"""
        return self.status == AnnouncementStatus.PUBLISHED
    
    def is_active(self):
        """检查是否有效（已发布且未过期）"""
        return self.is_published() and not self.is_expired()
    
    def publish(self):
        """发布公告"""
        self.status = AnnouncementStatus.PUBLISHED
        self.publish_time = datetime.utcnow()
        db.session.commit()
    
    def unpublish(self):
        """取消发布公告"""
        self.status = AnnouncementStatus.DRAFT
        db.session.commit()
    
    def archive(self):
        """归档公告"""
        self.status = AnnouncementStatus.ARCHIVED
        db.session.commit()
    
    def increment_view_count(self):
        """增加查看次数"""
        self.view_count += 1
        db.session.commit()
    
    def get_priority_color(self):
        """获取优先级颜色"""
        colors = {
            AnnouncementPriority.LOW: 'success',
            AnnouncementPriority.MEDIUM: 'warning',
            AnnouncementPriority.HIGH: 'danger'
        }
        return colors.get(self.priority, 'default')
    
    def get_type_label(self):
        """获取类型标签"""
        labels = {
            AnnouncementType.SYSTEM: '系统公告',
            AnnouncementType.EXAM: '考试公告',
            AnnouncementType.MAINTENANCE: '维护公告'
        }
        return labels.get(self.type, '未知类型')
    
    def get_status_label(self):
        """获取状态标签"""
        labels = {
            AnnouncementStatus.DRAFT: '草稿',
            AnnouncementStatus.PUBLISHED: '已发布',
            AnnouncementStatus.ARCHIVED: '已归档'
        }
        return labels.get(self.status, '未知状态')
    
    def __repr__(self):
        return f'<Announcement {self.id}: {self.title}>'
