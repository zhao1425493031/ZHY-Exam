from app import db
from datetime import datetime
from typing import Dict, Any

class UserFavorite(db.Model):
    __tablename__ = 'user_favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # 添加唯一约束
    __table_args__ = (db.UniqueConstraint('user_id', 'question_id', name='unique_user_question'),)

    def __repr__(self):
        return f'<UserFavorite {self.user_id}-{self.question_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }