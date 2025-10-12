# 科目模型
from app.models import BaseModel, db
from sqlalchemy import Column, String, Text, Enum, Integer, Boolean, DECIMAL

class Subject(BaseModel):
    """科目模型"""
    __tablename__ = 'subjects'
    
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False, index=True)
    description = Column(Text)
    category = Column(String(50))
    status = Column(Enum('active', 'inactive', name='subject_status'), 
                    default='active', nullable=False)
    is_free = Column(Boolean, default=True, nullable=False, comment='是否免费')
    price = Column(DECIMAL(10, 2), default=0.00, nullable=False, comment='价格（元）')
    original_price = Column(DECIMAL(10, 2), default=0.00, nullable=False, comment='原价（元）')
    discount_rate = Column(DECIMAL(5, 2), default=100.00, nullable=False, comment='折扣率（%）')
    cover_image = Column(String(500), comment='课程封面图片URL')
    created_by = Column(Integer, nullable=False, index=True)  # 用户ID，不设置外键
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'category': self.category,
            'status': self.status,
            'is_free': self.is_free,
            'price': float(self.price) if self.price else 0.00,
            'original_price': float(self.original_price) if self.original_price else 0.00,
            'discount_rate': float(self.discount_rate) if self.discount_rate else 100.00,
            'cover_image': self.cover_image,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Subject {self.name}>'
