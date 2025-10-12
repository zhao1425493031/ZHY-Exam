# 考试记录模型
from app.models import BaseModel, db
from sqlalchemy import Column, Enum, Integer, JSON, DateTime, DECIMAL

class ExamRecord(BaseModel):
    """考试记录模型"""
    __tablename__ = 'exam_records'
    
    exam_id = Column(Integer, nullable=False, index=True)  # 考试ID，不设置外键
    user_id = Column(Integer, nullable=False, index=True)  # 用户ID，不设置外键
    start_time = Column(DateTime)
    submit_time = Column(DateTime)
    answers = Column(JSON)  # 用户答案
    score = Column(DECIMAL(5, 2))
    correct_count = Column(Integer, default=0)  # 正确题数
    total_count = Column(Integer, default=0)  # 总题数
    status = Column(Enum('in_progress', 'submitted', 'timeout', 'cancelled', 
                         name='exam_record_status'), default='in_progress')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'exam_id': self.exam_id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'submit_time': self.submit_time.isoformat() if self.submit_time else None,
            'answers': self.answers,
            'score': float(self.score) if self.score else None,
            'correct_count': self.correct_count,
            'total_count': self.total_count,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<ExamRecord {self.user_id}-{self.exam_id}>'
