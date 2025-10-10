from datetime import datetime
from app import db
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
import os

class File(db.Model):
    """文件模型"""
    __tablename__ = 'files'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False, comment='文件名')
    original_name = Column(String(255), nullable=False, comment='原始文件名')
    file_path = Column(String(500), nullable=False, comment='文件路径')
    file_size = Column(BigInteger, nullable=False, comment='文件大小（字节）')
    file_type = Column(String(100), comment='文件类型')
    uploader_id = Column(Integer, ForeignKey('users.id'), nullable=False, comment='上传者ID')
    related_type = Column(String(50), comment='关联类型（question, user, exam等）')
    related_id = Column(Integer, comment='关联记录ID')
    description = Column(Text, comment='文件描述')
    is_public = Column(db.Boolean, default=False, comment='是否公开')
    download_count = Column(Integer, default=0, comment='下载次数')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关系
    uploader = relationship('User', backref='uploaded_files')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_name': self.original_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_size_formatted': self.format_file_size(),
            'file_type': self.file_type,
            'uploader_id': self.uploader_id,
            'uploader_name': self.uploader.username if self.uploader else '',
            'related_type': self.related_type,
            'related_id': self.related_id,
            'description': self.description,
            'is_public': self.is_public,
            'download_count': self.download_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def format_file_size(self):
        """格式化文件大小"""
        size = self.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
    
    def get_file_extension(self):
        """获取文件扩展名"""
        return os.path.splitext(self.original_name)[1].lower()
    
    def is_image(self):
        """判断是否为图片文件"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']
        return self.get_file_extension() in image_extensions
    
    def is_document(self):
        """判断是否为文档文件"""
        doc_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']
        return self.get_file_extension() in doc_extensions
    
    def is_video(self):
        """判断是否为视频文件"""
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
        return self.get_file_extension() in video_extensions
    
    def is_audio(self):
        """判断是否为音频文件"""
        audio_extensions = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma']
        return self.get_file_extension() in audio_extensions
    
    def increment_download_count(self):
        """增加下载次数"""
        self.download_count += 1
        db.session.commit()
    
    def delete_file(self):
        """删除文件"""
        try:
            # 删除物理文件
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
            
            # 删除数据库记录
            db.session.delete(self)
            db.session.commit()
            
            return True
        except Exception as e:
            db.session.rollback()
            raise Exception(f'删除文件失败: {str(e)}')
    
    def __repr__(self):
        return f'<File {self.id}: {self.original_name}>'
