from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from werkzeug.utils import secure_filename
from app.models.user import User
from app.models.file import File
from app import db
import os
import uuid
import mimetypes
import logging

logger = logging.getLogger(__name__)

class FileService:
    """文件服务"""
    
    # 允许的文件类型
    ALLOWED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
        'document': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt'],
        'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'],
        'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
        'archive': ['.zip', '.rar', '.7z', '.tar', '.gz']
    }
    
    # 最大文件大小（字节）
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
    
    @staticmethod
    def upload_file(file, user_id: int, related_type: str = 'general', 
                   related_id: Optional[int] = None) -> Dict[str, Any]:
        """上传文件"""
        try:
            # 验证文件
            if not file or not file.filename:
                raise Exception('没有选择文件')
            
            # 验证文件大小
            file.seek(0, 2)  # 移动到文件末尾
            file_size = file.tell()
            file.seek(0)  # 重置到文件开头
            
            if file_size > FileService.MAX_FILE_SIZE:
                raise Exception(f'文件大小超过限制（最大{FileService.MAX_FILE_SIZE // (1024*1024)}MB）')
            
            # 验证文件类型
            original_filename = secure_filename(file.filename)
            file_extension = os.path.splitext(original_filename)[1].lower()
            
            if not FileService._is_allowed_file_type(file_extension):
                raise Exception(f'不支持的文件类型: {file_extension}')
            
            # 生成唯一文件名
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            
            # 创建上传目录
            upload_dir = os.path.join('uploads', related_type)
            os.makedirs(upload_dir, exist_ok=True)
            
            # 保存文件
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)
            
            # 获取文件类型
            file_type, _ = mimetypes.guess_type(file_path)
            if not file_type:
                file_type = 'application/octet-stream'
            
            # 保存文件信息到数据库
            file_record = File(
                filename=unique_filename,
                original_name=original_filename,
                file_path=file_path,
                file_size=file_size,
                file_type=file_type,
                uploader_id=user_id,
                related_type=related_type,
                related_id=related_id
            )
            
            db.session.add(file_record)
            db.session.commit()
            
            return file_record.to_dict()
            
        except Exception as e:
            logger.error(f'Upload file error: {str(e)}')
            raise Exception(f'上传文件失败: {str(e)}')
    
    @staticmethod
    def batch_upload_files(files: List, user_id: int, related_type: str = 'general',
                          related_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """批量上传文件"""
        try:
            uploaded_files = []
            
            for file in files:
                try:
                    uploaded_file = FileService.upload_file(
                        file, user_id, related_type, related_id
                    )
                    uploaded_files.append(uploaded_file)
                except Exception as e:
                    logger.error(f'Upload file {file.filename} error: {str(e)}')
                    # 继续上传其他文件
                    continue
            
            return uploaded_files
            
        except Exception as e:
            logger.error(f'Batch upload files error: {str(e)}')
            raise Exception(f'批量上传文件失败: {str(e)}')
    
    @staticmethod
    def get_file(file_id: int, user_id: int) -> Dict[str, Any]:
        """获取文件信息"""
        try:
            file_record = File.query.filter_by(id=file_id).first()
            
            if not file_record:
                raise Exception('文件不存在')
            
            # 检查权限（只有上传者或管理员可以访问）
            if file_record.uploader_id != user_id:
                # TODO: 检查是否为管理员
                if not file_record.is_public:
                    raise Exception('没有权限访问此文件')
            
            return file_record.to_dict()
            
        except Exception as e:
            logger.error(f'Get file error: {str(e)}')
            raise Exception(f'获取文件信息失败: {str(e)}')
    
    @staticmethod
    def get_file_path(file_id: int, user_id: int) -> Tuple[str, str]:
        """获取文件路径和文件名"""
        try:
            file_record = File.query.filter_by(id=file_id).first()
            
            if not file_record:
                raise Exception('文件不存在')
            
            # 检查权限
            if file_record.uploader_id != user_id:
                if not file_record.is_public:
                    raise Exception('没有权限访问此文件')
            
            # 检查文件是否存在
            if not os.path.exists(file_record.file_path):
                raise Exception('文件不存在')
            
            # 增加下载次数
            file_record.increment_download_count()
            
            return file_record.file_path, file_record.original_name
            
        except Exception as e:
            logger.error(f'Get file path error: {str(e)}')
            raise Exception(f'获取文件路径失败: {str(e)}')
    
    @staticmethod
    def get_files(params: Dict[str, Any]) -> Dict[str, Any]:
        """获取文件列表"""
        try:
            user_id = params.get('user_id')
            page = params.get('page', 1)
            size = params.get('size', 10)
            related_type = params.get('related_type')
            related_id = params.get('related_id')
            file_type = params.get('file_type')
            
            # 构建查询
            query = File.query.filter_by(uploader_id=user_id)
            
            if related_type:
                query = query.filter(File.related_type == related_type)
            
            if related_id:
                query = query.filter(File.related_id == related_id)
            
            if file_type:
                query = query.filter(File.file_type.like(f'{file_type}%'))
            
            # 分页查询
            pagination = query.order_by(File.created_at.desc()).paginate(
                page=page, 
                per_page=size, 
                error_out=False
            )
            
            return {
                'items': [file.to_dict() for file in pagination.items],
                'total': pagination.total,
                'page': page,
                'size': size,
                'pages': pagination.pages
            }
            
        except Exception as e:
            logger.error(f'Get files error: {str(e)}')
            raise Exception(f'获取文件列表失败: {str(e)}')
    
    @staticmethod
    def update_file(file_id: int, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新文件信息"""
        try:
            file_record = File.query.filter_by(id=file_id, uploader_id=user_id).first()
            
            if not file_record:
                raise Exception('文件不存在或没有权限')
            
            # 更新文件信息
            if 'description' in data:
                file_record.description = data['description']
            
            if 'is_public' in data:
                file_record.is_public = data['is_public']
            
            db.session.commit()
            
            return file_record.to_dict()
            
        except Exception as e:
            logger.error(f'Update file error: {str(e)}')
            raise Exception(f'更新文件信息失败: {str(e)}')
    
    @staticmethod
    def delete_file(file_id: int, user_id: int) -> None:
        """删除文件"""
        try:
            file_record = File.query.filter_by(id=file_id, uploader_id=user_id).first()
            
            if not file_record:
                raise Exception('文件不存在或没有权限')
            
            file_record.delete_file()
            
        except Exception as e:
            logger.error(f'Delete file error: {str(e)}')
            raise Exception(f'删除文件失败: {str(e)}')
    
    @staticmethod
    def batch_delete_files(file_ids: List[int], user_id: int) -> None:
        """批量删除文件"""
        try:
            files = File.query.filter(
                File.id.in_(file_ids),
                File.uploader_id == user_id
            ).all()
            
            for file_record in files:
                file_record.delete_file()
            
        except Exception as e:
            logger.error(f'Batch delete files error: {str(e)}')
            raise Exception(f'批量删除文件失败: {str(e)}')
    
    @staticmethod
    def get_storage_info(user_id: int) -> Dict[str, Any]:
        """获取存储信息"""
        try:
            files = File.query.filter_by(uploader_id=user_id).all()
            
            total_size = sum(file.file_size for file in files)
            total_count = len(files)
            
            # 按类型统计
            type_stats = {}
            for file in files:
                file_type = file.file_type.split('/')[0] if file.file_type else 'unknown'
                if file_type not in type_stats:
                    type_stats[file_type] = {'count': 0, 'size': 0}
                type_stats[file_type]['count'] += 1
                type_stats[file_type]['size'] += file.file_size
            
            return {
                'total_size': total_size,
                'total_size_formatted': FileService._format_file_size(total_size),
                'total_count': total_count,
                'type_stats': type_stats,
                'max_size': FileService.MAX_FILE_SIZE,
                'max_size_formatted': FileService._format_file_size(FileService.MAX_FILE_SIZE)
            }
            
        except Exception as e:
            logger.error(f'Get storage info error: {str(e)}')
            raise Exception(f'获取存储信息失败: {str(e)}')
    
    @staticmethod
    def cleanup_unused_files() -> Dict[str, Any]:
        """清理无用文件"""
        try:
            # 查找没有关联记录的文件
            unused_files = File.query.filter(
                File.related_type.is_(None),
                File.related_id.is_(None)
            ).all()
            
            cleaned_count = 0
            cleaned_size = 0
            
            for file_record in unused_files:
                try:
                    cleaned_size += file_record.file_size
                    file_record.delete_file()
                    cleaned_count += 1
                except Exception as e:
                    logger.error(f'Cleanup file {file_record.id} error: {str(e)}')
                    continue
            
            return {
                'cleaned_count': cleaned_count,
                'cleaned_size': cleaned_size,
                'cleaned_size_formatted': FileService._format_file_size(cleaned_size)
            }
            
        except Exception as e:
            logger.error(f'Cleanup unused files error: {str(e)}')
            raise Exception(f'清理无用文件失败: {str(e)}')
    
    @staticmethod
    def get_allowed_types() -> Dict[str, Any]:
        """获取允许的文件类型"""
        return {
            'allowed_extensions': FileService.ALLOWED_EXTENSIONS,
            'max_file_size': FileService.MAX_FILE_SIZE,
            'max_file_size_formatted': FileService._format_file_size(FileService.MAX_FILE_SIZE)
        }
    
    @staticmethod
    def _is_allowed_file_type(extension: str) -> bool:
        """检查文件类型是否允许"""
        for category, extensions in FileService.ALLOWED_EXTENSIONS.items():
            if extension in extensions:
                return True
        return False
    
    @staticmethod
    def _format_file_size(size: int) -> str:
        """格式化文件大小"""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        else:
            return f"{size / (1024 * 1024 * 1024):.1f} GB"
