# 考试模型
from app.models import BaseModel, db
from sqlalchemy import Column, String, Text, Enum, Integer, JSON, DateTime

class Exam(BaseModel):
    """考试模型"""
    __tablename__ = 'exams'
    
    title = Column(String(200), nullable=False)
    subject_id = Column(Integer, nullable=False, index=True)  # 科目ID，不设置外键
    description = Column(Text)
    duration = Column(Integer, nullable=False)  # 考试时长(分钟)
    total_points = Column(Integer, nullable=False)
    passing_score = Column(Integer)  # 合格分数
    question_count = Column(Integer, nullable=False)
    question_ids = Column(JSON, nullable=False)  # 试题ID列表
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Enum('draft', 'published', 'ongoing', 'finished', 'cancelled', 
                         name='exam_status'), default='draft')
    settings = Column(JSON)  # 考试设置
    created_by = Column(Integer, nullable=False, index=True)  # 用户ID，不设置外键
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'subject_id': self.subject_id,
            'description': self.description,
            'duration': self.duration,
            'total_points': self.total_points,
            'passing_score': self.passing_score,
            'question_count': self.question_count,
            'question_ids': self.question_ids,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'settings': self.settings,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Exam {self.title}>'
