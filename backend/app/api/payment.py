from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.subject import Subject
from app.models.user_subject import UserSubject
from app.utils.helpers import build_response, build_error_response
from app.utils.log_decorators import log_operation
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/alipay', methods=['POST'])
@jwt_required()
@log_operation('PAYMENT_ALIPAY', '支付宝支付')
def alipay_payment():
    """支付宝支付"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        course_id = data.get('course_id')
        amount = data.get('amount')
        
        if not course_id or not amount:
            return jsonify(build_error_response(400, '缺少必要参数'))
        
        # 检查课程是否存在
        subject = Subject.query.get(course_id)
        if not subject:
            return jsonify(build_error_response(404, '课程不存在'))
        
        # 检查用户是否已经订阅
        existing_subscription = UserSubject.query.filter_by(
            user_id=current_user_id,
            subject_id=course_id
        ).first()
        
        if existing_subscription:
            return jsonify(build_error_response(400, '您已经订阅了该课程'))
        
        # 生成订单号
        order_id = f"ALI_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8].upper()}"
        
        logger.info(f'[支付宝支付] 用户ID: {current_user_id}, 课程ID: {course_id}, 金额: {amount}, 订单号: {order_id}')
        
        # 模拟支付宝收款二维码URL生成
        qr_code_url = f"https://qr.alipay.com/bax{order_id[:10]}"  # 模拟支付宝收款码
        
        return jsonify(build_response(data={
            'order_id': order_id,
            'qr_code_url': qr_code_url,
            'amount': amount,
            'subject_name': subject.name
        }))
        
    except Exception as e:
        logger.error(f'[支付宝支付] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 支付失败: {str(e)}')
        return jsonify(build_error_response(500, f'支付失败: {str(e)}'))

@payment_bp.route('/wechat', methods=['POST'])
@jwt_required()
@log_operation('PAYMENT_WECHAT', '微信支付')
def wechat_payment():
    """微信支付"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        course_id = data.get('course_id')
        amount = data.get('amount')
        
        if not course_id or not amount:
            return jsonify(build_error_response(400, '缺少必要参数'))
        
        # 检查课程是否存在
        subject = Subject.query.get(course_id)
        if not subject:
            return jsonify(build_error_response(404, '课程不存在'))
        
        # 检查用户是否已经订阅
        existing_subscription = UserSubject.query.filter_by(
            user_id=current_user_id,
            subject_id=course_id
        ).first()
        
        if existing_subscription:
            return jsonify(build_error_response(400, '您已经订阅了该课程'))
        
        # 生成订单号
        order_id = f"WX_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8].upper()}"
        
        logger.info(f'[微信支付] 用户ID: {current_user_id}, 课程ID: {course_id}, 金额: {amount}, 订单号: {order_id}')
        
        # 模拟微信收款二维码URL
        qr_code_url = f"https://weixin.qq.com/qr/{order_id[:10]}"  # 模拟微信收款码
        
        return jsonify(build_response(data={
            'order_id': order_id,
            'qr_code_url': qr_code_url,
            'amount': amount,
            'subject_name': subject.name
        }))
        
    except Exception as e:
        logger.error(f'[微信支付] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 支付失败: {str(e)}')
        return jsonify(build_error_response(500, f'支付失败: {str(e)}'))

