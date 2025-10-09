# 支付订单模型
from app.models import BaseModel, db
from sqlalchemy import Column, String, Enum, Integer, DECIMAL, DateTime, JSON

class PaymentOrder(BaseModel):
    """支付订单模型"""
    __tablename__ = 'payment_orders'
    
    order_id = Column(String(50), unique=True, nullable=False, comment='订单号')
    user_id = Column(Integer, nullable=False, index=True)  # 用户ID，不设置外键
    subject_id = Column(Integer, nullable=False, index=True)  # 科目ID，不设置外键
    payment_method = Column(Enum('alipay', 'wechat', 'paypal', 'admin', name='payment_method'), 
                           nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(10), default='CNY', comment='货币类型')
    status = Column(Enum('pending', 'paid', 'cancelled', 'refunded', 'failed', name='order_status'), 
                    default='pending')
    third_party_order_id = Column(String(100), comment='第三方支付订单号')
    payment_url = Column(String(500), comment='支付链接')
    callback_data = Column(JSON, comment='支付回调数据')
    paid_at = Column(DateTime, comment='支付完成时间')
    expired_at = Column(DateTime, comment='订单过期时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'subject_id': self.subject_id,
            'payment_method': self.payment_method,
            'amount': float(self.amount) if self.amount else 0.00,
            'currency': self.currency,
            'status': self.status,
            'third_party_order_id': self.third_party_order_id,
            'payment_url': self.payment_url,
            'callback_data': self.callback_data,
            'paid_at': self.paid_at.isoformat() if self.paid_at else None,
            'expired_at': self.expired_at.isoformat() if self.expired_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<PaymentOrder {self.order_id}>'
