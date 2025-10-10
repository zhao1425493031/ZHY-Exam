from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.subject import Subject
from app.models.question import Question
from app.models.exam import Exam
from app.models.exam_record import ExamRecord
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.statistics_service import StatisticsService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/statistics')

@statistics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_statistics():
    """获取仪表盘统计数据"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        # 根据用户角色返回不同的统计数据
        if user and user.role == 'admin':
            statistics = StatisticsService.get_admin_dashboard_statistics()
        else:
            statistics = StatisticsService.get_user_dashboard_statistics(current_user_id)
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Get dashboard statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取仪表盘统计失败: {str(e)}')), 500

@statistics_bp.route('/exam-data', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_exam_statistics():
    """获取考试数据统计（管理员）"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        subject_id = request.args.get('subject_id', type=int)
        
        statistics = StatisticsService.get_exam_statistics(
            start_date=start_date,
            end_date=end_date,
            subject_id=subject_id
        )
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Get exam statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取考试统计失败: {str(e)}')), 500

@statistics_bp.route('/user-behavior', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_user_behavior_statistics():
    """获取用户行为统计（管理员）"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        statistics = StatisticsService.get_user_behavior_statistics(
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Get user behavior statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取用户行为统计失败: {str(e)}')), 500

@statistics_bp.route('/question-analysis', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_question_analysis():
    """获取试题分析统计（管理员）"""
    try:
        subject_id = request.args.get('subject_id', type=int)
        question_type = request.args.get('type')
        difficulty = request.args.get('difficulty')
        
        analysis = StatisticsService.get_question_analysis(
            subject_id=subject_id,
            question_type=question_type,
            difficulty=difficulty
        )
        
        return jsonify(build_response(data=analysis))
        
    except Exception as e:
        logger.error(f'Get question analysis error: {str(e)}')
        return jsonify(build_error_response(500, f'获取试题分析失败: {str(e)}')), 500

@statistics_bp.route('/score-distribution', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_score_distribution():
    """获取成绩分布统计（管理员）"""
    try:
        exam_id = request.args.get('exam_id', type=int)
        subject_id = request.args.get('subject_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        distribution = StatisticsService.get_score_distribution(
            exam_id=exam_id,
            subject_id=subject_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify(build_response(data=distribution))
        
    except Exception as e:
        logger.error(f'Get score distribution error: {str(e)}')
        return jsonify(build_error_response(500, f'获取成绩分布失败: {str(e)}')), 500

@statistics_bp.route('/learning-progress', methods=['GET'])
@jwt_required()
def get_learning_progress_statistics():
    """获取学习进度统计"""
    try:
        current_user_id = get_jwt_identity()
        subject_id = request.args.get('subject_id', type=int)
        
        statistics = StatisticsService.get_learning_progress_statistics(
            user_id=current_user_id,
            subject_id=subject_id
        )
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Get learning progress statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取学习进度统计失败: {str(e)}')), 500

@statistics_bp.route('/performance-trends', methods=['GET'])
@jwt_required()
def get_performance_trends():
    """获取成绩趋势统计"""
    try:
        current_user_id = get_jwt_identity()
        subject_id = request.args.get('subject_id', type=int)
        days = request.args.get('days', 30, type=int)
        
        trends = StatisticsService.get_performance_trends(
            user_id=current_user_id,
            subject_id=subject_id,
            days=days
        )
        
        return jsonify(build_response(data=trends))
        
    except Exception as e:
        logger.error(f'Get performance trends error: {str(e)}')
        return jsonify(build_error_response(500, f'获取成绩趋势失败: {str(e)}')), 500

@statistics_bp.route('/subject-performance', methods=['GET'])
@jwt_required()
def get_subject_performance():
    """获取科目表现统计"""
    try:
        current_user_id = get_jwt_identity()
        
        performance = StatisticsService.get_subject_performance(current_user_id)
        
        return jsonify(build_response(data=performance))
        
    except Exception as e:
        logger.error(f'Get subject performance error: {str(e)}')
        return jsonify(build_error_response(500, f'获取科目表现失败: {str(e)}')), 500

@statistics_bp.route('/weak-areas', methods=['GET'])
@jwt_required()
def get_weak_areas():
    """获取薄弱环节分析"""
    try:
        current_user_id = get_jwt_identity()
        subject_id = request.args.get('subject_id', type=int)
        
        weak_areas = StatisticsService.get_weak_areas(
            user_id=current_user_id,
            subject_id=subject_id
        )
        
        return jsonify(build_response(data=weak_areas))
        
    except Exception as e:
        logger.error(f'Get weak areas error: {str(e)}')
        return jsonify(build_error_response(500, f'获取薄弱环节失败: {str(e)}')), 500

@statistics_bp.route('/comparison', methods=['GET'])
@jwt_required()
def get_performance_comparison():
    """获取成绩对比统计"""
    try:
        current_user_id = get_jwt_identity()
        subject_id = request.args.get('subject_id', type=int)
        
        comparison = StatisticsService.get_performance_comparison(
            user_id=current_user_id,
            subject_id=subject_id
        )
        
        return jsonify(build_response(data=comparison))
        
    except Exception as e:
        logger.error(f'Get performance comparison error: {str(e)}')
        return jsonify(build_error_response(500, f'获取成绩对比失败: {str(e)}')), 500

@statistics_bp.route('/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_statistics():
    """导出统计数据（管理员）"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        export_type = request.args.get('type', 'all')
        
        # 这里可以调用导入导出服务来生成Excel文件
        # 暂时返回统计数据的JSON格式
        statistics = StatisticsService.get_all_statistics(
            start_date=start_date,
            end_date=end_date,
            export_type=export_type
        )
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Export statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'导出统计数据失败: {str(e)}')), 500
