from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.announcement import Announcement
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.announcement_service import AnnouncementService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
announcement_bp = Blueprint('announcements', __name__, url_prefix='/api/announcements')

@announcement_bp.route('/', methods=['GET'])
@jwt_required()
def get_announcements():
    """获取公告列表"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        status = request.args.get('status')
        announcement_type = request.args.get('type')
        priority = request.args.get('priority')
        
        # 构建查询参数
        params = {
            'page': page,
            'size': size,
            'user_id': current_user_id
        }
        
        if status:
            params['status'] = status
        if announcement_type:
            params['type'] = announcement_type
        if priority:
            params['priority'] = priority
        
        # 获取公告列表
        announcements = AnnouncementService.get_announcements(params)
        
        return jsonify(build_response(data=announcements))
        
    except Exception as e:
        logger.error(f'Get announcements error: {str(e)}')
        return jsonify(build_error_response(500, f'获取公告列表失败: {str(e)}')), 500

@announcement_bp.route('/public', methods=['GET'])
def get_public_announcements():
    """获取公开公告列表（无需登录）"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        
        # 构建查询参数
        params = {
            'page': page,
            'size': size,
            'status': 'published'
        }
        
        # 获取公开公告列表
        announcements = AnnouncementService.get_public_announcements(params)
        
        return jsonify(build_response(data=announcements))
        
    except Exception as e:
        logger.error(f'Get public announcements error: {str(e)}')
        return jsonify(build_error_response(500, f'获取公开公告失败: {str(e)}')), 500

@announcement_bp.route('/<int:announcement_id>', methods=['GET'])
@jwt_required()
def get_announcement(announcement_id):
    """获取单个公告详情"""
    try:
        current_user_id = get_jwt_identity()
        
        announcement = AnnouncementService.get_announcement(announcement_id, current_user_id)
        
        return jsonify(build_response(data=announcement))
        
    except Exception as e:
        logger.error(f'Get announcement error: {str(e)}')
        return jsonify(build_error_response(500, f'获取公告详情失败: {str(e)}')), 500

@announcement_bp.route('/<int:announcement_id>/public', methods=['GET'])
def get_public_announcement(announcement_id):
    """获取公开公告详情（无需登录）"""
    try:
        announcement = AnnouncementService.get_public_announcement(announcement_id)
        
        return jsonify(build_response(data=announcement))
        
    except Exception as e:
        logger.error(f'Get public announcement error: {str(e)}')
        return jsonify(build_error_response(500, f'获取公告详情失败: {str(e)}')), 500

@announcement_bp.route('/', methods=['POST'])
@jwt_required()
@require_roles('admin')
def create_announcement():
    """创建公告（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['title', 'content', 'type']
        for field in required_fields:
            if field not in data:
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 创建公告
        announcement = AnnouncementService.create_announcement(current_user_id, data)
        
        return jsonify(build_response(data=announcement))
        
    except Exception as e:
        logger.error(f'Create announcement error: {str(e)}')
        return jsonify(build_error_response(500, f'创建公告失败: {str(e)}')), 500

@announcement_bp.route('/<int:announcement_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_announcement(announcement_id):
    """更新公告（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 更新公告
        announcement = AnnouncementService.update_announcement(announcement_id, current_user_id, data)
        
        return jsonify(build_response(data=announcement))
        
    except Exception as e:
        logger.error(f'Update announcement error: {str(e)}')
        return jsonify(build_error_response(500, f'更新公告失败: {str(e)}')), 500

@announcement_bp.route('/<int:announcement_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_announcement(announcement_id):
    """删除公告（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        AnnouncementService.delete_announcement(announcement_id, current_user_id)
        
        return jsonify(build_response(data={'message': '删除公告成功'}))
        
    except Exception as e:
        logger.error(f'Delete announcement error: {str(e)}')
        return jsonify(build_error_response(500, f'删除公告失败: {str(e)}')), 500

@announcement_bp.route('/<int:announcement_id>/publish', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def publish_announcement(announcement_id):
    """发布公告（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        announcement = AnnouncementService.publish_announcement(announcement_id, current_user_id)
        
        return jsonify(build_response(data=announcement))
        
    except Exception as e:
        logger.error(f'Publish announcement error: {str(e)}')
        return jsonify(build_error_response(500, f'发布公告失败: {str(e)}')), 500

@announcement_bp.route('/<int:announcement_id>/unpublish', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def unpublish_announcement(announcement_id):
    """取消发布公告（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        announcement = AnnouncementService.unpublish_announcement(announcement_id, current_user_id)
        
        return jsonify(build_response(data=announcement))
        
    except Exception as e:
        logger.error(f'Unpublish announcement error: {str(e)}')
        return jsonify(build_error_response(500, f'取消发布公告失败: {str(e)}')), 500

@announcement_bp.route('/batch-publish', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def batch_publish_announcements():
    """批量发布公告（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        announcement_ids = data.get('announcement_ids', [])
        if not announcement_ids:
            return jsonify(build_error_response(400, '请选择要发布的公告')), 400
        
        AnnouncementService.batch_publish_announcements(announcement_ids, current_user_id)
        
        return jsonify(build_response(data={'message': '批量发布公告成功'}))
        
    except Exception as e:
        logger.error(f'Batch publish announcements error: {str(e)}')
        return jsonify(build_error_response(500, f'批量发布公告失败: {str(e)}')), 500

@announcement_bp.route('/batch-delete', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def batch_delete_announcements():
    """批量删除公告（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        announcement_ids = data.get('announcement_ids', [])
        if not announcement_ids:
            return jsonify(build_error_response(400, '请选择要删除的公告')), 400
        
        AnnouncementService.batch_delete_announcements(announcement_ids, current_user_id)
        
        return jsonify(build_response(data={'message': '批量删除公告成功'}))
        
    except Exception as e:
        logger.error(f'Batch delete announcements error: {str(e)}')
        return jsonify(build_error_response(500, f'批量删除公告失败: {str(e)}')), 500

@announcement_bp.route('/statistics', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_announcement_statistics():
    """获取公告统计（管理员）"""
    try:
        statistics = AnnouncementService.get_announcement_statistics()
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Get announcement statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取公告统计失败: {str(e)}')), 500
