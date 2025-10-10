from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.exam_record import ExamRecord
from app.models.exam_monitoring import ExamMonitoring
from app.models.user import User
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response, get_client_ip
from app.services.exam_monitoring_service import ExamMonitoringService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
exam_monitoring_bp = Blueprint('exam_monitoring', __name__, url_prefix='/api/exam-monitoring')

@exam_monitoring_bp.route('/events', methods=['POST'])
@jwt_required()
def record_event():
    """记录考试监控事件"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['exam_record_id', 'event_type']
        for field in required_fields:
            if field not in data:
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 验证考试记录是否存在且属于当前用户
        exam_record = ExamRecord.query.get(data['exam_record_id'])
        if not exam_record:
            return jsonify(build_error_response(404, '考试记录不存在')), 404
        
        if exam_record.user_id != current_user_id:
            return jsonify(build_error_response(403, '无权限访问此考试记录')), 403
        
        # 记录监控事件
        event_data = {
            'exam_record_id': data['exam_record_id'],
            'event_type': data['event_type'],
            'event_data': data.get('event_data', {}),
            'ip_address': get_client_ip(request),
            'user_agent': request.headers.get('User-Agent', '')
        }
        
        result = ExamMonitoringService.record_event(event_data)
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Record monitoring event error: {str(e)}')
        return jsonify(build_error_response(500, f'记录监控事件失败: {str(e)}')), 500

@exam_monitoring_bp.route('/<int:exam_record_id>/events', methods=['GET'])
@jwt_required()
def get_exam_events(exam_record_id):
    """获取考试监控事件"""
    try:
        current_user_id = get_jwt_identity()
        
        # 验证考试记录权限
        exam_record = ExamRecord.query.get(exam_record_id)
        if not exam_record:
            return jsonify(build_error_response(404, '考试记录不存在')), 404
        
        if exam_record.user_id != current_user_id:
            return jsonify(build_error_response(403, '无权限访问此考试记录')), 403
        
        # 获取监控事件
        events = ExamMonitoringService.get_exam_events(exam_record_id)
        
        return jsonify(build_response(data=events))
        
    except Exception as e:
        logger.error(f'Get exam events error: {str(e)}')
        return jsonify(build_error_response(500, f'获取监控事件失败: {str(e)}')), 500

@exam_monitoring_bp.route('/suspicious-behavior', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_suspicious_behavior():
    """获取可疑行为记录（管理员）"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)
        exam_id = request.args.get('exam_id', type=int)
        user_id = request.args.get('user_id', type=int)
        
        # 获取可疑行为
        result = ExamMonitoringService.get_suspicious_behavior(
            page=page,
            size=size,
            exam_id=exam_id,
            user_id=user_id
        )
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Get suspicious behavior error: {str(e)}')
        return jsonify(build_error_response(500, f'获取可疑行为失败: {str(e)}')), 500

@exam_monitoring_bp.route('/statistics', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_monitoring_statistics():
    """获取监控统计信息（管理员）"""
    try:
        exam_id = request.args.get('exam_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 获取统计信息
        stats = ExamMonitoringService.get_monitoring_statistics(
            exam_id=exam_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify(build_response(data=stats))
        
    except Exception as e:
        logger.error(f'Get monitoring statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取监控统计失败: {str(e)}')), 500

@exam_monitoring_bp.route('/real-time/<int:exam_id>', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_real_time_monitoring(exam_id):
    """获取实时监控数据（管理员）"""
    try:
        # 获取实时监控数据
        monitoring_data = ExamMonitoringService.get_real_time_monitoring(exam_id)
        
        return jsonify(build_response(data=monitoring_data))
        
    except Exception as e:
        logger.error(f'Get real-time monitoring error: {str(e)}')
        return jsonify(build_error_response(500, f'获取实时监控数据失败: {str(e)}')), 500

@exam_monitoring_bp.route('/alerts', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_monitoring_alerts():
    """获取监控告警（管理员）"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 20, type=int)
        status = request.args.get('status', 'active')
        
        # 获取告警信息
        alerts = ExamMonitoringService.get_monitoring_alerts(
            page=page,
            size=size,
            status=status
        )
        
        return jsonify(build_response(data=alerts))
        
    except Exception as e:
        logger.error(f'Get monitoring alerts error: {str(e)}')
        return jsonify(build_error_response(500, f'获取监控告警失败: {str(e)}')), 500

@exam_monitoring_bp.route('/alerts/<int:alert_id>/resolve', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def resolve_alert(alert_id):
    """处理监控告警（管理员）"""
    try:
        data = request.get_json()
        resolution_note = data.get('resolution_note', '')
        
        # 处理告警
        result = ExamMonitoringService.resolve_alert(alert_id, resolution_note)
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Resolve alert error: {str(e)}')
        return jsonify(build_error_response(500, f'处理告警失败: {str(e)}')), 500
