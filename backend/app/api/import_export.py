from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.subject import Subject
from app.models.question import Question
from app.models.exam import Exam
from app.models.exam_record import ExamRecord
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.import_export_service import ImportExportService
from app.services.log_service import LogService
import logging
import io
import pandas as pd
import traceback

logger = logging.getLogger(__name__)

# 创建蓝图
import_export_bp = Blueprint('import_export', __name__, url_prefix='/api/import-export')

@import_export_bp.route('/users/import', methods=['POST'])
@jwt_required()
@require_roles('admin')
def import_users():
    """导入用户数据（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        LogService.log_info(f"[IMPORT_USERS] 开始导入用户数据，操作用户ID: {current_user_id}", 'IMPORT_EXPORT')
        LogService.log_info(f"[IMPORT_USERS] 请求文件信息: {request.files}", 'IMPORT_EXPORT')
        
        if 'file' not in request.files:
            LogService.log_warning("[IMPORT_USERS] 请求中没有找到文件", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            LogService.log_warning("[IMPORT_USERS] 文件名为空", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        LogService.log_info(f"[IMPORT_USERS] 接收到文件: {file.filename}, 文件大小: {file.content_length}", 'IMPORT_EXPORT')
        
        # 验证文件类型
        if not file.filename.endswith(('.xlsx', '.xls')):
            LogService.log_warning(f"[IMPORT_USERS] 不支持的文件类型: {file.filename}", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '只支持Excel文件')), 400
        
        # 导入用户数据
        LogService.log_info("[IMPORT_USERS] 开始调用ImportExportService.import_users", 'IMPORT_EXPORT')
        result = ImportExportService.import_users(file)
        LogService.log_info(f"[IMPORT_USERS] 导入完成，结果: {result}", 'IMPORT_EXPORT')
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        LogService.log_error(f"[IMPORT_USERS] 导入用户数据失败: {str(e)}", 'IMPORT_EXPORT')
        LogService.log_error(f"[IMPORT_USERS] 错误类型: {type(e).__name__}", 'IMPORT_EXPORT')
        LogService.log_error(f"[IMPORT_USERS] 错误堆栈: {traceback.format_exc()}", 'IMPORT_EXPORT')
        logger.error(f'Import users error: {str(e)}')
        return jsonify(build_error_response(500, f'导入用户数据失败: {str(e)}')), 500

@import_export_bp.route('/subjects/import', methods=['POST'])
@jwt_required()
@require_roles('admin')
def import_subjects():
    """导入科目数据（管理员）"""
    try:
        if 'file' not in request.files:
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        # 验证文件类型
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify(build_error_response(400, '只支持Excel文件')), 400
        
        # 导入科目数据
        result = ImportExportService.import_subjects(file)
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Import subjects error: {str(e)}')
        return jsonify(build_error_response(500, f'导入科目数据失败: {str(e)}')), 500

@import_export_bp.route('/questions/import', methods=['POST'])
@jwt_required()
@require_roles('admin')
def import_questions():
    """导入试题数据（管理员）"""
    try:
        current_user_id = get_jwt_identity()
        LogService.log_info(f"[IMPORT_QUESTIONS] 开始导入试题数据，操作用户ID: {current_user_id}", 'IMPORT_EXPORT')
        LogService.log_info(f"[IMPORT_QUESTIONS] 请求文件信息: {request.files}", 'IMPORT_EXPORT')
        LogService.log_info(f"[IMPORT_QUESTIONS] 请求表单数据: {request.form}", 'IMPORT_EXPORT')
        
        if 'file' not in request.files:
            LogService.log_warning("[IMPORT_QUESTIONS] 请求中没有找到文件", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            LogService.log_warning("[IMPORT_QUESTIONS] 文件名为空", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        LogService.log_info(f"[IMPORT_QUESTIONS] 接收到文件: {file.filename}, 文件大小: {file.content_length}", 'IMPORT_EXPORT')
        
        # 验证文件类型
        if not file.filename.endswith(('.xlsx', '.xls')):
            LogService.log_warning(f"[IMPORT_QUESTIONS] 不支持的文件类型: {file.filename}", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '只支持Excel文件')), 400
        
        # 获取参数
        subject_id = request.form.get('subject_id')
        LogService.log_info(f"[IMPORT_QUESTIONS] 获取到的subject_id: {subject_id}, 类型: {type(subject_id)}", 'IMPORT_EXPORT')
        
        if not subject_id:
            LogService.log_warning("[IMPORT_QUESTIONS] 没有提供subject_id", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '请选择科目')), 400
        
        try:
            subject_id_int = int(subject_id)
            LogService.log_info(f"[IMPORT_QUESTIONS] 转换后的subject_id: {subject_id_int}", 'IMPORT_EXPORT')
        except ValueError as ve:
            LogService.log_error(f"[IMPORT_QUESTIONS] subject_id转换失败: {str(ve)}, 原始值: {subject_id}", 'IMPORT_EXPORT')
            return jsonify(build_error_response(400, '科目ID格式错误')), 400
        
        # 导入试题数据
        LogService.log_info(f"[IMPORT_QUESTIONS] 开始调用ImportExportService.import_questions，参数: file={file.filename}, subject_id={subject_id_int}", 'IMPORT_EXPORT')
        result = ImportExportService.import_questions(file, subject_id_int)
        LogService.log_info(f"[IMPORT_QUESTIONS] 导入完成，结果: {result}", 'IMPORT_EXPORT')
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        LogService.log_error(f"[IMPORT_QUESTIONS] 导入试题数据失败: {str(e)}", 'IMPORT_EXPORT')
        LogService.log_error(f"[IMPORT_QUESTIONS] 错误类型: {type(e).__name__}", 'IMPORT_EXPORT')
        LogService.log_error(f"[IMPORT_QUESTIONS] 错误堆栈: {traceback.format_exc()}", 'IMPORT_EXPORT')
        logger.error(f'Import questions error: {str(e)}')
        return jsonify(build_error_response(500, f'导入试题数据失败: {str(e)}')), 500

@import_export_bp.route('/users/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_users():
    """导出用户数据（管理员）"""
    try:
        # 获取查询参数
        role = request.args.get('role')
        status = request.args.get('status')
        
        # 导出用户数据（美化版）
        output = ImportExportService.export_users_styled(role=role, status=status)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='用户数据.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Export users error: {str(e)}')
        return jsonify(build_error_response(500, f'导出用户数据失败: {str(e)}')), 500

@import_export_bp.route('/subjects/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_subjects():
    """导出科目数据（管理员）"""
    try:
        # 获取查询参数
        status = request.args.get('status')
        
        # 导出科目数据（美化版）
        output = ImportExportService.export_subjects_styled(status=status)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='科目数据.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Export subjects error: {str(e)}')
        return jsonify(build_error_response(500, f'导出科目数据失败: {str(e)}')), 500

@import_export_bp.route('/questions/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_questions():
    """导出试题数据（管理员）"""
    try:
        # 获取查询参数
        subject_id = request.args.get('subject_id', type=int)
        question_type = request.args.get('type')
        difficulty = request.args.get('difficulty')
        
        # 导出试题数据（美化版）
        output = ImportExportService.export_questions_styled(
            subject_id=subject_id,
            question_type=question_type,
            difficulty=difficulty
        )
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='试题数据.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Export questions error: {str(e)}')
        return jsonify(build_error_response(500, f'导出试题数据失败: {str(e)}')), 500

@import_export_bp.route('/exams/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_exams():
    """导出考试数据（管理员）"""
    try:
        LogService.log_info("[EXPORT_EXAMS] 开始导出考试数据", 'IMPORT_EXPORT')
        
        # 获取查询参数
        keyword = request.args.get('keyword')
        subject_id = request.args.get('subject_id', type=int)
        status = request.args.get('status')
        
        LogService.log_info(f"[EXPORT_EXAMS] 查询参数 - keyword: {keyword}, subject_id: {subject_id}, status: {status}", 'IMPORT_EXPORT')
        
        # 导出考试数据（美化版）
        output = ImportExportService.export_exams_styled(
            keyword=keyword,
            subject_id=subject_id,
            status=status
        )
        
        LogService.log_info("[EXPORT_EXAMS] 考试数据导出成功", 'IMPORT_EXPORT')
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='考试数据.xlsx'
        )
        
    except Exception as e:
        LogService.log_error(f"[EXPORT_EXAMS] 导出考试数据失败: {str(e)}", 'IMPORT_EXPORT')
        LogService.log_error(f"[EXPORT_EXAMS] 错误堆栈: {traceback.format_exc()}", 'IMPORT_EXPORT')
        logger.error(f'Export exams error: {str(e)}')
        return jsonify(build_error_response(500, f'导出考试数据失败: {str(e)}')), 500

@import_export_bp.route('/exam-results/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_exam_results():
    """导出考试结果数据（管理员）"""
    try:
        # 获取查询参数
        exam_id = request.args.get('exam_id', type=int)
        user_id = request.args.get('user_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 导出考试结果数据（美化版）
        output = ImportExportService.export_exam_results_styled(
            exam_id=exam_id,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='考试结果.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Export exam results error: {str(e)}')
        return jsonify(build_error_response(500, f'导出考试结果失败: {str(e)}')), 500

@import_export_bp.route('/statistics/export', methods=['GET'])
@jwt_required()
@require_roles('admin')
def export_statistics():
    """导出统计数据（管理员）"""
    try:
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 导出统计数据
        excel_data = ImportExportService.export_statistics(
            start_date=start_date,
            end_date=end_date
        )
        
        # 创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for sheet_name, data in excel_data.items():
                data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='统计数据.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Export statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'导出统计数据失败: {str(e)}')), 500

@import_export_bp.route('/templates/users', methods=['GET'])
def download_user_template():
    """下载用户导入模板"""
    try:
        # 创建用户导入模板
        template_data = ImportExportService.create_user_template()
        
        # 创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            template_data.to_excel(writer, sheet_name='用户模板', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='用户导入模板.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Download user template error: {str(e)}')
        return jsonify(build_error_response(500, f'下载用户模板失败: {str(e)}')), 500

@import_export_bp.route('/templates/subjects', methods=['GET'])
def download_subject_template():
    """下载科目导入模板"""
    try:
        # 创建科目导入模板
        template_data = ImportExportService.create_subject_template()
        
        # 创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            template_data.to_excel(writer, sheet_name='科目模板', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='科目导入模板.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Download subject template error: {str(e)}')
        return jsonify(build_error_response(500, f'下载科目模板失败: {str(e)}')), 500

@import_export_bp.route('/templates/questions', methods=['GET'])
def download_question_template():
    """下载试题导入模板"""
    try:
        # 创建试题导入模板
        template_data = ImportExportService.create_question_template()
        
        # 创建Excel文件
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            template_data.to_excel(writer, sheet_name='试题模板', index=False)
        
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='试题导入模板.xlsx'
        )
        
    except Exception as e:
        logger.error(f'Download question template error: {str(e)}')
        return jsonify(build_error_response(500, f'下载试题模板失败: {str(e)}')), 500

@import_export_bp.route('/records', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_import_records():
    """获取导入记录（管理员）"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        import_type = request.args.get('type')
        
        # 获取导入记录
        records = ImportExportService.get_import_records(
            page=page,
            size=size,
            import_type=import_type
        )
        
        return jsonify(build_response(data=records))
        
    except Exception as e:
        logger.error(f'Get import records error: {str(e)}')
        return jsonify(build_error_response(500, f'获取导入记录失败: {str(e)}')), 500
