from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON

class ImportRecord(db.Model):
    """导入记录模型"""
    __tablename__ = 'import_records'
    
    id = Column(Integer, primary_key=True)
    import_type = Column(Enum('users', 'questions', 'subjects', name='import_type_enum'), nullable=False, comment='导入类型')
    filename = Column(String(255), nullable=False, comment='文件名')
    file_path = Column(String(500), nullable=False, comment='文件路径')
    total_count = Column(Integer, default=0, comment='总记录数')
    success_count = Column(Integer, default=0, comment='成功记录数')
    failed_count = Column(Integer, default=0, comment='失败记录数')
    error_details = Column(JSON, comment='错误详情（JSON格式）')
    status = Column(Enum('pending', 'processing', 'completed', 'failed', name='import_status_enum'), default='pending', comment='状态')
    imported_by = Column(Integer, comment='导入者ID')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'import_type': self.import_type,
            'filename': self.filename,
            'file_path': self.file_path,
            'total_count': self.total_count,
            'success_count': self.success_count,
            'failed_count': self.failed_count,
            'error_details': self.error_details,
            'status': self.status,
            'imported_by': self.imported_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
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
