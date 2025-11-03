from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user_subject import UserSubject
from app.models.subject import Subject
from app.models.user import User
from app.utils.helpers import build_response, build_error_response, paginate_query, get_client_ip, log_operation
from app.utils.decorators import require_roles
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

# ==================== 管理员接口 ====================

@user_subjects_bp.route('/admin', methods=['GET'])
@jwt_required()
@require_roles('admin')
def admin_get_user_subjects():
    """管理员获取所有用户课程关联列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        user_id = request.args.get('user_id', type=int)
        subject_id = request.args.get('subject_id', type=int)
        status = request.args.get('status')
        
        logger.info(f'[管理员] 获取用户课程关联列表, page={page}, per_page={per_page}, user_id={user_id}, subject_id={subject_id}, status={status}')
        
        # 构建查询
        query = db.session.query(UserSubject)
        
        # 应用过滤条件
        if user_id:
            query = query.filter(UserSubject.user_id == user_id)
        if subject_id:
            query = query.filter(UserSubject.subject_id == subject_id)
        if status:
            query = query.filter(UserSubject.status == status)
        
        # 排序
        query = query.order_by(UserSubject.created_at.desc())
        
        # 分页
        pagination = paginate_query(query, page=page, per_page=per_page)
        
        # 获取关联的用户和科目信息
        user_ids = list(set([us.user_id for us in pagination.items]))
        subject_ids = list(set([us.subject_id for us in pagination.items]))
        
        users = {u.id: u for u in User.query.filter(User.id.in_(user_ids)).all()} if user_ids else {}
        subjects = {s.id: s for s in Subject.query.filter(Subject.id.in_(subject_ids)).all()} if subject_ids else {}
        
        # 构建响应数据
        items = []
        for us in pagination.items:
            user = users.get(us.user_id)
            subject = subjects.get(us.subject_id)
            if user and subject:
                items.append({
                    'id': us.id,
                    'user_id': user.id,
                    'username': user.username,
                    'real_name': user.real_name,
                    'user_email': user.email,
                    'subject_id': subject.id,
                    'subject_name': subject.name,
                    'subject_code': subject.code,
                    'is_free': us.is_free,
                    'status': us.status,
                    'purchased_at': us.purchased_at.isoformat() if us.purchased_at else None,
                    'expires_at': us.expires_at.isoformat() if us.expires_at else None,
                    'created_at': us.created_at.isoformat() if us.created_at else None,
                    'updated_at': us.updated_at.isoformat() if us.updated_at else None
                })
        
        logger.info(f'[管理员] 获取到 {len(items)} 个用户课程关联')
        return jsonify(build_response(data={
            'items': items,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }))
        
    except Exception as e:
        logger.error(f'[管理员] 获取用户课程关联列表失败: {str(e)}', exc_info=True)
        return jsonify(build_error_response(500, f'获取用户课程关联列表失败: {str(e)}')), 500

@user_subjects_bp.route('/admin', methods=['POST'])
@jwt_required()
@require_roles('admin')
def admin_create_user_subject():
    """管理员创建用户课程关联"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        user_id = data.get('user_id')
        subject_id = data.get('subject_id')
        status = data.get('status', 'pending')
        
        if not user_id or not subject_id:
            return jsonify(build_error_response(400, '缺少用户ID或科目ID')), 400
        
        # 验证状态值
        if status not in ['pending', 'approved', 'rejected', 'active', 'expired', 'cancelled']:
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        logger.info(f'[管理员] 创建用户课程关联: user_id={user_id}, subject_id={subject_id}, status={status}')
        
        # 验证用户是否存在
        user = User.query.get(user_id)
        if not user:
            return jsonify(build_error_response(404, '用户不存在')), 404
        
        # 验证科目是否存在
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify(build_error_response(404, '科目不存在')), 404
        
        # 根据课程的is_free自动设置关联类型（前端传的值可能不准确，以课程为准）
        is_free = subject.is_free
        
        # 检查是否已存在关联
        existing = UserSubject.query.filter_by(user_id=user_id, subject_id=subject_id).first()
        if existing:
            # 如果已存在，更新状态和关联类型
            existing.status = status
            existing.is_free = is_free
            db.session.commit()
            logger.info(f'[管理员] 已存在的关联已更新: status={status}')
            return jsonify(build_response(message='关联已更新'))
        
        # 创建新的关联
        user_subject = UserSubject(
            user_id=user_id,
            subject_id=subject_id,
            is_free=is_free,
            status=status
        )
        db.session.add(user_subject)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='admin_create_user_subject',
            details=f'管理员创建用户课程关联: 用户={user.username}, 课程={subject.name}',
            ip=get_client_ip(request)
        )
        
        logger.info(f'[管理员] 用户课程关联创建成功')
        return jsonify(build_response(
            message='用户课程关联创建成功',
            data={
                'id': user_subject.id,
                'user_id': user_id,
                'subject_id': subject_id,
                'username': user.username,
                'subject_name': subject.name
            }
        ))
        
    except Exception as e:
        logger.error(f'[管理员] 创建用户课程关联失败: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify(build_error_response(500, f'创建用户课程关联失败: {str(e)}')), 500

@user_subjects_bp.route('/admin/<int:user_subject_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def admin_delete_user_subject(user_subject_id):
    """管理员删除用户课程关联"""
    try:
        current_user_id = get_jwt_identity()
        user_subject = UserSubject.query.get_or_404(user_subject_id)
        
        logger.info(f'[管理员] 删除用户课程关联: {user_subject_id}')
        
        # 获取关联的用户和科目信息用于日志
        user = User.query.get(user_subject.user_id)
        subject = Subject.query.get(user_subject.subject_id)
        
        db.session.delete(user_subject)
        db.session.commit()
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='admin_delete_user_subject',
            details=f'管理员删除用户课程关联: 用户={user.username if user else "未知"}, 课程={subject.name if subject else "未知"}',
            ip=get_client_ip(request)
        )
        
        logger.info(f'[管理员] 用户课程关联删除成功')
        return jsonify(build_response(message='用户课程关联删除成功'))
        
    except Exception as e:
        logger.error(f'[管理员] 删除用户课程关联失败: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify(build_error_response(500, f'删除用户课程关联失败: {str(e)}')), 500

@user_subjects_bp.route('/admin/<int:user_subject_id>/status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def admin_update_user_subject_status(user_subject_id):
    """管理员更新用户课程关联状态"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['active', 'expired', 'cancelled', 'pending', 'approved', 'rejected']:
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        user_subject = UserSubject.query.get_or_404(user_subject_id)
        old_status = user_subject.status
        
        logger.info(f'[管理员] 更新用户课程关联状态: {user_subject_id}, {old_status} -> {status}')
        
        user_subject.status = status
        db.session.commit()
        
        # 获取关联的用户和科目信息用于日志
        user = User.query.get(user_subject.user_id)
        subject = Subject.query.get(user_subject.subject_id)
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='admin_update_user_subject_status',
            details=f'管理员更新用户课程关联状态: 用户={user.username if user else "未知"}, 课程={subject.name if subject else "未知"}, {old_status} -> {status}',
            ip=get_client_ip(request)
        )
        
        logger.info(f'[管理员] 用户课程关联状态更新成功')
        return jsonify(build_response(
            message='状态更新成功',
            data={'status': status}
        ))
        
    except Exception as e:
        logger.error(f'[管理员] 更新用户课程关联状态失败: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify(build_error_response(500, f'更新状态失败: {str(e)}')), 500
