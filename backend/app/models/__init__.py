# 基础模型类
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

# 导入db实例（从app包中导入，避免循环导入）
from app import db

class BaseModel(db.Model):
    """基础模型类"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# 导入所有模型
from .user import User
from .subject import Subject
from .question import Question
from .exam import Exam
from .exam_record import ExamRecord
from .notification import Notification
from .user_favorite import UserFavorite
from .wrong_answer import WrongAnswer
from .file import File
from .announcement import Announcement
from .system_config import SystemConfig
from .permission import Permission
from .role_permission import RolePermission
from .payment_order import PaymentOrder
from .user_purchase import UserPurchase
from .import_record import ImportRecord
from .log_config import LogConfig
from .exam_monitoring import ExamMonitoring
from .user_subject import UserSubject
from .user_setting import UserSetting
from .user_favorite import UserFavorite
