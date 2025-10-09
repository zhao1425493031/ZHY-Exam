# 基础模型类
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

db = SQLAlchemy()

class BaseModel(db.Model):
    """基础模型类"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def save(self):
        """保存到数据库"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """从数据库删除"""
        db.session.delete(self)
        db.session.commit()
        return True
    
    @classmethod
    def get_by_id(cls, id):
        """根据ID获取记录"""
        return cls.query.get(id)
    
    @classmethod
    def get_all(cls, page=1, per_page=10, **filters):
        """获取所有记录"""
        query = cls.query
        for key, value in filters.items():
            if hasattr(cls, key) and value is not None:
                query = query.filter(getattr(cls, key) == value)
        return query.paginate(page=page, per_page=per_page, error_out=False)
