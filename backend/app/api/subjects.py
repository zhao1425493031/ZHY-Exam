# 科目管理API
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import subjects_bp, BaseAPI
from app.models.subject import Subject
from app.models import db
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import SubjectSchema, PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation
from app.services.log_service import LogService
import traceback

# 创建科目API实例
subject_api = BaseAPI(Subject, SubjectSchema)

@subjects_bp.route('', methods=['GET'])
def get_subjects():
    """获取科目列表"""
    try:
        LogService.log_info(f"[GET_SUBJECTS] 接收到请求参数: {request.args}", 'SUBJECT_MANAGEMENT')
        
        # 验证所有参数（包括分页和搜索参数）
        search_schema = SearchSchema()
        all_data = search_schema.load(request.args)
        
        LogService.log_info(f"[GET_SUBJECTS] 验证后的参数: {all_data}", 'SUBJECT_MANAGEMENT')
        
        # 构建查询
        query = Subject.query
        
        # 应用搜索过滤
        if all_data.get('keyword'):
            keyword = f"%{all_data['keyword']}%"
            query = query.filter(
                Subject.name.like(keyword) |
                Subject.code.like(keyword) |
                Subject.description.like(keyword)
            )
            LogService.log_info(f"[GET_SUBJECTS] 应用关键词过滤: {all_data['keyword']}", 'SUBJECT_MANAGEMENT')
        
        if all_data.get('status'):
            query = query.filter(Subject.status == all_data['status'])
            LogService.log_info(f"[GET_SUBJECTS] 应用状态过滤: {all_data['status']}", 'SUBJECT_MANAGEMENT')
        
        if all_data.get('category'):
            query = query.filter(Subject.category == all_data['category'])
            LogService.log_info(f"[GET_SUBJECTS] 应用分类过滤: {all_data['category']}", 'SUBJECT_MANAGEMENT')
        
        # 应用排序
        sort_field = all_data.get('sort', 'id')
        order = all_data.get('order', 'desc')
        
        if hasattr(Subject, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(Subject, sort_field).desc())
            else:
                query = query.order_by(getattr(Subject, sort_field).asc())
            LogService.log_info(f"[GET_SUBJECTS] 应用排序: {sort_field} {order}", 'SUBJECT_MANAGEMENT')
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=all_data.get('page', 1),
            per_page=all_data.get('size', 10)
        )
        
        result = {
            'items': [subject.to_dict() for subject in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
        
        LogService.log_info(f"[GET_SUBJECTS] 查询成功，返回 {len(result['items'])} 条记录，总计 {result['total']} 条", 'SUBJECT_MANAGEMENT')
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        LogService.log_error(f"[GET_SUBJECTS] 查询失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[GET_SUBJECTS] 错误类型: {type(e).__name__}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[GET_SUBJECTS] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(400, str(e))), 400

@subjects_bp.route('', methods=['POST'])
@jwt_required()
@require_roles('admin')
@validate_json(SubjectSchema)
def create_subject():
    """创建科目（仅管理员）"""
    try:
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[CREATE_SUBJECT] 接收到数据: {data}", 'SUBJECT_MANAGEMENT')
        LogService.log_info(f"[CREATE_SUBJECT] 操作用户ID: {current_user_id}", 'SUBJECT_MANAGEMENT')
        
        # 检查科目代码是否已存在
        existing_subject = Subject.query.filter_by(code=data['code']).first()
        if existing_subject:
            LogService.log_warning(f"[CREATE_SUBJECT] 科目代码已存在: {data['code']}", 'SUBJECT_MANAGEMENT')
            return jsonify(build_error_response(400, '科目代码已存在')), 400
        
        # 创建科目
        subject = Subject(
            name=data['name'],
            code=data['code'],
            description=data.get('description', ''),
            category=data.get('category', ''),
            status=data.get('status', 'active'),
            is_free=data.get('is_free', True),
            price=data.get('price', 0.00),
            original_price=data.get('original_price', 0.00),
            discount_rate=data.get('discount_rate', 100.00),
            created_by=current_user_id
        )
        
        LogService.log_info(f"[CREATE_SUBJECT] 创建科目对象: name={subject.name}, code={subject.code}, status={subject.status}", 'SUBJECT_MANAGEMENT')
        
        db.session.add(subject)
        db.session.commit()
        
        LogService.log_info(f"[CREATE_SUBJECT] 科目创建成功: ID={subject.id}, name={subject.name}, code={subject.code}", 'SUBJECT_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='create_subject',
            details=f'创建科目: {subject.name} ({subject.code})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='科目创建成功',
            data=subject.to_dict()
        )), 201
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[CREATE_SUBJECT] 创建科目失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[CREATE_SUBJECT] 错误类型: {type(e).__name__}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[CREATE_SUBJECT] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(500, f'创建科目失败: {str(e)}')), 500

@subjects_bp.route('/<int:subject_id>', methods=['GET'])
@jwt_required()
def get_subject(subject_id):
    """获取科目详情"""
    try:
        LogService.log_info(f"[GET_SUBJECT] 获取科目详情: ID={subject_id}", 'SUBJECT_MANAGEMENT')
        
        subject = Subject.query.get_or_404(subject_id)
        
        LogService.log_info(f"[GET_SUBJECT] 科目详情获取成功: name={subject.name}, code={subject.code}", 'SUBJECT_MANAGEMENT')
        
        return jsonify(build_response(data=subject.to_dict()))
    except Exception as e:
        LogService.log_error(f"[GET_SUBJECT] 获取科目详情失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[GET_SUBJECT] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(404, str(e))), 404

@subjects_bp.route('/<int:subject_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
@validate_json(SubjectSchema)
def update_subject(subject_id):
    """更新科目信息（仅管理员）"""
    try:
        subject = Subject.query.get_or_404(subject_id)
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[UPDATE_SUBJECT] 更新科目: ID={subject_id}, 数据={data}", 'SUBJECT_MANAGEMENT')
        LogService.log_info(f"[UPDATE_SUBJECT] 操作用户ID: {current_user_id}", 'SUBJECT_MANAGEMENT')
        
        # 检查科目代码是否已被其他科目使用
        if 'code' in data and data['code'] != subject.code:
            existing_subject = Subject.query.filter_by(code=data['code']).first()
            if existing_subject:
                LogService.log_warning(f"[UPDATE_SUBJECT] 科目代码已存在: {data['code']}", 'SUBJECT_MANAGEMENT')
                return jsonify(build_error_response(400, '科目代码已存在')), 400
        
        # 更新科目信息
        for key, value in data.items():
            if hasattr(subject, key):
                setattr(subject, key, value)
                LogService.log_info(f"[UPDATE_SUBJECT] 更新字段: {key} = {value}", 'SUBJECT_MANAGEMENT')
        
        db.session.commit()
        
        LogService.log_info(f"[UPDATE_SUBJECT] 科目更新成功: ID={subject.id}, name={subject.name}, code={subject.code}", 'SUBJECT_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_subject',
            details=f'更新科目: {subject.name} ({subject.code})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='科目更新成功',
            data=subject.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[UPDATE_SUBJECT] 更新科目失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[UPDATE_SUBJECT] 错误类型: {type(e).__name__}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[UPDATE_SUBJECT] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(500, f'更新科目失败: {str(e)}')), 500

@subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_subject(subject_id):
    """删除科目（仅管理员）"""
    try:
        subject = Subject.query.get_or_404(subject_id)
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[DELETE_SUBJECT] 删除科目: ID={subject_id}, name={subject.name}, code={subject.code}", 'SUBJECT_MANAGEMENT')
        LogService.log_info(f"[DELETE_SUBJECT] 操作用户ID: {current_user_id}", 'SUBJECT_MANAGEMENT')
        
        # TODO: 检查是否有试题或考试关联此科目
        # 这里可以添加关联检查逻辑
        
        name = subject.name
        code = subject.code
        db.session.delete(subject)
        db.session.commit()
        
        LogService.log_info(f"[DELETE_SUBJECT] 科目删除成功: name={name}, code={code}", 'SUBJECT_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='delete_subject',
            details=f'删除科目: {name} ({code})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='科目删除成功'))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[DELETE_SUBJECT] 删除科目失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[DELETE_SUBJECT] 错误类型: {type(e).__name__}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[DELETE_SUBJECT] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(500, f'删除科目失败: {str(e)}')), 500

@subjects_bp.route('/<int:subject_id>/status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_subject_status(subject_id):
    """更新科目状态（仅管理员）"""
    try:
        subject = Subject.query.get_or_404(subject_id)
        data = request.get_json()
        status = data.get('status')
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[UPDATE_SUBJECT_STATUS] 更新科目状态: ID={subject_id}, 状态={status}", 'SUBJECT_MANAGEMENT')
        LogService.log_info(f"[UPDATE_SUBJECT_STATUS] 操作用户ID: {current_user_id}", 'SUBJECT_MANAGEMENT')
        
        if status not in ['active', 'inactive']:
            LogService.log_warning(f"[UPDATE_SUBJECT_STATUS] 无效的状态值: {status}", 'SUBJECT_MANAGEMENT')
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        old_status = subject.status
        subject.status = status
        db.session.commit()
        
        LogService.log_info(f"[UPDATE_SUBJECT_STATUS] 科目状态更新成功: {subject.name} ({old_status} -> {status})", 'SUBJECT_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_subject_status',
            details=f'修改科目状态: {subject.name} ({old_status} -> {status})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='科目状态更新成功',
            data={'status': subject.status}
        ))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[UPDATE_SUBJECT_STATUS] 更新科目状态失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[UPDATE_SUBJECT_STATUS] 错误类型: {type(e).__name__}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[UPDATE_SUBJECT_STATUS] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(500, f'更新科目状态失败: {str(e)}')), 500

@subjects_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """获取科目分类列表"""
    try:
        LogService.log_info("[GET_CATEGORIES] 获取科目分类列表", 'SUBJECT_MANAGEMENT')
        
        categories = db.session.query(Subject.category).filter(
            Subject.category.isnot(None),
            Subject.category != ''
        ).distinct().all()
        
        category_list = [cat[0] for cat in categories if cat[0]]
        
        LogService.log_info(f"[GET_CATEGORIES] 获取到 {len(category_list)} 个分类: {category_list}", 'SUBJECT_MANAGEMENT')
        
        return jsonify(build_response(data=category_list))
        
    except Exception as e:
        LogService.log_error(f"[GET_CATEGORIES] 获取科目分类失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[GET_CATEGORIES] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(500, f'获取科目分类失败: {str(e)}')), 500

@subjects_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_subject_stats():
    """获取科目统计信息（仅管理员）"""
    try:
        LogService.log_info("[GET_SUBJECT_STATS] 获取科目统计信息", 'SUBJECT_MANAGEMENT')
        
        total_subjects = Subject.query.count()
        active_subjects = Subject.query.filter_by(status='active').count()
        inactive_subjects = Subject.query.filter_by(status='inactive').count()
        
        # 获取分类统计
        categories = db.session.query(Subject.category).filter(
            Subject.category.isnot(None),
            Subject.category != ''
        ).distinct().count()
        
        stats = {
            'total': total_subjects,
            'active': active_subjects,
            'inactive': inactive_subjects,
            'categories': categories
        }
        
        LogService.log_info(f"[GET_SUBJECT_STATS] 统计信息: {stats}", 'SUBJECT_MANAGEMENT')
        
        return jsonify(build_response(data=stats))
        
    except Exception as e:
        LogService.log_error(f"[GET_SUBJECT_STATS] 获取科目统计失败: {str(e)}", 'SUBJECT_MANAGEMENT')
        LogService.log_error(f"[GET_SUBJECT_STATS] 错误堆栈: {traceback.format_exc()}", 'SUBJECT_MANAGEMENT')
        return jsonify(build_error_response(500, f'获取科目统计失败: {str(e)}')), 500



