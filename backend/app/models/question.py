# 试题模型
from app.models import BaseModel, db
from sqlalchemy import Column, String, Text, Enum, Integer, JSON

class Question(BaseModel):
    """试题模型"""
    __tablename__ = 'questions'
    
    subject_id = Column(Integer, nullable=False, index=True)  # 科目ID，不设置外键
    type = Column(Enum('single', 'multiple', 'judge', 'fill', 'essay', name='question_type'), 
                  nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text)
    options = Column(JSON)  # 选项，JSON格式存储
    answer = Column(Text, nullable=False)
    explanation = Column(Text)
    difficulty = Column(Enum('easy', 'medium', 'hard', name='question_difficulty'), 
                        default='medium')
    tags = Column(JSON)  # 标签，JSON格式存储
    points = Column(Integer, default=1)
    status = Column(Enum('draft', 'published', 'archived', name='question_status'), 
                    default='draft')
    created_by = Column(Integer, nullable=False, index=True)  # 用户ID，不设置外键
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'options': self.options,
            'answer': self.answer,
            'explanation': self.explanation,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'points': self.points,
            'status': self.status,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Question {self.title[:50]}...>'
