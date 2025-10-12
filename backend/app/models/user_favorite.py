from datetime import datetime
from app import db

class UserFavorite(db.Model):
    """用户收藏表"""
    __tablename__ = 'user_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, comment='用户ID')
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, comment='题目ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='收藏时间')
    
    # 关系
    user = db.relationship('User', backref='favorites')
    question = db.relationship('Question', backref='favorited_by')
    
    # 唯一约束：一个用户只能收藏一个题目一次
    __table_args__ = (
        db.UniqueConstraint('user_id', 'question_id', name='unique_user_question_favorite'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<UserFavorite {self.user_id}-{self.question_id}>'
