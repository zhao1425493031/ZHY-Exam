from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, Text, DateTime

class ImportRecord(db.Model):
    """导入记录模型"""
    __tablename__ = 'import_records'
    
    id = Column(Integer, primary_key=True)
    import_type = Column(String(50), nullable=False, comment='导入类型')
    total_count = Column(Integer, nullable=False, comment='总数量')
    success_count = Column(Integer, nullable=False, comment='成功数量')
    error_count = Column(Integer, nullable=False, comment='错误数量')
    error_details = Column(Text, comment='错误详情')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'import_type': self.import_type,
            'total_count': self.total_count,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'error_details': self.error_details,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'success_rate': round((self.success_count / self.total_count * 100), 2) if self.total_count > 0 else 0
        }
    
    def get_type_label(self):
        """获取类型标签"""
        labels = {
            'users': '用户导入',
            'subjects': '科目导入',
            'questions': '试题导入'
        }
        return labels.get(self.import_type, self.import_type)
    
    def __repr__(self):
        return f'<ImportRecord {self.id}: {self.import_type}>'
