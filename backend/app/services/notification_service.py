from datetime import datetime
from typing import List, Dict, Any, Optional
from app.models.user import User
from app.models.notification import Notification, NotificationType
from app import db
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """通知服务"""
    
    @staticmethod
    def get_notifications(params: Dict[str, Any]) -> Dict[str, Any]:
        """获取通知列表"""
        try:
            user_id = params.get('user_id')
            page = params.get('page', 1)
            size = params.get('size', 10)
            notification_type = params.get('type')
            is_read = params.get('is_read')
            
            # 构建查询
            query = Notification.query.filter_by(user_id=user_id)
            
            if notification_type:
                query = query.filter(Notification.type == NotificationType(notification_type))
            
            if is_read is not None:
                query = query.filter(Notification.is_read == is_read)
            
            # 分页查询
            pagination = query.order_by(Notification.created_at.desc()).paginate(
                page=page, 
                per_page=size, 
                error_out=False
            )
            
            return {
                'items': [notification.to_dict() for notification in pagination.items],
                'total': pagination.total,
                'page': page,
                'size': size,
                'pages': pagination.pages
            }
            
        except Exception as e:
            logger.error(f'Get notifications error: {str(e)}')
            raise Exception(f'获取通知列表失败: {str(e)}')
    
    @staticmethod
    def get_notification(notification_id: int, user_id: int) -> Dict[str, Any]:
        """获取单个通知详情"""
        try:
            notification = Notification.query.filter_by(
                id=notification_id, 
                user_id=user_id
            ).first()
            
            if not notification:
                raise Exception('通知不存在')
            
            return notification.to_dict()
            
        except Exception as e:
            logger.error(f'Get notification error: {str(e)}')
            raise Exception(f'获取通知详情失败: {str(e)}')
    
    @staticmethod
    def mark_as_read(notification_id: int, user_id: int) -> None:
        """标记通知为已读"""
        try:
            notification = Notification.query.filter_by(
                id=notification_id, 
                user_id=user_id
            ).first()
            
            if not notification:
                raise Exception('通知不存在')
            
            notification.mark_as_read()
            
        except Exception as e:
            logger.error(f'Mark notification as read error: {str(e)}')
            raise Exception(f'标记已读失败: {str(e)}')
    
    @staticmethod
    def batch_mark_as_read(notification_ids: List[int], user_id: int) -> None:
        """批量标记通知为已读"""
        try:
            notifications = Notification.query.filter(
                Notification.id.in_(notification_ids),
                Notification.user_id == user_id
            ).all()
            
            for notification in notifications:
                notification.mark_as_read()
            
        except Exception as e:
            logger.error(f'Batch mark notifications as read error: {str(e)}')
            raise Exception(f'批量标记已读失败: {str(e)}')
    
    @staticmethod
    def delete_notification(notification_id: int, user_id: int) -> None:
        """删除通知"""
        try:
            notification = Notification.query.filter_by(
                id=notification_id, 
                user_id=user_id
            ).first()
            
            if not notification:
                raise Exception('通知不存在')
            
            db.session.delete(notification)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Delete notification error: {str(e)}')
            raise Exception(f'删除通知失败: {str(e)}')
    
    @staticmethod
    def batch_delete_notifications(notification_ids: List[int], user_id: int) -> None:
        """批量删除通知"""
        try:
            notifications = Notification.query.filter(
                Notification.id.in_(notification_ids),
                Notification.user_id == user_id
            ).all()
            
            for notification in notifications:
                db.session.delete(notification)
            
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Batch delete notifications error: {str(e)}')
            raise Exception(f'批量删除通知失败: {str(e)}')
    
    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """获取未读通知数量"""
        try:
            count = Notification.query.filter_by(
                user_id=user_id, 
                is_read=False
            ).count()
            
            return count
            
        except Exception as e:
            logger.error(f'Get unread count error: {str(e)}')
            raise Exception(f'获取未读数量失败: {str(e)}')
    
    @staticmethod
    def send_notification(sender_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送通知"""
        try:
            # 验证必要参数
            title = data.get('title')
            content = data.get('content')
            notification_type = data.get('type', 'system')
            user_id = data.get('user_id')
            related_id = data.get('related_id')
            related_type = data.get('related_type')
            
            if not title:
                raise Exception('通知标题不能为空')
            
            # 创建通知
            notification = Notification(
                user_id=user_id,
                title=title,
                content=content,
                type=NotificationType(notification_type),
                related_id=related_id,
                related_type=related_type
            )
            
            db.session.add(notification)
            db.session.commit()
            
            return notification.to_dict()
            
        except Exception as e:
            logger.error(f'Send notification error: {str(e)}')
            raise Exception(f'发送通知失败: {str(e)}')
    
    @staticmethod
    def send_notification_to_user(sender_id: int, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送通知给指定用户"""
        try:
            # 验证用户存在
            user = User.query.get(user_id)
            if not user:
                raise Exception('用户不存在')
            
            # 添加用户ID到数据中
            data['user_id'] = user_id
            
            return NotificationService.send_notification(sender_id, data)
            
        except Exception as e:
            logger.error(f'Send notification to user error: {str(e)}')
            raise Exception(f'发送通知失败: {str(e)}')
    
    @staticmethod
    def send_notification_to_all(sender_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """发送通知给所有用户"""
        try:
            # 获取所有用户
            users = User.query.filter_by(status='active').all()
            
            if not users:
                raise Exception('没有找到活跃用户')
            
            # 批量创建通知
            notifications = []
            for user in users:
                notification = Notification(
                    user_id=user.id,
                    title=data.get('title'),
                    content=data.get('content'),
                    type=NotificationType(data.get('type', 'system')),
                    related_id=data.get('related_id'),
                    related_type=data.get('related_type')
                )
                notifications.append(notification)
            
            db.session.add_all(notifications)
            db.session.commit()
            
            return {
                'message': f'成功发送通知给 {len(users)} 个用户',
                'count': len(users)
            }
            
        except Exception as e:
            logger.error(f'Send notification to all error: {str(e)}')
            raise Exception(f'发送通知失败: {str(e)}')
    
    @staticmethod
    def get_notification_settings(user_id: int) -> Dict[str, Any]:
        """获取用户通知设置"""
        try:
            # 这里应该从用户设置表获取
            # 目前返回默认设置
            settings = {
                'email_notifications': True,
                'exam_notifications': True,
                'score_notifications': True,
                'system_notifications': True,
                'announcement_notifications': True
            }
            
            return settings
            
        except Exception as e:
            logger.error(f'Get notification settings error: {str(e)}')
            raise Exception(f'获取通知设置失败: {str(e)}')
    
    @staticmethod
    def update_notification_settings(user_id: int, settings_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新用户通知设置"""
        try:
            # 这里应该保存到用户设置表
            # 目前返回更新后的设置
            settings = {
                'email_notifications': settings_data.get('email_notifications', True),
                'exam_notifications': settings_data.get('exam_notifications', True),
                'score_notifications': settings_data.get('score_notifications', True),
                'system_notifications': settings_data.get('system_notifications', True),
                'announcement_notifications': settings_data.get('announcement_notifications', True)
            }
            
            return settings
            
        except Exception as e:
            logger.error(f'Update notification settings error: {str(e)}')
            raise Exception(f'更新通知设置失败: {str(e)}')
    
    @staticmethod
    def create_exam_notification(user_id: int, exam_title: str, exam_id: int) -> None:
        """创建考试通知"""
        try:
            notification = Notification(
                user_id=user_id,
                title=f'新考试发布: {exam_title}',
                content=f'您有新的考试可以参加: {exam_title}',
                type=NotificationType.EXAM,
                related_id=exam_id,
                related_type='exam'
            )
            
            db.session.add(notification)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Create exam notification error: {str(e)}')
    
    @staticmethod
    def create_score_notification(user_id: int, exam_title: str, score: float, exam_id: int) -> None:
        """创建成绩通知"""
        try:
            notification = Notification(
                user_id=user_id,
                title=f'考试成绩发布: {exam_title}',
                content=f'您的考试成绩已发布，得分: {score}分',
                type=NotificationType.SCORE,
                related_id=exam_id,
                related_type='exam'
            )
            
            db.session.add(notification)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Create score notification error: {str(e)}')
    
    @staticmethod
 def create_system_notification(user_id: int, title: str, content: str) -> None:
        """创建系统通知"""
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                content=content,
                type=NotificationType.SYSTEM
            )
            
            db.session.add(notification)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Create system notification error: {str(e)}')
    
    @staticmethod
    def create_announcement_notification(user_id: int, title: str, content: str, announcement_id: int) -> None:
        """创建公告通知"""
        try:
            notification = Notification(
                user_id=user_id,
                title=f'系统公告: {title}',
                content=content,
                type=NotificationType.ANNOUNCEMENT,
                related_id=announcement_id,
                related_type='announcement'
            )
            
            db.session.add(notification)
            db.session.commit()
            
        except Exception as e:
            logger.error(f'Create announcement notification error: {str(e)}')
