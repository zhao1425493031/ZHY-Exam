from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_subject import UserSubject
from app.models.subject import Subject
from app.utils.helpers import build_response, build_error_response
from app import db
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
user_subjects_bp = Blueprint('user_subjects', __name__, url_prefix='/api/user-subjects')

@user_subjects_bp.route('', methods=['GET'])
@jwt_required()
def get_user_subjects():
    """获取用户订阅的科目列表"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        logger.info(f'[用户科目] 用户ID: {current_user_id} 获取订阅科目列表, page={page}, size={size}')
        
        # 获取用户订阅的科目
        user_subjects = db.session.query(UserSubject).filter_by(
            user_id=current_user_id,
            status='active'
        ).offset((page - 1) * size).limit(size).all()
        
        # 获取科目详细信息
        subject_ids = [us.subject_id for us in user_subjects]
        subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
        
        # 构建响应数据
        subject_dict = {s.id: s for s in subjects}
        items = []
        for us in user_subjects:
            subject = subject_dict.get(us.subject_id)
            if subject:
                items.append({
                    'id': us.id,
                    'subject_id': subject.id,
                    'subject_name': subject.name,
                    'subject_code': subject.code,
                    'description': subject.description,
                    'is_free': us.is_free,
                    'purchased_at': us.purchased_at.isoformat() if us.purchased_at else None,
                    'expires_at': us.expires_at.isoformat() if us.expires_at else None,
                    'subscribed_at': us.created_at.isoformat() if us.created_at else None
                })
        
        logger.info(f'[用户科目] 用户ID: {current_user_id} 获取到 {len(items)} 个订阅科目')
        return jsonify(build_response(data={
            'items': items,
            'total': len(items),
            'page': page,
            'size': size
        }))
        
    except Exception as e:
        logger.error(f'[用户科目] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 获取订阅科目失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'获取订阅科目失败: {str(e)}')), 500

@user_subjects_bp.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe_subject():
    """用户订阅科目"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        subject_id = data.get('subject_id')
        
        if not subject_id:
            logger.warning(f'[用户科目] 用户ID: {current_user_id} 订阅科目缺少subject_id参数')
            return jsonify(build_error_response(400, '缺少科目ID')), 400
        
        logger.info(f'[用户科目] 用户ID: {current_user_id} 开始订阅科目 {subject_id}')
        
        # 检查科目是否存在
        subject = Subject.query.get(subject_id)
        if not subject:
            logger.warning(f'[用户科目] 用户ID: {current_user_id} 科目 {subject_id} 不存在')
            return jsonify(build_error_response(404, '科目不存在')), 404
        
        # 检查科目状态
        if subject.status != 'active':
            logger.warning(f'[用户科目] 用户ID: {current_user_id} 科目 {subject.name} 状态不可用')
            return jsonify(build_error_response(400, '科目不可用')), 400
        
        # 订阅科目
        user_subject, result = UserSubject.subscribe_subject(
            current_user_id, 
            subject_id, 
            is_free=subject.is_free
        )
        
        if result == 'new_subscription':
            db.session.add(user_subject)
            logger.info(f'[用户科目] 用户ID: {current_user_id} 新订阅科目 {subject.name}')
        elif result == 'reactivated':
            logger.info(f'[用户科目] 用户ID: {current_user_id} 重新激活科目订阅 {subject.name}')
        else:
            logger.info(f'[用户科目] 用户ID: {current_user_id} 科目 {subject.name} 已订阅')
        
        db.session.commit()
        
        return jsonify(build_response(
            message='订阅成功' if result != 'already_subscribed' else '科目已订阅',
            data={
                'subject_id': subject_id,
                'subject_name': subject.name,
                'is_free': subject.is_free,
                'status': result
            }
        ))
        
    except Exception as e:
        logger.error(f'[用户科目] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 订阅科目失败: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify(build_error_response(500, f'订阅科目失败: {str(e)}')), 500

@user_subjects_bp.route('/unsubscribe', methods=['POST'])
@jwt_required()
def unsubscribe_subject():
    """用户取消订阅科目"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        subject_id = data.get('subject_id')
        
        if not subject_id:
            logger.warning(f'[用户科目] 用户ID: {current_user_id} 取消订阅缺少subject_id参数')
            return jsonify(build_error_response(400, '缺少科目ID')), 400
        
        logger.info(f'[用户科目] 用户ID: {current_user_id} 开始取消订阅科目 {subject_id}')
        
        # 取消订阅
        user_subject, result = UserSubject.unsubscribe_subject(current_user_id, subject_id)
        
        if result == 'not_found':
            logger.warning(f'[用户科目] 用户ID: {current_user_id} 科目 {subject_id} 未订阅')
            return jsonify(build_error_response(404, '科目未订阅')), 404
        
        db.session.commit()
        logger.info(f'[用户科目] 用户ID: {current_user_id} 取消订阅科目 {subject_id} 成功')
        
        return jsonify(build_response(message='取消订阅成功'))
        
    except Exception as e:
        logger.error(f'[用户科目] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 取消订阅科目失败: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify(build_error_response(500, f'取消订阅科目失败: {str(e)}')), 500

@user_subjects_bp.route('/check/<int:subject_id>', methods=['GET'])
@jwt_required()
def check_subscription(subject_id):
    """检查用户是否已订阅指定科目"""
    try:
        current_user_id = get_jwt_identity()
        logger.info(f'[用户科目] 用户ID: {current_user_id} 检查科目 {subject_id} 订阅状态')
        
        is_subscribed = UserSubject.is_user_subscribed(current_user_id, subject_id)
        
        return jsonify(build_response(data={
            'subject_id': subject_id,
            'is_subscribed': is_subscribed
        }))
        
    except Exception as e:
        logger.error(f'[用户科目] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 检查订阅状态失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'检查订阅状态失败: {str(e)}')), 500
