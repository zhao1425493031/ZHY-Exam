from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.models.user import User
from app.models.announcement import Announcement, AnnouncementType, AnnouncementPriority, AnnouncementStatus
from app.services.notification_service import NotificationService
from app import db
import logging

logger = logging.getLogger(__name__)

class AnnouncementService:
    """公告服务"""
    
    @staticmethod
    def get_announcements(params: Dict[str, Any]) -> Dict[str, Any]:
        """获取公告列表"""
        try:
            user_id = params.get('user_id')
            page = params.get('page', 1)
            size = params.get('size', 10)
            status = params.get('status')
            announcement_type = params.get('type')
            priority = params.get('priority')
            
            # 构建查询
            query = Announcement.query
            
            # 非管理员只能看到已发布的公告
            user = User.query.get(user_id)
            if not user or user.role != 'admin':
                query = query.filter(Announcement.status == AnnouncementStatus.PUBLISHED)
            
            if status:
                query = query.filter(Announcement.status == AnnouncementStatus(status))
            
            if announcement_type:
                query = query.filter(Announcement.type == AnnouncementType(announcement_type))
            
            if priority:
                query = query.filter(Announcement.priority == AnnouncementPriority(priority))
            
            # 分页查询
            pagination = query.order_by(Announcement.created_at.desc()).paginate(
                page=page, 
                per_page=size, 
                error_out=False
            )
            
            return {
                'items': [announcement.to_dict() for announcement in pagination.items],
                'total': pagination.total,
                'page': page,
                'size': size,
                'pages': pagination.pages
            }
            
        except Exception as e:
            logger.error(f'Get announcements error: {str(e)}')
            raise Exception(f'获取公告列表失败: {str(e)}')
    
    @staticmethod
    def get_public_announcements(params: Dict[str, Any]) -> Dict[str, Any]:
        """获取公开公告列表"""
        try:
            page = params.get('page', 1)
            size = params.get('size', 10)
            
            # 只获取已发布且未过期的公告
            query = Announcement.query.filter(
                Announcement.status == AnnouncementStatus.PUBLISHED
            ).filter(
                db.or_(
                    Announcement.expire_time.is_(None),
                    Announcement.expire_time > datetime.utcnow()
                )
            )
            
            # 分页查询
            pagination = query.order_by(Announcement.priority.desc(), Announcement.created_at.desc()).paginate(
                page=page, 
                per_page=size, 
                error_out=False
            )
            
            return {
                'items': [announcement.to_dict() for announcement in pagination.items],
                'total': pagination.total,
                'page': page,
                'size': size,
                'pages': pagination.pages
            }
            
        except Exception as e:
            logger.error(f'Get public announcements error: {str(e)}')
            raise Exception(f'获取公开公告失败: {str(e)}')
    
    @staticmethod
    def get_announcement(announcement_id: int, user_id: int) -> Dict[str, Any]:
        """获取单个公告详情"""
        try:
            announcement = Announcement.query.get(announcement_id)
            
            if not announcement:
                raise Exception('公告不存在')
            
            # 检查权限
            user = User.query.get(user_id)
            if not user or user.role != 'admin':
                if announcement.status != AnnouncementStatus.PUBLISHED:
                    raise Exception('公告不存在')
                
                if announcement.is_expired():
                    raise Exception('公告已过期')
            
            # 增加查看次数
            announcement.increment_view_count()
            
            return announcement.to_dict()
            
        except Exception as e:
            logger.error(f'Get announcement error: {str(e)}')
            raise Exception(f'获取公告详情失败: {str(e)}')
    
    @staticmethod
    def get_public_announcement(announcement_id: int) -> Dict[str, Any]:
        """获取公开公告详情"""
        try:
            announcement = Announcement.query.get(announcement_id)
            
            if not announcement:
                raise Exception('公告不存在')
            
            if announcement.status != AnnouncementStatus.PUBLISHED:
                raise Exception('公告不存在')
            
            if announcement.is_expired():
                raise Exception('公告已过期')
            
            # 增加查看次数
            announcement.increment_view_count()
            
            return announcement.to_dict()
            
        except Exception as e:
            logger.error(f'Get public announcement error: {str(e)}')
            raise Exception(f'获取公告详情失败: {str(e)}')
    
    @staticmethod
    def create_announcement(creator_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """创建公告"""
        try:
            # 验证必要参数
            title = data.get('title')
            content = data.get('content')
            announcement_type = data.get('type', 'system')
            priority = data.get('priority', 'medium')
            
            if not title or not content:
                raise Exception('标题和内容不能为空')
            
            # 创建公告
            announcement = Announcement(
                title=title,
                content=content,
                type=AnnouncementType(announcement_type),
                priority=AnnouncementPriority(priority),
                created_by=creator_id,
                expire_time=datetime.fromisoformat(data['expire_time'].replace('Z', '+00:00')) if data.get('expire_time') else None
            )
            
            db.session.add(announcement)
            db.session.commit()
            
            return announcement.to_dict()
            
        except Exception as e:
            logger.error(f'Create announcement error: {str(e)}')
            raise Exception(f'创建公告失败: {str(e)}')
    
    @staticmethod
    def update_announcement(announcement_id: int, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """更新公告"""
        try:
            announcement = Announcement.query.get(announcement_id)
            
            if not announcement:
                raise Exception('公告不存在')
            
            # 检查权限
            if announcement.created_by != user_id:
                user = User.query.get(user_id)
                if not user or user.role != 'admin':
                    raise Exception('没有权限修改此公告')
            
            # 更新公告信息
            if 'title' in data:
                announcement.title = data['title']
            
            if 'content' in data:
                announcement.content = data['content']
            
            if 'type' in data:
                announcement.type = AnnouncementType(data['type'])
            
            if 'priority' in data:
                announcement.priority = AnnouncementPriority(data['priority'])
            
            if 'expire_time' in data:
                announcement.expire_time = datetime.fromisoformat(data['expire_time'].replace('Z', '+00:00')) if data['expire_time'] else None
            
            db.session.commit()
            
            return announcement.to_dict()
            
        except Exception as e:
            logger.error(f'Update announcement error: {str(e)}')
            raise Exception(f'更新公告失败: {str(e)}')
    
    @staticmethod
    def delete_announcement(announcement_id: int, user_id: int) -> None:
        """删除公告"""
        try:
            announcement = Announcement.query.get(announcement_id)
            
            if not announcement:
                raise Exception('公告不存在')
            
            # 检查权限
            if announcement.created_by != user_id:
                user = User.query.get(user_id)
                if not user or user.role != 'admin':
                    raise Exception('没有权限删除此公告')
            
            db.session.delete(announcement)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Delete announcement error: {str(e)}')
            raise Exception(f'删除公告失败: {str(e)}')
    
    @staticmethod
    def publish_announcement(announcement_id: int, user_id: int) -> Dict[str, Any]:
        """发布公告"""
        try:
            announcement = Announcement.query.get(announcement_id)
            
            if not announcement:
                raise Exception('公告不存在')
            
            # 检查权限
            if announcement.created_by != user_id:
                user = User.query.get(user_id)
                if not user or user.role != 'admin':
                    raise Exception('没有权限发布此公告')
            
            # 发布公告
            announcement.publish()
            
            # 发送通知给所有用户
            try:
                NotificationService.create_announcement_notification(
                    user_id=0,  # 系统通知
                    title=announcement.title,
                    content=announcement.content,
                    announcement_id=announcement.id
                )
            except Exception as e:
                logger.error(f'Send announcement notification error: {str(e)}')
            
            return announcement.to_dict()
            
        except Exception as e:
            logger.error(f'Publish announcement error: {str(e)}')
            raise Exception(f'发布公告失败: {str(e)}')
    
    @staticmethod
    def unpublish_announcement(announcement_id: int, user_id: int) -> Dict[str, Any]:
        """取消发布公告"""
        try:
            announcement = Announcement.query.get(announcement_id)
            
            if not announcement:
                raise Exception('公告不存在')
            
            # 检查权限
            if announcement.created_by != user_id:
                user = User.query.get(user_id)
                if not user or user.role != 'admin':
                    raise Exception('没有权限取消发布此公告')
            
            # 取消发布
            announcement.unpublish()
            
            return announcement.to_dict()
            
        except Exception as e:
            logger.error(f'Unpublish announcement error: {str(e)}')
            raise Exception(f'取消发布公告失败: {str(e)}')
    
    @staticmethod
    def batch_publish_announcements(announcement_ids: List[int], user_id: int) -> None:
        """批量发布公告"""
        try:
            announcements = Announcement.query.filter(
                Announcement.id.in_(announcement_ids)
            ).all()
            
            for announcement in announcements:
                # 检查权限
                if announcement.created_by != user_id:
                    user = User.query.get(user_id)
                    if not user or user.role != 'admin':
                        continue
                
                announcement.publish()
                
                # 发送通知
                try:
                    NotificationService.create_announcement_notification(
                        user_id=0,
                        title=announcement.title,
                        content=announcement.content,
                        announcement_id=announcement.id
                    )
                except Exception as e:
                    logger.error(f'Send announcement notification error: {str(e)}')
            
        except Exception as e:
            logger.error(f'Batch publish announcements error: {str(e)}')
            raise Exception(f'批量发布公告失败: {str(e)}')
    
    @staticmethod
    def batch_delete_announcements(announcement_ids: List[int], user_id: int) -> None:
        """批量删除公告"""
        try:
            announcements = Announcement.query.filter(
                Announcement.id.in_(announcement_ids)
            ).all()
            
            for announcement in announcements:
                # 检查权限
                if announcement.created_by != user_id:
                    user = User.query.get(user_id)
                    if not user or user.role != 'admin':
                        continue
                
                db.session.delete(announcement)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Batch delete announcements error: {str(e)}')
            raise Exception(f'批量删除公告失败: {str(e)}')
    
    @staticmethod
    def get_announcement_statistics() -> Dict[str, Any]:
        """获取公告统计"""
        try:
            total_count = Announcement.query.count()
            published_count = Announcement.query.filter(
                Announcement.status == AnnouncementStatus.PUBLISHED
            ).count()
            draft_count = Announcement.query.filter(
                Announcement.status == AnnouncementStatus.DRAFT
            ).count()
            archived_count = Announcement.query.filter(
                Announcement.status == AnnouncementStatus.ARCHIVED
            ).count()
            
            # 按类型统计
            type_stats = {}
            for announcement_type in AnnouncementType:
                count = Announcement.query.filter(
                    Announcement.type == announcement_type
                ).count()
                type_stats[announcement_type.value] = count
            
            # 按优先级统计
            priority_stats = {}
            for priority in AnnouncementPriority:
                count = Announcement.query.filter(
                    Announcement.priority == priority
                ).count()
                priority_stats[priority.value] = count
            
            # 最近7天的公告数量
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            recent_count = Announcement.query.filter(
                Announcement.created_at >= seven_days_ago
            ).count()
            
            return {
                'total_count': total_count,
                'published_count': published_count,
                'draft_count': draft_count,
                'archived_count': archived_count,
                'type_stats': type_stats,
                'priority_stats': priority_stats,
                'recent_count': recent_count
            }
            
        except Exception as e:
            logger.error(f'Get announcement statistics error: {str(e)}')
            raise Exception(f'获取公告统计失败: {str(e)}')
