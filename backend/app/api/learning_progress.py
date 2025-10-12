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
from app import db
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
        logger.info(f'[学习概览] 用户ID: {current_user_id} 开始获取学习概览')
        
        # 获取学习概览数据
        overview = LearningProgressService.get_learning_overview(current_user_id)
        logger.info(f'[学习概览] 用户ID: {current_user_id} 获取学习概览成功')
        
        return jsonify(build_response(data=overview))
        
    except Exception as e:
        logger.error(f'[学习概览] 用户ID: {current_user_id} 获取学习概览失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'获取学习概览失败: {str(e)}')), 500

@learning_progress_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_learning_progress():
    """获取学习进度"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        logger.info(f'[学习进度] 用户ID: {current_user_id} 开始获取学习进度, page={page}, size={size}')
        
        # 简化的学习进度数据，避免复杂查询
        progress_items = []
        
        try:
            # 获取所有活跃科目
            logger.info(f'[学习进度] 用户ID: {current_user_id} 开始查询活跃科目')
            subjects = Subject.query.filter_by(status='active').limit(size).all()
            logger.info(f'[学习进度] 用户ID: {current_user_id} 查询到 {len(subjects)} 个活跃科目')
            
            # 为每个科目创建基础进度数据
            for subject in subjects:
                logger.info(f'[学习进度] 用户ID: {current_user_id} 处理科目: {subject.name} (ID: {subject.id})')
                
                # 简化的进度计算
                progress_item = {
                    'id': subject.id,
                    'subject_name': subject.name,
                    'completed_questions': 0,  # 暂时设为0，避免复杂查询
                    'total_questions': 100,    # 默认值
                    'percentage': 0.0          # 默认进度
                }
                progress_items.append(progress_item)
                logger.info(f'[学习进度] 用户ID: {current_user_id} 科目 {subject.name} 基础进度数据创建完成')
                
        except Exception as query_error:
            logger.error(f'[学习进度] 用户ID: {current_user_id} 查询科目失败: {str(query_error)}', exc_info=True)
            # 如果查询失败，返回空数据
            progress_items = []
        
        logger.info(f'[学习进度] 用户ID: {current_user_id} 成功处理 {len(progress_items)} 个科目的学习进度')
        return jsonify(build_response(data={
            'items': progress_items,
            'total': len(progress_items),
            'page': page,
            'size': size
        }))
        
    except Exception as e:
        logger.error(f'[学习进度] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 获取学习进度失败: {str(e)}', exc_info=True)
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
        logger.info(f'[学习统计] 用户ID: {current_user_id} 开始获取学习统计, subject_id={subject_id}, start_date={start_date}, end_date={end_date}')
        
        # 获取学习统计数据
        statistics = LearningProgressService.get_learning_statistics(
            current_user_id,
            subject_id=subject_id,
            start_date=start_date,
            end_date=end_date
        )
        logger.info(f'[学习统计] 用户ID: {current_user_id} 获取学习统计成功')
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'[学习统计] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 获取学习统计失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'获取学习统计失败: {str(e)}')), 500

@learning_progress_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    """获取学习成就"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f'[学习成就] 用户ID: {current_user_id} 开始获取学习成就')
        
        # 获取学习成就
        achievements = LearningProgressService.get_achievements(current_user_id)
        logger.info(f'[学习成就] 用户ID: {current_user_id} 获取学习成就成功')
        
        return jsonify(build_response(data=achievements))
        
    except Exception as e:
        logger.error(f'[学习成就] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 获取学习成就失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'获取学习成就失败: {str(e)}')), 500

@learning_progress_bp.route('/report', methods=['GET'])
@jwt_required()
def generate_learning_report():
    """生成学习报告"""
    try:
        current_user_id = get_jwt_identity()
        period = request.args.get('period', 'month')  # week, month, quarter, year
        subject_id = request.args.get('subject_id', type=int)
        logger.info(f'[学习报告] 用户ID: {current_user_id} 开始生成学习报告, period={period}, subject_id={subject_id}')
        
        # 生成学习报告
        report = LearningProgressService.generate_learning_report(
            current_user_id,
            period=period,
            subject_id=subject_id
        )
        logger.info(f'[学习报告] 用户ID: {current_user_id} 生成学习报告成功')
        
        return jsonify(build_response(data=report))
        
    except Exception as e:
        logger.error(f'[学习报告] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 生成学习报告失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'生成学习报告失败: {str(e)}')), 500

@learning_progress_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_learning_recommendations():
    """获取学习建议"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f'[学习建议] 用户ID: {current_user_id} 开始获取学习建议')
        
        # 获取学习建议
        recommendations = LearningProgressService.get_learning_recommendations(current_user_id)
        logger.info(f'[学习建议] 用户ID: {current_user_id} 获取学习建议成功')
        
        return jsonify(build_response(data=recommendations))
        
    except Exception as e:
        logger.error(f'[学习建议] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 获取学习建议失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'获取学习建议失败: {str(e)}')), 500

@learning_progress_bp.route('/goals', methods=['GET'])
@jwt_required()
def get_learning_goals():
    """获取学习目标"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f'[学习目标] 用户ID: {current_user_id} 开始获取学习目标')
        
        # 获取学习目标
        goals = LearningProgressService.get_learning_goals(current_user_id)
        logger.info(f'[学习目标] 用户ID: {current_user_id} 获取学习目标成功')
        
        return jsonify(build_response(data=goals))
        
    except Exception as e:
        logger.error(f'[学习目标] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 获取学习目标失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'获取学习目标失败: {str(e)}')), 500

@learning_progress_bp.route('/goals', methods=['POST'])
@jwt_required()
def create_learning_goal():
    """创建学习目标"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        logger.info(f'[创建学习目标] 用户ID: {current_user_id} 开始创建学习目标, data={data}')
        
        # 验证必要参数
        required_fields = ['title', 'subject_id', 'target_score', 'target_date']
        for field in required_fields:
            if field not in data:
                logger.warning(f'[创建学习目标] 用户ID: {current_user_id} 缺少必要参数: {field}')
                return jsonify(build_error_response(400, f'缺少必要参数: {field}')), 400
        
        # 创建学习目标
        goal = LearningProgressService.create_learning_goal(current_user_id, data)
        logger.info(f'[创建学习目标] 用户ID: {current_user_id} 创建学习目标成功')
        
        return jsonify(build_response(data=goal))
        
    except Exception as e:
        logger.error(f'[创建学习目标] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 创建学习目标失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'创建学习目标失败: {str(e)}')), 500

@learning_progress_bp.route('/goals/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_learning_goal(goal_id):
    """更新学习目标"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        logger.info(f'[更新学习目标] 用户ID: {current_user_id} 开始更新学习目标 {goal_id}, data={data}')
        
        # 更新学习目标
        goal = LearningProgressService.update_learning_goal(goal_id, current_user_id, data)
        logger.info(f'[更新学习目标] 用户ID: {current_user_id} 更新学习目标 {goal_id} 成功')
        
        return jsonify(build_response(data=goal))
        
    except Exception as e:
        logger.error(f'[更新学习目标] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 更新学习目标 {goal_id} 失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'更新学习目标失败: {str(e)}')), 500

@learning_progress_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_learning_goal(goal_id):
    """删除学习目标"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f'[删除学习目标] 用户ID: {current_user_id} 开始删除学习目标 {goal_id}')
        
        # 删除学习目标
        LearningProgressService.delete_learning_goal(goal_id, current_user_id)
        logger.info(f'[删除学习目标] 用户ID: {current_user_id} 删除学习目标 {goal_id} 成功')
        
        return jsonify(build_response(data={'message': '学习目标删除成功'}))
        
    except Exception as e:
        logger.error(f'[删除学习目标] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 删除学习目标 {goal_id} 失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'删除学习目标失败: {str(e)}')), 500