@payment_bp.route('/paypal', methods=['POST'])
@jwt_required()
@log_operation('PAYMENT_PAYPAL', 'PayPal支付')
def paypal_payment():
    """PayPal支付"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        course_id = data.get('course_id')
        amount = data.get('amount')
        
        if not course_id or not amount:
            return jsonify(build_error_response(400, '缺少必要参数'))
        
        # 检查课程是否存在
        subject = Subject.query.get(course_id)
        if not subject:
            return jsonify(build_error_response(404, '课程不存在'))
        
        # 检查用户是否已经订阅
        existing_subscription = UserSubject.query.filter_by(
            user_id=current_user_id,
            subject_id=course_id
        ).first()
        
        if existing_subscription:
            return jsonify(build_error_response(400, '您已经订阅了该课程'))
        
        # 生成订单号
        order_id = f"PP_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8].upper()}"
        
        logger.info(f'[PayPal支付] 用户ID: {current_user_id}, 课程ID: {course_id}, 金额: {amount}, 订单号: {order_id}')
        
        # 模拟PayPal支付URL生成
        payment_url = f"https://www.paypal.com/paypalme/examsphere/{amount}?order_id={order_id}"
        
        return jsonify(build_response(data={
            'order_id': order_id,
            'payment_url': payment_url,
            'amount': amount,
            'subject_name': subject.name
        }))
        
    except Exception as e:
        logger.error(f'[PayPal支付] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 支付失败: {str(e)}')
        return jsonify(build_error_response(500, f'支付失败: {str(e)}'))

@payment_bp.route('/admin', methods=['POST'])
@jwt_required()
@log_operation('PAYMENT_ADMIN', '联系管理员支付')
def admin_payment():
    """联系管理员支付"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        course_id = data.get('course_id')
        amount = data.get('amount')
        
        if not course_id or not amount:
            return jsonify(build_error_response(400, '缺少必要参数'))
        
        # 检查课程是否存在
        subject = Subject.query.get(course_id)
        if not subject:
            return jsonify(build_error_response(404, '课程不存在'))
        
        # 检查用户是否已经订阅
        existing_subscription = UserSubject.query.filter_by(
            user_id=current_user_id,
            subject_id=course_id
        ).first()
        
        if existing_subscription:
            return jsonify(build_error_response(400, '您已经订阅了该课程'))
        
        # 生成订单号
        order_id = f"ADMIN_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8].upper()}"
        
        logger.info(f'[管理员支付] 用户ID: {current_user_id}, 课程ID: {course_id}, 金额: {amount}, 订单号: {order_id}')
        
        # 这里可以将支付申请保存到数据库，供管理员处理
        # 暂时直接返回成功，模拟管理员确认
        
        return jsonify(build_response(data={
            'order_id': order_id,
            'status': 'pending',
            'message': '支付申请已提交，管理员将在24小时内处理',
            'amount': amount,
            'subject_name': subject.name
        }))
        
    except Exception as e:
        logger.error(f'[管理员支付] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 支付失败: {str(e)}')
        return jsonify(build_error_response(500, f'支付失败: {str(e)}'))

@payment_bp.route('/status/<order_id>', methods=['GET'])
@jwt_required()
def query_payment_status(order_id):
    """查询支付状态"""
    try:
        current_user_id = get_jwt_identity()
        
        logger.info(f'[查询支付状态] 用户ID: {current_user_id}, 订单号: {order_id}')
        
        # 这里应该查询真实的支付状态
        # 暂时返回模拟状态
        return jsonify(build_response(data={
            'order_id': order_id,
            'status': 'completed',
            'message': '支付成功'
        }))
        
    except Exception as e:
        logger.error(f'[查询支付状态] 用户ID: {current_user_id if "current_user_id" in locals() else "unknown"} 查询失败: {str(e)}')
        return jsonify(build_error_response(500, f'查询失败: {str(e)}'))

@payment_bp.route('/methods', methods=['GET'])
def get_payment_methods():
    """获取支付方式列表"""
    try:
        payment_methods = [
            {
                'id': 'alipay',
                'name': '支付宝',
                'icon': 'alipay',
                'available': True
            },
            {
                'id': 'wechat',
                'name': '微信支付',
                'icon': 'wechat',
                'available': True
            },
            {
                'id': 'paypal',
                'name': 'PayPal',
                'icon': 'paypal',
                'available': True
            },
            {
                'id': 'admin',
                'name': '联系管理员',
                'icon': 'admin',
                'available': True
            }
        ]
        
        return jsonify(build_response(data=payment_methods))
        
    except Exception as e:
        logger.error(f'[获取支付方式] 失败: {str(e)}')
        return jsonify(build_error_response(500, f'获取支付方式失败: {str(e)}'))
