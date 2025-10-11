# 试题管理API
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api import questions_bp, BaseAPI
from app.models.question import Question
from app.models.subject import Subject
from app.models import db
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import QuestionSchema, PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, get_client_ip, log_operation
from app.services.question_import_export_service import QuestionImportExportService
from app.services.log_service import LogService
import traceback

# 创建试题API实例
question_api = BaseAPI(Question, QuestionSchema)

@questions_bp.route('', methods=['GET'])
@jwt_required()
def get_questions():
    """获取试题列表"""
    try:
        LogService.log_info(f"[GET_QUESTIONS] 接收到请求参数: {request.args}", 'QUESTION_MANAGEMENT')
        
        # 验证分页参数
        pagination_schema = PaginationSchema()
        pagination_data = pagination_schema.load({
            'page': request.args.get('page', 1, type=int),
            'size': request.args.get('size', 10, type=int),
            'sort': request.args.get('sort', 'id'),
            'order': request.args.get('order', 'desc')
        })
        
        # 验证搜索参数
        search_schema = SearchSchema()
        search_data = search_schema.load(request.args)
        
        LogService.log_info(f"[GET_QUESTIONS] 验证后的参数 - 分页: {pagination_data}, 搜索: {search_data}", 'QUESTION_MANAGEMENT')
        
        # 构建查询
        query = Question.query
        
        # 应用搜索过滤
        if search_data.get('keyword'):
            keyword = f"%{search_data['keyword']}%"
            query = query.filter(
                Question.title.like(keyword) |
                Question.content.like(keyword)
            )
            LogService.log_info(f"[GET_QUESTIONS] 应用关键词过滤: {search_data['keyword']}", 'QUESTION_MANAGEMENT')
        
        if search_data.get('subject_id'):
            query = query.filter(Question.subject_id == search_data['subject_id'])
            LogService.log_info(f"[GET_QUESTIONS] 应用科目过滤: {search_data['subject_id']}", 'QUESTION_MANAGEMENT')
        
        if search_data.get('type'):
            query = query.filter(Question.type == search_data['type'])
            LogService.log_info(f"[GET_QUESTIONS] 应用题型过滤: {search_data['type']}", 'QUESTION_MANAGEMENT')
        
        if search_data.get('difficulty'):
            query = query.filter(Question.difficulty == search_data['difficulty'])
            LogService.log_info(f"[GET_QUESTIONS] 应用难度过滤: {search_data['difficulty']}", 'QUESTION_MANAGEMENT')
        
        if search_data.get('status'):
            query = query.filter(Question.status == search_data['status'])
            LogService.log_info(f"[GET_QUESTIONS] 应用状态过滤: {search_data['status']}", 'QUESTION_MANAGEMENT')
        
        if search_data.get('tag'):
            # 使用JSON_CONTAINS查询标签（MySQL）
            from sqlalchemy import func
            tag = search_data['tag']
            query = query.filter(func.json_contains(Question.tags, f'"{tag}"'))
            LogService.log_info(f"[GET_QUESTIONS] 应用标签过滤: {tag}", 'QUESTION_MANAGEMENT')
        
        if search_data.get('ids'):
            # 处理特定ID查询
            ids_str = search_data['ids']
            try:
                ids_list = [int(id_str.strip()) for id_str in ids_str.split(',') if id_str.strip()]
                if ids_list:
                    query = query.filter(Question.id.in_(ids_list))
                    LogService.log_info(f"[GET_QUESTIONS] 应用ID过滤: {ids_list}", 'QUESTION_MANAGEMENT')
            except ValueError as e:
                LogService.log_error(f"[GET_QUESTIONS] ID格式错误: {ids_str}, 错误: {str(e)}", 'QUESTION_MANAGEMENT')
                return jsonify(build_error_response(400, 'ID格式错误')), 400
        
        # 应用排序
        sort_field = pagination_data.get('sort', 'id')
        order = pagination_data.get('order', 'desc')
        
        if hasattr(Question, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(Question, sort_field).desc())
            else:
                query = query.order_by(getattr(Question, sort_field).asc())
            LogService.log_info(f"[GET_QUESTIONS] 应用排序: {sort_field} {order}", 'QUESTION_MANAGEMENT')
        
        # 执行分页查询
        from app.utils.helpers import paginate_query
        pagination = paginate_query(
            query,
            page=pagination_data.get('page', 1),
            per_page=pagination_data.get('size', 10)
        )
        
        result = {
            'items': [question.to_dict() for question in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
        
        LogService.log_info(f"[GET_QUESTIONS] 查询成功，返回 {len(result['items'])} 条记录，总计 {result['total']} 条", 'QUESTION_MANAGEMENT')
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        LogService.log_error(f"[GET_QUESTIONS] 查询失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[GET_QUESTIONS] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(400, str(e))), 400

@questions_bp.route('', methods=['POST'])
@jwt_required()
@require_roles('admin')
@validate_json(QuestionSchema)
def create_question():
    """创建试题（仅管理员）"""
    try:
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[CREATE_QUESTION] 接收到数据: {data}", 'QUESTION_MANAGEMENT')
        LogService.log_info(f"[CREATE_QUESTION] 操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        
        # 验证科目是否存在
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            LogService.log_warning(f"[CREATE_QUESTION] 科目不存在: {data['subject_id']}", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 创建试题
        question = Question(
            subject_id=data['subject_id'],
            type=data['type'],
            title=data['title'],
            content=data.get('content', ''),
            options=data.get('options', []),
            answer=data['answer'],
            explanation=data.get('explanation', ''),
            difficulty=data.get('difficulty', 'medium'),
            tags=data.get('tags', []),
            points=data.get('points', 1),
            status=data.get('status', 'draft'),
            created_by=current_user_id
        )
        
        LogService.log_info(f"[CREATE_QUESTION] 创建试题对象: title={question.title[:50]}, type={question.type}, difficulty={question.difficulty}", 'QUESTION_MANAGEMENT')
        
        db.session.add(question)
        db.session.commit()
        
        LogService.log_info(f"[CREATE_QUESTION] 试题创建成功: ID={question.id}, title={question.title[:50]}", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='create_question',
            details=f'创建试题: {question.title[:50]}...',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='试题创建成功',
            data=question.to_dict()
        )), 201
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[CREATE_QUESTION] 创建试题失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[CREATE_QUESTION] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'创建试题失败: {str(e)}')), 500

@questions_bp.route('/<int:question_id>', methods=['GET'])
@jwt_required()
def get_question(question_id):
    """获取试题详情"""
    try:
        LogService.log_info(f"[GET_QUESTION] 获取试题详情，ID: {question_id}", 'QUESTION_MANAGEMENT')
        question = Question.query.get_or_404(question_id)
        LogService.log_info(f"[GET_QUESTION] 试题详情获取成功: {question.title[:50]}", 'QUESTION_MANAGEMENT')
        return jsonify(build_response(data=question.to_dict()))
    except Exception as e:
        LogService.log_error(f"[GET_QUESTION] 获取试题详情失败，ID: {question_id}, 错误: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[GET_QUESTION] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(404, str(e))), 404

@questions_bp.route('/<int:question_id>', methods=['PUT'])
@jwt_required()
@require_roles('admin')
@validate_json(QuestionSchema)
def update_question(question_id):
    """更新试题信息（仅管理员）"""
    try:
        LogService.log_info(f"[UPDATE_QUESTION] 更新试题，ID: {question_id}", 'QUESTION_MANAGEMENT')
        question = Question.query.get_or_404(question_id)
        data = request.validated_data
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[UPDATE_QUESTION] 接收到数据: {data}", 'QUESTION_MANAGEMENT')
        LogService.log_info(f"[UPDATE_QUESTION] 操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        
        # 验证科目是否存在
        if 'subject_id' in data:
            subject = Subject.query.get(data['subject_id'])
            if not subject:
                LogService.log_warning(f"[UPDATE_QUESTION] 科目不存在: {data['subject_id']}", 'QUESTION_MANAGEMENT')
                return jsonify(build_error_response(400, '科目不存在')), 400
        
        # 更新试题信息
        for key, value in data.items():
            if hasattr(question, key):
                old_value = getattr(question, key)
                setattr(question, key, value)
                LogService.log_info(f"[UPDATE_QUESTION] 更新字段 {key}: {old_value} -> {value}", 'QUESTION_MANAGEMENT')
        
        db.session.commit()
        
        LogService.log_info(f"[UPDATE_QUESTION] 试题更新成功: ID={question.id}, title={question.title[:50]}", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_question',
            details=f'更新试题: {question.title[:50]}...',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='试题更新成功',
            data=question.to_dict()
        ))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[UPDATE_QUESTION] 更新试题失败，ID: {question_id}, 错误: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[UPDATE_QUESTION] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'更新试题失败: {str(e)}')), 500

@questions_bp.route('/<int:question_id>', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def delete_question(question_id):
    """删除试题（仅管理员）"""
    try:
        LogService.log_info(f"[DELETE_QUESTION] 删除试题，ID: {question_id}", 'QUESTION_MANAGEMENT')
        question = Question.query.get_or_404(question_id)
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[DELETE_QUESTION] 操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        
        # TODO: 检查是否有考试关联此试题
        # 这里可以添加关联检查逻辑
        
        title = question.title
        LogService.log_info(f"[DELETE_QUESTION] 准备删除试题: {title[:50]}", 'QUESTION_MANAGEMENT')
        
        db.session.delete(question)
        db.session.commit()
        
        LogService.log_info(f"[DELETE_QUESTION] 试题删除成功，ID: {question_id}", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='delete_question',
            details=f'删除试题: {title[:50]}...',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='试题删除成功'))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[DELETE_QUESTION] 删除试题失败，ID: {question_id}, 错误: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[DELETE_QUESTION] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'删除试题失败: {str(e)}')), 500

