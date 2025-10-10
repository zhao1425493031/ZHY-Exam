from datetime import datetime
from app.models import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class WrongAnswer(BaseModel):
    """错题记录模型"""
    __tablename__ = 'wrong_answers'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False, index=True)
    exam_record_id = Column(Integer, ForeignKey('exam_records.id'), nullable=True, index=True)
    user_answer = Column(Text)  # 用户答案
    correct_answer = Column(Text)  # 正确答案
    is_reviewed = Column(Boolean, default=False)  # 是否已复习
    reviewed_at = Column(DateTime)  # 复习时间
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 关系
    user = relationship('User', backref='wrong_answers')
    question = relationship('Question', backref='wrong_answers')
    exam_record = relationship('ExamRecord', backref='wrong_answers')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'exam_record_id': self.exam_record_id,
            'user_answer': self.user_answer,
            'correct_answer': self.correct_answer,
            'is_reviewed': self.is_reviewed,
            'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
