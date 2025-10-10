from datetime import datetime
from app.models import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class ExamMonitoring(BaseModel):
    """考试监控模型"""
    __tablename__ = 'exam_monitoring'

    exam_record_id = Column(Integer, ForeignKey('exam_records.id'), nullable=False, index=True)
    event_type = Column(Enum('start', 'pause', 'resume', 'submit', 'timeout', 'cheat', 
                             'switch_tab', 'answer_time', 'ip_change', name='monitoring_event_type'),
                        nullable=False)
    event_data = Column(JSON)  # 事件数据，JSON格式存储
    ip_address = Column(String(45))  # IP地址
    user_agent = Column(Text)  # 用户代理
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关系
    exam_record = relationship('ExamRecord', backref='monitoring_events')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'exam_record_id': self.exam_record_id,
            'event_type': self.event_type,
            'event_data': self.event_data,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
