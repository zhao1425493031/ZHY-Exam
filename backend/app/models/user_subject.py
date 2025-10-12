from datetime import datetime
from app.models import BaseModel
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

class UserSubject(BaseModel):
    """用户科目关联模型"""
    __tablename__ = 'user_subjects'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False, index=True)
    is_free = Column(Boolean, default=True, comment='是否免费订阅')
    purchased_at = Column(DateTime, comment='购买时间（付费课程）')
    expires_at = Column(DateTime, comment='到期时间（付费课程）')
    status = Column(Enum('active', 'expired', 'cancelled', name='user_subject_status'), 
                   default='active', comment='订阅状态')

    # 关系
    user = relationship('User', backref='user_subjects')
    subject = relationship('Subject', backref='user_subjects')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subject_id': self.subject_id,
            'is_free': self.is_free,
            'purchased_at': self.purchased_at.isoformat() if self.purchased_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @classmethod
    def is_user_subscribed(cls, user_id, subject_id):
        """检查用户是否已订阅科目"""
        return cls.query.filter_by(
            user_id=user_id,
            subject_id=subject_id,
            status='active'
        ).first() is not None

    @classmethod
    def get_user_subjects(cls, user_id):
        """获取用户订阅的所有科目"""
        return cls.query.filter_by(
            user_id=user_id,
            status='active'
        ).all()

    @classmethod
    def subscribe_subject(cls, user_id, subject_id, is_free=True):
        """用户订阅科目"""
        # 检查是否已订阅
        existing = cls.query.filter_by(
            user_id=user_id,
            subject_id=subject_id
        ).first()
        
        if existing:
            if existing.status == 'active':
                return existing, 'already_subscribed'
            else:
                # 重新激活订阅
                existing.status = 'active'
                existing.updated_at = datetime.utcnow()
                return existing, 'reactivated'
        else:
            # 创建新订阅
            user_subject = cls(
                user_id=user_id,
                subject_id=subject_id,
                is_free=is_free,
                purchased_at=datetime.utcnow() if not is_free else None
            )
            return user_subject, 'new_subscription'

    @classmethod
    def unsubscribe_subject(cls, user_id, subject_id):
        """用户取消订阅科目"""
        user_subject = cls.query.filter_by(
            user_id=user_id,
            subject_id=subject_id
        ).first()
        
        if user_subject:
            user_subject.status = 'cancelled'
            user_subject.updated_at = datetime.utcnow()
            return user_subject, 'unsubscribed'
        
        return None, 'not_found'