@questions_bp.route('/<int:question_id>/status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def update_question_status(question_id):
    """更新试题状态（仅管理员）"""
    try:
        LogService.log_info(f"[UPDATE_QUESTION_STATUS] 更新试题状态，ID: {question_id}", 'QUESTION_MANAGEMENT')
        question = Question.query.get_or_404(question_id)
        data = request.get_json()
        status = data.get('status')
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[UPDATE_QUESTION_STATUS] 新状态: {status}, 操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        
        if status not in ['draft', 'published', 'archived']:
            LogService.log_warning(f"[UPDATE_QUESTION_STATUS] 无效的状态值: {status}", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        old_status = question.status
        question.status = status
        db.session.commit()
        
        LogService.log_info(f"[UPDATE_QUESTION_STATUS] 状态更新成功: {old_status} -> {status}", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='update_question_status',
            details=f'修改试题状态: {question.title[:30]}... ({old_status} -> {status})',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message='试题状态更新成功',
            data={'status': question.status}
        ))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[UPDATE_QUESTION_STATUS] 更新状态失败，ID: {question_id}, 错误: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[UPDATE_QUESTION_STATUS] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'更新试题状态失败: {str(e)}')), 500

@questions_bp.route('/types', methods=['GET'])
@jwt_required()
def get_question_types():
    """获取试题类型列表"""
    try:
        LogService.log_info("[GET_QUESTION_TYPES] 获取试题类型列表", 'QUESTION_MANAGEMENT')
        types = [
            {'value': 'single', 'label': '单选题'},
            {'value': 'multiple', 'label': '多选题'},
            {'value': 'judge', 'label': '判断题'},
            {'value': 'fill', 'label': '填空题'},
            {'value': 'essay', 'label': '简答题'}
        ]
        
        LogService.log_info(f"[GET_QUESTION_TYPES] 返回 {len(types)} 种题型", 'QUESTION_MANAGEMENT')
        return jsonify(build_response(data=types))
        
    except Exception as e:
        LogService.log_error(f"[GET_QUESTION_TYPES] 获取失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[GET_QUESTION_TYPES] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'获取试题类型失败: {str(e)}')), 500

@questions_bp.route('/difficulties', methods=['GET'])
@jwt_required()
def get_question_difficulties():
    """获取试题难度列表"""
    try:
        LogService.log_info("[GET_QUESTION_DIFFICULTIES] 获取试题难度列表", 'QUESTION_MANAGEMENT')
        difficulties = [
            {'value': 'easy', 'label': '简单'},
            {'value': 'medium', 'label': '中等'},
            {'value': 'hard', 'label': '困难'}
        ]
        
        LogService.log_info(f"[GET_QUESTION_DIFFICULTIES] 返回 {len(difficulties)} 种难度", 'QUESTION_MANAGEMENT')
        return jsonify(build_response(data=difficulties))
        
    except Exception as e:
        LogService.log_error(f"[GET_QUESTION_DIFFICULTIES] 获取失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[GET_QUESTION_DIFFICULTIES] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'获取试题难度失败: {str(e)}')), 500

@questions_bp.route('/stats', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_question_stats():
    """获取试题统计信息（仅管理员）"""
    try:
        LogService.log_info("[GET_QUESTION_STATS] 开始获取试题统计信息", 'QUESTION_MANAGEMENT')
        
        total_questions = Question.query.count()
        draft_questions = Question.query.filter_by(status='draft').count()
        published_questions = Question.query.filter_by(status='published').count()
        archived_questions = Question.query.filter_by(status='archived').count()
        
        # 按类型统计
        type_stats = {}
        for qtype in ['single', 'multiple', 'judge', 'fill', 'essay']:
            count = Question.query.filter_by(type=qtype).count()
            type_stats[qtype] = count
        
        # 按难度统计
        difficulty_stats = {}
        for difficulty in ['easy', 'medium', 'hard']:
            count = Question.query.filter_by(difficulty=difficulty).count()
            difficulty_stats[difficulty] = count
        
        stats = {
            'total': total_questions,
            'draft': draft_questions,
            'published': published_questions,
            'archived': archived_questions,
            'by_type': type_stats,
            'by_difficulty': difficulty_stats
        }
        
        LogService.log_info(f"[GET_QUESTION_STATS] 统计完成 - 总数: {total_questions}, 草稿: {draft_questions}, 已发布: {published_questions}", 'QUESTION_MANAGEMENT')
        
        return jsonify(build_response(data=stats))
        
    except Exception as e:
        LogService.log_error(f"[GET_QUESTION_STATS] 获取统计失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[GET_QUESTION_STATS] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'获取试题统计失败: {str(e)}')), 500
        
@questions_bp.route('/import', methods=['POST'])
@jwt_required()
@require_roles('admin')
def import_questions():
    """批量导入试题（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[IMPORT_QUESTIONS] 开始导入试题，操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        
        # 检查是否有文件上传
        if 'file' not in request.files:
            LogService.log_warning("[IMPORT_QUESTIONS] 请求中没有文件", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '请选择要导入的文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            LogService.log_warning("[IMPORT_QUESTIONS] 文件名为空", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '请选择要导入的文件')), 400
        
        LogService.log_info(f"[IMPORT_QUESTIONS] 接收到文件: {file.filename}", 'QUESTION_MANAGEMENT')
        
        # 获取科目ID
        subject_id = request.form.get('subject_id')
        if not subject_id:
            LogService.log_warning("[IMPORT_QUESTIONS] 未提供科目ID", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '请选择科目')), 400
        
        try:
            subject_id = int(subject_id)
        except ValueError:
            LogService.log_error(f"[IMPORT_QUESTIONS] 科目ID格式错误: {subject_id}", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '无效的科目ID')), 400
        
        # 验证科目是否存在
        subject = Subject.query.get(subject_id)
        if not subject:
            LogService.log_warning(f"[IMPORT_QUESTIONS] 科目不存在: {subject_id}", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '科目不存在')), 400
        
        LogService.log_info(f"[IMPORT_QUESTIONS] 开始导入到科目: {subject.name} (ID: {subject_id})", 'QUESTION_MANAGEMENT')
        
        # 执行导入
        result = QuestionImportExportService.import_questions_from_excel(
            file, subject_id, current_user_id
        )
        
        LogService.log_info(f"[IMPORT_QUESTIONS] 导入完成 - 成功: {result['success_count']}, 失败: {result.get('error_count', 0)}", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='import_questions',
            details=f'批量导入试题到科目 {subject.name}: 成功{result["success_count"]}题，失败{result.get("error_count", 0)}题',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message=f'导入完成：成功{result["success_count"]}题，失败{result.get("error_count", 0)}题',
            data=result
        ))
        
    except Exception as e:
        LogService.log_error(f"[IMPORT_QUESTIONS] 导入失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[IMPORT_QUESTIONS] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'导入试题失败: {str(e)}')), 500

@questions_bp.route('/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_questions():
    """导出试题（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        LogService.log_info("[EXPORT_QUESTIONS] 开始导出试题", 'QUESTION_MANAGEMENT')
        
        # 获取参数
        subject_id = request.args.get('subject_id', type=int)
        question_ids = request.args.get('question_ids')
        
        LogService.log_info(f"[EXPORT_QUESTIONS] 导出参数 - 科目ID: {subject_id}, 试题IDs: {question_ids}", 'QUESTION_MANAGEMENT')
        
        # 处理试题ID列表
        if question_ids:
            try:
                question_ids = [int(id) for id in question_ids.split(',')]
                LogService.log_info(f"[EXPORT_QUESTIONS] 解析试题IDs成功，共 {len(question_ids)} 个", 'QUESTION_MANAGEMENT')
            except ValueError:
                LogService.log_error(f"[EXPORT_QUESTIONS] 试题ID列表格式错误: {question_ids}", 'QUESTION_MANAGEMENT')
                return jsonify(build_error_response(400, '无效的试题ID列表')), 400
        
        # 执行导出
        file_response = QuestionImportExportService.export_questions_to_excel(
            subject_id=subject_id,
            question_ids=question_ids
        )
        
        LogService.log_info(f"[EXPORT_QUESTIONS] 导出成功", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='export_questions',
            details=f'导出试题: 科目ID={subject_id}, 试题数量={len(question_ids) if question_ids else "全部"}',
            ip=get_client_ip(request)
        )
        
        return file_response
        
    except Exception as e:
        LogService.log_error(f"[EXPORT_QUESTIONS] 导出失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[EXPORT_QUESTIONS] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'导出试题失败: {str(e)}')), 500

@questions_bp.route('/import-template', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_import_template():
    """获取导入模板（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        
        LogService.log_info(f"[GET_IMPORT_TEMPLATE] 下载导入模板，操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        
        # 生成模板文件
        file_response = QuestionImportExportService.get_import_template()
        
        LogService.log_info("[GET_IMPORT_TEMPLATE] 模板生成成功", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='download_import_template',
            details='下载试题导入模板',
            ip=get_client_ip(request)
        )
        
        return file_response
        
    except Exception as e:
        LogService.log_error(f"[GET_IMPORT_TEMPLATE] 获取模板失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[GET_IMPORT_TEMPLATE] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'获取模板失败: {str(e)}')), 500

@questions_bp.route('/batch-delete', methods=['DELETE'])
@jwt_required()
@require_roles('admin')
def batch_delete_questions():
    """批量删除试题（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        LogService.log_info(f"[BATCH_DELETE_QUESTIONS] 开始批量删除，操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        LogService.log_info(f"[BATCH_DELETE_QUESTIONS] 接收到数据: {data}", 'QUESTION_MANAGEMENT')
        
        question_ids = data.get('ids')
        if not isinstance(question_ids, list) or not question_ids:
            LogService.log_warning("[BATCH_DELETE_QUESTIONS] 未提供试题ID列表", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '请提供要删除的试题ID列表')), 400
        
        LogService.log_info(f"[BATCH_DELETE_QUESTIONS] 准备删除 {len(question_ids)} 个试题: {question_ids}", 'QUESTION_MANAGEMENT')
        
        # 检查试题是否存在
        questions = Question.query.filter(Question.id.in_(question_ids)).all()
        if len(questions) != len(question_ids):
            LogService.log_warning(f"[BATCH_DELETE_QUESTIONS] 部分试题不存在，找到 {len(questions)}/{len(question_ids)}", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '部分试题不存在')), 400
        
        # TODO: 检查是否有考试关联这些试题
        # 这里可以添加关联检查逻辑
        
        # 删除试题
        deleted_count = Question.query.filter(Question.id.in_(question_ids)).delete(synchronize_session=False)
        db.session.commit()
        
        LogService.log_info(f"[BATCH_DELETE_QUESTIONS] 批量删除成功，删除了 {deleted_count} 个试题", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='batch_delete_questions',
            details=f'批量删除试题ID: {question_ids}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message=f'成功删除 {deleted_count} 个试题'
        ))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[BATCH_DELETE_QUESTIONS] 批量删除失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[BATCH_DELETE_QUESTIONS] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'批量删除试题失败: {str(e)}')), 500

@questions_bp.route('/batch-update-status', methods=['PUT'])
@jwt_required()
@require_roles('admin')
def batch_update_question_status():
    """批量更新试题状态（仅管理员）"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        LogService.log_info(f"[BATCH_UPDATE_STATUS] 开始批量更新状态，操作用户ID: {current_user_id}", 'QUESTION_MANAGEMENT')
        LogService.log_info(f"[BATCH_UPDATE_STATUS] 接收到数据: {data}", 'QUESTION_MANAGEMENT')
        
        question_ids = data.get('ids')
        status = data.get('status')
        
        if not isinstance(question_ids, list) or not question_ids:
            LogService.log_warning("[BATCH_UPDATE_STATUS] 未提供试题ID列表", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '请提供要更新的试题ID列表')), 400
        
        if status not in ['draft', 'published', 'archived']:
            LogService.log_warning(f"[BATCH_UPDATE_STATUS] 无效的状态值: {status}", 'QUESTION_MANAGEMENT')
            return jsonify(build_error_response(400, '无效的状态值')), 400
        
        LogService.log_info(f"[BATCH_UPDATE_STATUS] 准备更新 {len(question_ids)} 个试题状态为: {status}", 'QUESTION_MANAGEMENT')
        
        # 更新试题状态
        updated_count = Question.query.filter(Question.id.in_(question_ids)).update(
            {'status': status}, synchronize_session=False
        )
        db.session.commit()
        
        LogService.log_info(f"[BATCH_UPDATE_STATUS] 批量更新成功，更新了 {updated_count} 个试题状态", 'QUESTION_MANAGEMENT')
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='batch_update_question_status',
            details=f'批量更新试题状态: {question_ids} -> {status}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(
            message=f'成功更新 {updated_count} 个试题状态'
        ))
        
    except Exception as e:
        db.session.rollback()
        LogService.log_error(f"[BATCH_UPDATE_STATUS] 批量更新失败: {str(e)}", 'QUESTION_MANAGEMENT')
        LogService.log_error(f"[BATCH_UPDATE_STATUS] 错误堆栈: {traceback.format_exc()}", 'QUESTION_MANAGEMENT')
        return jsonify(build_error_response(500, f'批量更新试题状态失败: {str(e)}')), 500
