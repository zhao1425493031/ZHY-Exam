from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.exam_record import ExamRecord
from app.models.exam import Exam
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response
from app.services.exam_scoring_service import ExamScoringService
import logging

logger = logging.getLogger(__name__)

# 创建蓝图
exam_scoring_bp = Blueprint('exam_scoring', __name__, url_prefix='/api/exam-scoring')

@exam_scoring_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_exam():
    """提交考试"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # 验证必要参数
        if 'exam_record_id' not in data:
            return jsonify(build_error_response(400, '缺少必要参数: exam_record_id')), 400
        
        exam_record_id = data['exam_record_id']
        answers = data.get('answers', [])
        
        # 验证考试记录权限
        exam_record = ExamRecord.query.get(exam_record_id)
        if not exam_record:
            return jsonify(build_error_response(404, '考试记录不存在')), 404
        
        if exam_record.user_id != current_user_id:
            return jsonify(build_error_response(403, '无权限访问此考试记录')), 403
        
        if exam_record.status != 'in_progress':
            return jsonify(build_error_response(400, '考试状态不允许提交')), 400
        
        # 计算分数
        result = ExamScoringService.calculate_score(exam_record_id, answers)
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Submit exam error: {str(e)}')
        return jsonify(build_error_response(500, f'提交考试失败: {str(e)}')), 500

@exam_scoring_bp.route('/result/<int:exam_record_id>', methods=['GET'])
@jwt_required()
def get_exam_result(exam_record_id):
    """获取考试结果"""
    try:
        current_user_id = get_jwt_identity()
        
        # 验证考试记录权限
        exam_record = ExamRecord.query.get(exam_record_id)
        if not exam_record:
            return jsonify(build_error_response(404, '考试记录不存在')), 404
        
        if exam_record.user_id != current_user_id:
            return jsonify(build_error_response(403, '无权限访问此考试记录')), 403
        
        if exam_record.status != 'submitted':
            return jsonify(build_error_response(400, '考试尚未提交')), 400
        
        # 获取考试结果
        result = ExamScoringService.get_exam_result(exam_record_id)
        
        return jsonify(build_response(data=result))
        
    except Exception as e:
        logger.error(f'Get exam result error: {str(e)}')
        return jsonify(build_error_response(500, f'获取考试结果失败: {str(e)}')), 500

@exam_scoring_bp.route('/statistics/<int:exam_id>', methods=['GET'])
@jwt_required()
@require_roles('admin')
def get_exam_statistics(exam_id):
    """获取考试统计信息（管理员）"""
    try:
        # 验证考试是否存在
        exam = Exam.query.get(exam_id)
        if not exam:
            return jsonify(build_error_response(404, '考试不存在')), 404
        
        # 获取统计信息
        statistics = ExamScoringService.get_exam_statistics(exam_id)
        
        return jsonify(build_response(data=statistics))
        
    except Exception as e:
        logger.error(f'Get exam statistics error: {str(e)}')
        return jsonify(build_error_response(500, f'获取考试统计失败: {str(e)}')), 500

@exam_scoring_bp.route('/records', methods=['GET'])
@jwt_required()
def get_exam_records():
    """获取用户的考试记录"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        exam_id = request.args.get('exam_id', type=int)
        
        # 构建查询
        query = ExamRecord.query.filter_by(user_id=current_user_id)
        
        if exam_id:
            query = query.filter_by(exam_id=exam_id)
        
        # 分页
        pagination = query.order_by(ExamRecord.created_at.desc())\
            .paginate(page=page, per_page=size, error_out=False)
        
        records = []
        for record in pagination.items:
            exam = Exam.query.get(record.exam_id)
            records.append({
                'id': record.id,
                'exam_id': record.exam_id,
                'exam_title': exam.title if exam else '未知考试',
                'score': record.score,
                'status': record.status,
                'start_time': record.start_time.isoformat() if record.start_time else None,
                'submit_time': record.submit_time.isoformat() if record.submit_time else None,
                'created_at': record.created_at.isoformat()
            })
        
        return jsonify(build_response(data={
            'items': records,
            'total': pagination.total,
            'page': page,
            'size': size,
            'pages': pagination.pages
        }))
        
    except Exception as e:
        logger.error(f'Get exam records error: {str(e)}')
        return jsonify(build_error_response(500, f'获取考试记录失败: {str(e)}')), 500

@exam_scoring_bp.route('/wrong-answers', methods=['GET'])
@jwt_required()
def get_wrong_answers():
    """获取用户的错题记录"""
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        subject_id = request.args.get('subject_id', type=int)
        
        from app.models.wrong_answer import WrongAnswer
        from app.models.question import Question
        
        # 构建查询
        query = WrongAnswer.query.filter_by(user_id=current_user_id)
        
        if subject_id:
            query = query.join(Question).filter(Question.subject_id == subject_id)
        
        # 分页
        pagination = query.order_by(WrongAnswer.created_at.desc())\
            .paginate(page=page, per_page=size, error_out=False)
        
        wrong_answers = []
        for wrong_answer in pagination.items:
            question = Question.query.get(wrong_answer.question_id)
            exam_record = ExamRecord.query.get(wrong_answer.exam_record_id)
            exam = Exam.query.get(exam_record.exam_id) if exam_record else None
            
            wrong_answers.append({
                'id': wrong_answer.id,
                'question_id': wrong_answer.question_id,
                'question_title': question.title if question else '未知题目',
                'question_type': question.type if question else 'unknown',
                'user_answer': wrong_answer.user_answer,
                'correct_answer': wrong_answer.correct_answer,
                'explanation': question.explanation if question else '',
                'exam_id': exam.id if exam else None,
                'exam_title': exam.title if exam else '未知考试',
                'created_at': wrong_answer.created_at.isoformat()
            })
        
        return jsonify(build_response(data={
            'items': wrong_answers,
            'total': pagination.total,
            'page': page,
            'size': size,
            'pages': pagination.pages
        }))
        
    except Exception as e:
        logger.error(f'Get wrong answers error: {str(e)}')
        return jsonify(build_error_response(500, f'获取错题记录失败: {str(e)}')), 500

@exam_scoring_bp.route('/wrong-answers/<int:wrong_answer_id>/review', methods=['POST'])
@jwt_required()
def review_wrong_answer(wrong_answer_id):
    """标记错题为已复习"""
    try:
        current_user_id = get_jwt_identity()
        
        from app.models.wrong_answer import WrongAnswer
        
        # 验证错题记录权限
        wrong_answer = WrongAnswer.query.get(wrong_answer_id)
        if not wrong_answer:
            return jsonify(build_error_response(404, '错题记录不存在')), 404
        
        if wrong_answer.user_id != current_user_id:
            return jsonify(build_error_response(403, '无权限访问此错题记录')), 403
        
        # 标记为已复习
        wrong_answer.is_reviewed = True
        wrong_answer.reviewed_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify(build_response(data={'message': '标记复习成功'}))
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Review wrong answer error: {str(e)}')
        return jsonify(build_error_response(500, f'标记复习失败: {str(e)}')), 500
