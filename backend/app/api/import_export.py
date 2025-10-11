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
import logging
import io
import pandas as pd

logger = logging.getLogger(__name__)

# 创建蓝图
import_export_bp = Blueprint('import_export', __name__, url_prefix='/api/import-export')

@import_export_bp.route('/users/import', methods=['POST'])
@jwt_required()
@require_roles('admin')
def import_users():
    """导入用户数据（管理员）"""
    try:
        if 'file' not in request.files:
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        # 验证文件类型
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify(build_error_response(400, '只支持Excel文件')), 400
        
        # 导入用户数据
        result = ImportExportService.import_users(file)
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
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
        if 'file' not in request.files:
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(build_error_response(400, '没有选择文件')), 400
        
        # 验证文件类型
        if not file.filename.endswith(('.xlsx', '.xls')):
            return jsonify(build_error_response(400, '只支持Excel文件')), 400
        
        # 获取参数
        subject_id = request.form.get('subject_id')
        if not subject_id:
            return jsonify(build_error_response(400, '请选择科目')), 400
        
        # 导入试题数据
        result = ImportExportService.import_questions(file, int(subject_id))
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
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
