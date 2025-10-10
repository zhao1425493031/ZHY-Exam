from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.exam_record import ExamRecord
from app.models.wrong_answer import WrongAnswer
from app.models.question import Question
from app.models.subject import Subject
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.learning_progress_service import LearningProgressService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
learning_progress_bp = Blueprint('learning_progress', __name__, url_prefix='/api/learning-progress')

@learning_progress_bp.route('/overview', methods=['GET'])
@jwt_required()
def get_learning_overview():
    """获取学习概览"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取学习概览数据
        overview = LearningProgressService.get_learning_overview(current_user_id)
        
        return jsonify(build_response(data=overview))
        
    except Exception as e:
        logger.error(f'Get learning overview error: {str(e)}')
        return jsonify(build_error_response(500, f'获取学习概览失败: {str(e)}')), 500

@learning_progress_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_learning_progress():
    """获取学习进度"""
    try:
        current_user_id = get_jwt_identity()
        subject_id = request.args.get('subject_id', type=int)
        period = request.args.get('period', '30d')  # 7d, 30d, 3m, 1y
        
        # 获取学习进度数据
        progress = LearningProgressService.get_learning_progress(
            current_user_id, 
            subject_id=subject_id, 
            period=period
        )
        
        return jsonify(build_response(data=progress))
        
    except Exception as e:
        logger.error(f'Get learning progress error: {str(e)}')
        return jsonify(build_error_response(500, f'获取学习进度失败: {str(e)}')), 500

@learning_progress_bp.route('/statistics', methods=['GET'])
@jwt_required()
def get_learning_statistics():
    """获取学习统计"""
    try:
        current_user_id = get_jwt_identity()
        subject_id = request.args.get('subject_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 获取学习统计数据
        statistics = LearningProgressService.get_learning_statistics(
            current_user_id,
            subject_id=subject_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Get learning statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取学习统计失败: {str(e)}')), 500

@learning_progress_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    """获取学习成就"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取学习成就
        achievements = LearningProgressService.get_achievements(current_user_id)
        
        return jsonify(build_response(data=achievements))
        
    except Exception as e:
        logger.error(f'Get achievements error: {str(e)}')
        return jsonify(build_error_response(500, f'获取学习成就失败: {str(e)}')), 500

@learning_progress_bp.route('/report', methods=['GET'])
@jwt_required()
def generate_learning_report():
    """生成学习报告"""
    try:
        current_user_id = get_jwt_identity()
        period = request.args.get('period', 'month')  # week, month, quarter, year
        subject_id = request.args.get('subject_id', type=int)
        
        # 生成学习报告
        report = LearningProgressService.generate_learning_report(
            current_user_id,
            period=period,
            subject_id=subject_id
        )
        
        return jsonify(build_response(data=report))
        
    except Exception as e:
        logger.error(f'Generate learning report error: {str(e)}')
        return jsonify(build_error_response(500, f'生成学习报告失败: {str(e)}')), 500

@learning_progress_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_learning_recommendations():
    """获取学习建议"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取学习建议
        recommendations = LearningProgressService.get_learning_recommendations(current_user_id)
        
        return jsonify(build_response(data=recommendations))
        
    except Exception as e:
        logger.error(f'Get learning recommendations error: {str(e)}')
        return jsonify(build_error_response(500, f'获取学习建议失败: {str(e)}')), 500

@learning_progress_bp.route('/goals', methods=['GET'])
@jwt_required()
def get_learning_goals():
    """获取学习目标"""
    try:
        current_user_id = get_jwt_identity()
        
        # 获取学习目标
        goals = LearningProgressService.get_learning_goals(current_user_id)
        
        return jsonify(build_response(data=goals))
        
    except Exception as e:
        logger.error(f'Get learning goals error: {str(e)}')
        return jsonify(build_error_response(500, f'获取学习目标失败: {str(e)}')), 500

@learning_progress_bp.route('/goals', methods=['POST'])
@jwt_required()
def create_learning_goal():
    """创建学习目标"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        required_fields = ['title', 'subject_id', 'target_score', 'target_date']
        for field in required_fields:
            if field not in data:
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 创建学习目标
        goal = LearningProgressService.create_learning_goal(current_user_id, data)
        
        return jsonify(build_response(data=goal))
        
    except Exception as e:
        logger.error(f'Create learning goal error: {str(e)}')
        return jsonify(build_error_response(500, f'创建学习目标失败: {str(e)}')), 500

@learning_progress_bp.route('/goals/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_learning_goal(goal_id):
    """更新学习目标"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 更新学习目标
        goal = LearningProgressService.update_learning_goal(goal_id, current_user_id, data)
        
        return jsonify(build_response(data=goal))
        
    except Exception as e:
        logger.error(f'Update learning goal error: {str(e)}')
        return jsonify(build_error_response(500, f'更新学习目标失败: {str(e)}')), 500

@learning_progress_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_learning_goal(goal_id):
    """删除学习目标"""
    try:
        current_user_id = get_jwt_identity()
        
        # 删除学习目标
        LearningProgressService.delete_learning_goal(goal_id, current_user_id)
        
        return jsonify(build_response(data={'message': '学习目标删除成功'}))
        
    except Exception as e:
        logger.error(f'Delete learning goal error: {str(e)}')
        return jsonify(build_error_response(500, f'删除学习目标失败: {str(e)}')), 500
