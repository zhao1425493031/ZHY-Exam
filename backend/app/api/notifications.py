from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.notification import Notification
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.notification_service import NotificationService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
notification_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

@notification_bp.route('', methods=['GET'])
@notification_bp.route('/', methods=['GET'])
@jwt_required()
def get_notifications():
    """获取用户通知列表"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        notification_type = request.args.get('type')
        is_read = request.args.get('is_read')
        
        # 构建查询参数
        params = {
            'page': page,
            'size': size,
            'user_id': current_user_id
        }
        
        if notification_type:
            params['type'] = notification_type
        if is_read is not None:
            params['is_read'] = is_read.lower() == 'true'
        
        # 获取通知列表
        notifications = NotificationService.get_notifications(params)
        
        return jsonify(build_response(data=notifications))
        
    except Exception as e:
        logger.error(f'Get notifications error: {str(e)}')
        return jsonify(build_error_response(500, f'获取通知列表失败: {str(e)}')), 500

@notification_bp.route('/<int:notification_id>', methods=['GET'])
@jwt_required()
def get_notification(notification_id):
    """获取单个通知详情"""
    try:
        current_user_id = get_jwt_identity()
        
        notification = NotificationService.get_notification(notification_id, current_user_id)
        
        return jsonify(build_response(data=notification))
        
    except Exception as e:
        logger.error(f'Get notification error: {str(e)}')
        return jsonify(build_error_response(500, f'获取通知详情失败: {str(e)}')), 500

@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_as_read(notification_id):
    """标记通知为已读"""
    try:
        current_user_id = get_jwt_identity()
        
        NotificationService.mark_as_read(notification_id, current_user_id)
        
        return jsonify(build_response(data={'message': '标记已读成功'}))
        
    except Exception as e:
        logger.error(f'Mark notification as read error: {str(e)}')
        return jsonify(build_error_response(500, f'标记已读失败: {str(e)}')), 500

@notification_bp.route('/batch-read', methods=['PUT'])
@jwt_required()
def batch_mark_as_read():
    """批量标记通知为已读"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        notification_ids = data.get('notification_ids', [])
        if not notification_ids:
            return jsonify(build_error_response(400, '请选择要标记的通知')), 400
        
        NotificationService.batch_mark_as_read(notification_ids, current_user_id)
        
        return jsonify(build_response(data={'message': '批量标记已读成功'}))
        
    except Exception as e:
        logger.error(f'Batch mark notifications as read error: {str(e)}')
        return jsonify(build_error_response(500, f'批量标记已读失败: {str(e)}')), 500

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@jwt_required()
def delete_notification(notification_id):
    """删除通知"""
    try:
        current_user_id = get_jwt_identity()
        
        NotificationService.delete_notification(notification_id, current_user_id)
        
        return jsonify(build_response(data={'message': '删除通知成功'}))
        
    except Exception as e:
        logger.error(f'Delete notification error: {str(e)}')
        return jsonify(build_error_response(500, f'删除通知失败: {str(e)}')), 500

@notification_bp.route('/batch-delete', methods=['DELETE'])
@jwt_required()
def batch_delete_notifications():
    """批量删除通知"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        notification_ids = data.get('notification_ids', [])
        if not notification_ids:
            return jsonify(build_error_response(400, '请选择要删除的通知')), 400
        
        NotificationService.batch_delete_notifications(notification_ids, current_user_id)
        
        return jsonify(build_response(data={'message': '批量删除通知成功'}))
        
    except Exception as e:
        logger.error(f'Batch delete notifications error: {str(e)}')
        return jsonify(build_error_response(500, f'批量删除通知失败: {str(e)}')), 500

@notification_bp.route('/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    """获取未读通知数量"""
    try:
        current_user_id = get_jwt_identity()
        
        count = NotificationService.get_unread_count(current_user_id)
        
        return jsonify(build_response(data={'unread_count': count}))
        
    except Exception as e:
        logger.error(f'Get unread count error: {str(e)}')
        return jsonify(build_error_response(500, f'获取未读数量失败: {str(e)}')), 500

@notification_bp.route('/send', methods=['POST'])
@jwt_required()
@require_roles('admin')
def send_notification():
    """发送通知（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['title', 'content', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 发送通知
        notification = NotificationService.send_notification(current_user_id, data)
        
        return jsonify(build_response(data=notification))
        
    except Exception as e:
        logger.error(f'Send notification error: {str(e)}')
        return jsonify(build_error_response(500, f'发送通知失败: {str(e)}')), 500

@notification_bp.route('/send-to-user', methods=['POST'])
@jwt_required()
@require_roles('admin')
def send_notification_to_user():
    """发送通知给指定用户（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['user_id', 'title', 'content', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 发送通知给指定用户
        notification = NotificationService.send_notification_to_user(
            current_user_id, 
            data['user_id'], 
            data
        )
        
        return jsonify(build_response(data=notification))
        
    except Exception as e:
        logger.error(f'Send notification to user error: {str(e)}')
        return jsonify(build_error_response(500, f'发送通知失败: {str(e)}')), 500

@notification_bp.route('/send-to-all', methods=['POST'])
@jwt_required()
@require_roles('admin')
def send_notification_to_all():
    """发送通知给所有用户（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['title', 'content', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 发送通知给所有用户
        result = NotificationService.send_notification_to_all(current_user_id, data)
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Send notification to all error: {str(e)}')
        return jsonify(build_error_response(500, f'发送通知失败: {str(e)}')), 500

@notification_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_notification_settings():
    """获取用户通知设置"""
    try:
        current_user_id = get_jwt_identity()
        
        settings = NotificationService.get_notification_settings(current_user_id)
        
        return jsonify(build_response(data=settings))
        
    except Exception as e:
        logger.error(f'Get notification settings error: {str(e)}')
        return jsonify(build_error_response(500, f'获取通知设置失败: {str(e)}')), 500

@notification_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_notification_settings():
    """更新用户通知设置"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        settings = NotificationService.update_notification_settings(current_user_id, data)
        
        return jsonify(build_response(data=settings))
        
    except Exception as e:
        logger.error(f'Update notification settings error: {str(e)}')
        return jsonify(build_error_response(500, f'更新通知设置失败: {str(e)}')), 500
