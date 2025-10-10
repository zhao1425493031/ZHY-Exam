from flask import Blueprint, request, jsonify, send_file, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models.user import User
from app.models.file import File
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.file_service import FileService
import os
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
file_bp = Blueprint('files', __name__, url_prefix='/api/files')

@file_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    """上传文件"""
    try:
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        # 获取其他参数
        related_type = request.form.get('related_type', 'general')
        related_id = request.form.get('related_id')
        
        # 上传文件
        uploaded_file = FileService.upload_file(
            file, 
            current_user_id, 
            related_type=related_type,
            related_id=related_id
        )
        
        return jsonify(build_response(data=uploaded_file))
        
    except Exception as e:
        logger.error(f'Upload file error: {str(e)}')
        return jsonify(build_error_response(500, f'上传文件失败: {str(e)}')), 500

@file_bp.route('/batch-upload', methods=['POST'])
@jwt_required()
def batch_upload_files():
    """批量上传文件"""
    try:
        current_user_id = get_jwt_identity()
        
        if 'files' not in request.files:
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        files = request.files.getlist('files')
        if not files:
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        # 获取其他参数
        related_type = request.form.get('related_type', 'general')
        related_id = request.form.get('related_id')
        
        # 批量上传文件
        uploaded_files = FileService.batch_upload_files(
            files, 
            current_user_id, 
            related_type=related_type,
            related_id=related_id
        )
        
        return jsonify(build_response(data=uploaded_files))
        
    except Exception as e:
        logger.error(f'Batch upload files error: {str(e)}')
        return jsonify(build_error_response(500, f'批量上传文件失败: {str(e)}')), 500

@file_bp.route('/<int:file_id>', methods=['GET'])
@jwt_required()
def get_file(file_id):
    """获取文件信息"""
    try:
        current_user_id = get_jwt_identity()
        
        file_info = FileService.get_file(file_id, current_user_id)
        
        return jsonify(build_response(data=file_info))
        
    except Exception as e:
        logger.error(f'Get file error: {str(e)}')
        return jsonify(build_error_response(500, f'获取文件信息失败: {str(e)}')), 500

@file_bp.route('/<int:file_id>/download', methods=['GET'])
@jwt_required()
def download_file(file_id):
    """下载文件"""
    try:
        current_user_id = get_jwt_identity()
        
        file_path, filename = FileService.get_file_path(file_id, current_user_id)
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f'Download file error: {str(e)}')
        return jsonify(build_error_response(500, f'下载文件失败: {str(e)}')), 500

@file_bp.route('/<int:file_id>/preview', methods=['GET'])
@jwt_required()
def preview_file(file_id):
    """预览文件"""
    try:
        current_user_id = get_jwt_identity()
        
        file_path, filename = FileService.get_file_path(file_id, current_user_id)
        
        # 根据文件类型返回不同的预览方式
        file_info = FileService.get_file(file_id, current_user_id)
        file_type = file_info['file_type']
        
        if file_type.startswith('image/'):
            return send_file(file_path, mimetype=file_type)
        elif file_type.startswith('text/'):
            return send_file(file_path, mimetype=file_type)
        else:
            return jsonify(build_error_response(400, '不支持预览此文件类型')), 400
        
    except Exception as e:
        logger.error(f'Preview file error: {str(e)}')
        return jsonify(build_error_response(500, f'预览文件失败: {str(e)}')), 500

@file_bp.route('/', methods=['GET'])
@jwt_required()
def get_files():
    """获取文件列表"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        related_type = request.args.get('related_type')
        related_id = request.args.get('related_id', type=int)
        file_type = request.args.get('file_type')
        
        # 构建查询参数
        params = {
            'page': page,
            'size': size,
            'user_id': current_user_id
        }
        
        if related_type:
            params['related_type'] = related_type
        if related_id:
            params['related_id'] = related_id
        if file_type:
            params['file_type'] = file_type
        
        # 获取文件列表
        files = FileService.get_files(params)
        
        return jsonify(build_response(data=files))
        
    except Exception as e:
        logger.error(f'Get files error: {str(e)}')
        return jsonify(build_error_response(500, f'获取文件列表失败: {str(e)}')), 500

@file_bp.route('/<int:file_id>', methods=['PUT'])
@jwt_required()
def update_file(file_id):
    """更新文件信息"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 更新文件信息
        file_info = FileService.update_file(file_id, current_user_id, data)
        
        return jsonify(build_response(data=file_info))
        
    except Exception as e:
        logger.error(f'Update file error: {str(e)}')
        return jsonify(build_error_response(500, f'更新文件信息失败: {str(e)}')), 500

@file_bp.route('/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_file(file_id):
    """删除文件"""
    try:
        current_user_id = get_jwt_identity()
        
        FileService.delete_file(file_id, current_user_id)
        
        return jsonify(build_response(data={'message': '删除文件成功'}))
        
    except Exception as e:
        logger.error(f'Delete file error: {str(e)}')
        return jsonify(build_error_response(500, f'删除文件失败: {str(e)}')), 500

@file_bp.route('/batch-delete', methods=['DELETE'])
@jwt_required()
def batch_delete_files():
    """批量删除文件"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        file_ids = data.get('file_ids', [])
        if not file_ids:
            return jsonify(build_error_response(400, '请选择要删除的文件')), 400
        
        FileService.batch_delete_files(file_ids, current_user_id)
        
        return jsonify(build_response(data={'message': '批量删除文件成功'}))
        
    except Exception as e:
        logger.error(f'Batch delete files error: {str(e)}')
        return jsonify(build_error_response(500, f'批量删除文件失败: {str(e)}')), 500

@file_bp.route('/storage-info', methods=['GET'])
@jwt_required()
def get_storage_info():
    """获取存储信息"""
    try:
        current_user_id = get_jwt_identity()
        
        storage_info = FileService.get_storage_info(current_user_id)
        
        return jsonify(build_response(data=storage_info))
        
    except Exception as e:
        logger.error(f'Get storage info error: {str(e)}')
        return jsonify(build_error_response(500, f'获取存储信息失败: {str(e)}')), 500

@file_bp.route('/cleanup', methods=['POST'])
@jwt_required()
@require_roles('admin')
def cleanup_files():
    """清理无用文件（管理员）"""
    try:
        result = FileService.cleanup_unused_files()
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Cleanup files error: {str(e)}')
        return jsonify(build_error_response(500, f'清理文件失败: {str(e)}')), 500

@file_bp.route('/allowed-types', methods=['GET'])
def get_allowed_types():
    """获取允许的文件类型"""
    try:
        allowed_types = FileService.get_allowed_types()
        
        return jsonify(build_response(data=allowed_types))
        
    except Exception as e:
        logger.error(f'Get allowed types error: {str(e)}')
        return jsonify(build_error_response(500, f'获取允许的文件类型失败: {str(e)}')), 500
