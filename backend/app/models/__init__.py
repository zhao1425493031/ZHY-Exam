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
