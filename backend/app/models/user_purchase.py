# 用户购买记录模型
from app.models import BaseModel, db
from sqlalchemy import Column, String, Enum, Integer, DECIMAL, DateTime

class UserPurchase(BaseModel):
    """用户购买记录模型"""
    __tablename__ = 'user_purchases'
    
    user_id = Column(Integer, nullable=False, index=True)  # 用户ID，不设置外键
    subject_id = Column(Integer, nullable=False, index=True)  # 科目ID，不设置外键
    order_id = Column(String(50), unique=True, nullable=False, comment='订单号')
    payment_method = Column(Enum('alipay', 'wechat', 'paypal', 'admin', name='payment_method'), 
                           nullable=False, comment='支付方式')
    amount = Column(DECIMAL(10, 2), nullable=False, comment='支付金额')
    original_amount = Column(DECIMAL(10, 2), nullable=False, comment='原价')
    discount_amount = Column(DECIMAL(10, 2), default=0.00, comment='优惠金额')
    status = Column(Enum('pending', 'paid', 'cancelled', 'refunded', name='purchase_status'), 
                    default='pending', comment='支付状态')
    payment_time = Column(DateTime, comment='支付时间')
    expire_time = Column(DateTime, comment='到期时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subject_id': self.subject_id,
            'order_id': self.order_id,
            'payment_method': self.payment_method,
            'amount': float(self.amount) if self.amount else 0.00,
            'original_amount': float(self.original_amount) if self.original_amount else 0.00,
            'discount_amount': float(self.discount_amount) if self.discount_amount else 0.00,
            'status': self.status,
            'payment_time': self.payment_time.isoformat() if self.payment_time else None,
            'expire_time': self.expire_time.isoformat() if self.expire_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<UserPurchase User:{self.user_id} Subject:{self.subject_id}>'
