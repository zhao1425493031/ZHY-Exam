from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd
import io
import logging
from app.models.user import User
from app.models.subject import Subject
from app.models.question import Question
from app.models.exam import Exam
from app.models.exam_record import ExamRecord
from app.models.import_record import ImportRecord
from app import db
from werkzeug.security import generate_password_hash

logger = logging.getLogger(__name__)

class ImportExportService:
    """导入导出服务"""
    
    @staticmethod
    def import_users(file) -> Dict[str, Any]:
        """导入用户数据"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file)
            
            # 验证列名
            required_columns = ['username', 'email', 'password', 'real_name', 'role']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise Exception(f'缺少必要列: {", ".join(missing_columns)}')
            
            # 验证数据
            errors = []
            success_count = 0
            
            for index, row in df.iterrows():
                try:
                    # 验证用户名
                    username = str(row['username']).strip()
                    if not username:
                        errors.append(f'第{index+2}行: 用户名不能为空')
                        continue
                    
                    # 检查用户名是否已存在
                    existing_user = User.query.filter_by(username=username).first()
                    if existing_user:
                        errors.append(f'第{index+2}行: 用户名"{username}"已存在')
                        continue
                    
                    # 验证邮箱
                    email = str(row['email']).strip()
                    if not email:
                        errors.append(f'第{index+2}行: 邮箱不能为空')
                        continue
                    
                    # 检查邮箱是否已存在
                    existing_email = User.query.filter_by(email=email).first()
                    if existing_email:
                        errors.append(f'第{index+2}行: 邮箱"{email}"已存在')
                        continue
                    
                    # 验证角色
                    role = str(row['role']).strip().lower()
                    if role not in ['admin', 'user']:
                        errors.append(f'第{index+2}行: 角色必须是admin或user')
                        continue
                    
                    # 创建用户
                    user = User(
                        username=username,
                        email=email,
                        password_hash=generate_password_hash(str(row['password'])),
                        real_name=str(row['real_name']).strip() if pd.notna(row['real_name']) else '',
                        role=role
                    )
                    
                    db.session.add(user)
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f'第{index+2}行: {str(e)}')
                    continue
            
            # 提交事务
            db.session.commit()
            
            # 记录导入记录
            import_record = ImportRecord(
                import_type='users',
                total_count=len(df),
                success_count=success_count,
                error_count=len(errors),
                error_details='; '.join(errors) if errors else None
            )
            db.session.add(import_record)
            db.session.commit()
            
            return {
                'total_count': len(df),
                'success_count': success_count,
                'error_count': len(errors),
                'errors': errors
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Import users error: {str(e)}')
            raise Exception(f'导入用户数据失败: {str(e)}')
    
    @staticmethod
    def import_subjects(file) -> Dict[str, Any]:
        """导入科目数据"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file)
            
            # 验证列名
            required_columns = ['name', 'code', 'description']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise Exception(f'缺少必要列: {", ".join(missing_columns)}')
            
            # 验证数据
            errors = []
            success_count = 0
            
            for index, row in df.iterrows():
                try:
                    # 验证科目名称
                    name = str(row['name']).strip()
                    if not name:
                        errors.append(f'第{index+2}行: 科目名称不能为空')
                        continue
                    
                    # 验证科目代码
                    code = str(row['code']).strip()
                    if not code:
                        errors.append(f'第{index+2}行: 科目代码不能为空')
                        continue
                    
                    # 检查科目代码是否已存在
                    existing_subject = Subject.query.filter_by(code=code).first()
                    if existing_subject:
                        errors.append(f'第{index+2}行: 科目代码"{code}"已存在')
                        continue
                    
                    # 创建科目
                    subject = Subject(
                        name=name,
                        code=code,
                        description=str(row['description']).strip() if pd.notna(row['description']) else '',
                        category=str(row.get('category', '')).strip() if pd.notna(row.get('category')) else '',
                        is_free=bool(row.get('is_free', True)),
                        price=float(row.get('price', 0)) if pd.notna(row.get('price')) else 0
                    )
                    
                    db.session.add(subject)
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f'第{index+2}行: {str(e)}')
                    continue
            
            # 提交事务
            db.session.commit()
            
            # 记录导入记录
            import_record = ImportRecord(
                import_type='subjects',
                total_count=len(df),
                success_count=success_count,
                error_count=len(errors),
                error_details='; '.join(errors) if errors else None
            )
            db.session.add(import_record)
            db.session.commit()
            
            return {
                'total_count': len(df),
                'success_count': success_count,
                'error_count': len(errors),
                'errors': errors
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Import subjects error: {str(e)}')
            raise Exception(f'导入科目数据失败: {str(e)}')
    
    @staticmethod
    def import_questions(file, subject_id: int) -> Dict[str, Any]:
        """导入试题数据"""
        try:
            # 验证科目是否存在
            subject = Subject.query.get(subject_id)
            if not subject:
                raise Exception('科目不存在')
            
            # 读取Excel文件
            df = pd.read_excel(file)
            
            # 验证列名
            required_columns = ['type', 'title', 'answer']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise Exception(f'缺少必要列: {", ".join(missing_columns)}')
            
            # 验证数据
            errors = []
            success_count = 0
            
            for index, row in df.iterrows():
                try:
                    # 验证题型
                    question_type = str(row['type']).strip().lower()
                    if question_type not in ['single', 'multiple', 'judge', 'fill', 'essay']:
                        errors.append(f'第{index+2}行: 题型必须是single、multiple、judge、fill或essay')
                        continue
                    
                    # 验证题目
                    title = str(row['title']).strip()
                    if not title:
                        errors.append(f'第{index+2}行: 题目不能为空')
                        continue
                    
                    # 验证答案
                    answer = str(row['answer']).strip()
                    if not answer:
                        errors.append(f'第{index+2}行: 答案不能为空')
                        continue
                    
                    # 处理选项（如果是选择题）
                    options = None
                    if question_type in ['single', 'multiple']:
                        options_list = []
                        for i in range(1, 7):  # 最多6个选项
                            option_key = f'option_{i}'
                            if option_key in df.columns and pd.notna(row[option_key]):
                                options_list.append(str(row[option_key]).strip())
                        if options_list:
                            options = options_list
                    
                    # 创建试题
                    question = Question(
                        subject_id=subject_id,
                        type=question_type,
                        title=title,
                        content=str(row.get('content', '')).strip() if pd.notna(row.get('content')) else '',
                        options=options,
                        answer=answer,
                        explanation=str(row.get('explanation', '')).strip() if pd.notna(row.get('explanation')) else '',
                        difficulty=str(row.get('difficulty', 'medium')).strip().lower(),
                        points=int(row.get('points', 1)) if pd.notna(row.get('points')) else 1
                    )
                    
                    db.session.add(question)
                    success_count += 1
                    
                except Exception as e:
                    errors.append(f'第{index+2}行: {str(e)}')
                    continue
            
            # 提交事务
            db.session.commit()
            
            # 记录导入记录
            import_record = ImportRecord(
                import_type='questions',
                total_count=len(df),
                success_count=success_count,
                error_count=len(errors),
                error_details='; '.join(errors) if errors else None
            )
            db.session.add(import_record)
            db.session.commit()
            
            return {
                'total_count': len(df),
                'success_count': success_count,
                'error_count': len(errors),
                'errors': errors
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f'Import questions error: {str(e)}')
            raise Exception(f'导入试题数据失败: {str(e)}')
    
    @staticmethod
    def export_users(role: Optional[str] = None, status: Optional[str] = None) -> pd.DataFrame:
        """导出用户数据"""
        try:
            query = User.query
            
            if role:
                query = query.filter(User.role == role)
            
            if status:
                query = query.filter(User.status == status)
            
            users = query.all()
            
            # 构建DataFrame
            data = []
            for user in users:
                data.append({
                    'ID': user.id,
                    '用户名': user.username,
                    '邮箱': user.email,
                    '真实姓名': user.real_name,
                    '角色': user.role,
                    '状态': user.status,
                    '创建时间': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else ''
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f'Export users error: {str(e)}')
            raise Exception(f'导出用户数据失败: {str(e)}')
    
    @staticmethod
    def export_subjects(status: Optional[str] = None) -> pd.DataFrame:
        """导出科目数据"""
        try:
            query = Subject.query
            
            if status:
                query = query.filter(Subject.status == status)
            
            subjects = query.all()
            
            # 构建DataFrame
            data = []
            for subject in subjects:
                data.append({
                    'ID': subject.id,
                    '科目名称': subject.name,
                    '科目代码': subject.code,
                    '描述': subject.description,
                    '分类': subject.category,
                    '是否免费': '是' if subject.is_free else '否',
                    '价格': subject.price,
                    '状态': subject.status,
                    '创建时间': subject.created_at.strftime('%Y-%m-%d %H:%M:%S') if subject.created_at else ''
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f'Export subjects error: {str(e)}')
            raise Exception(f'导出科目数据失败: {str(e)}')
    
    @staticmethod
    def export_questions(subject_id: Optional[int] = None, question_type: Optional[str] = None, 
                        difficulty: Optional[str] = None) -> pd.DataFrame:
        """导出试题数据"""
        try:
            query = Question.query
            
            if subject_id:
                query = query.filter(Question.subject_id == subject_id)
            
            if question_type:
                query = query.filter(Question.type == question_type)
            
            if difficulty:
                query = query.filter(Question.difficulty == difficulty)
            
            questions = query.all()
            
            # 构建DataFrame
            data = []
            for question in questions:
                data.append({
                    'ID': question.id,
                    '科目ID': question.subject_id,
                    '题型': question.type,
                    '题目': question.title,
                    '内容': question.content,
                    '选项': str(question.options) if question.options else '',
                    '答案': question.answer,
                    '解析': question.explanation,
                    '难度': question.difficulty,
                    '分值': question.points,
                    '状态': question.status,
                    '创建时间': question.created_at.strftime('%Y-%m-%d %H:%M:%S') if question.created_at else ''
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f'Export questions error: {str(e)}')
            raise Exception(f'导出试题数据失败: {str(e)}')
    
    @staticmethod
    def export_exam_results(exam_id: Optional[int] = None, user_id: Optional[int] = None,
                          start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        """导出考试结果数据"""
        try:
            query = ExamRecord.query
            
            if exam_id:
                query = query.filter(ExamRecord.exam_id == exam_id)
            
            if user_id:
                query = query.filter(ExamRecord.user_id == user_id)
            
            if start_date:
                query = query.filter(ExamRecord.created_at >= datetime.fromisoformat(start_date))
            
            if end_date:
                query = query.filter(ExamRecord.created_at <= datetime.fromisoformat(end_date))
            
            exam_records = query.all()
            
            # 构建DataFrame
            data = []
            for record in exam_records:
                data.append({
                    'ID': record.id,
                    '考试ID': record.exam_id,
                    '用户ID': record.user_id,
                    '开始时间': record.start_time.strftime('%Y-%m-%d %H:%M:%S') if record.start_time else '',
                    '提交时间': record.submit_time.strftime('%Y-%m-%d %H:%M:%S') if record.submit_time else '',
                    '分数': record.score,
                    '状态': record.status,
                    '创建时间': record.created_at.strftime('%Y-%m-%d %H:%M:%S') if record.created_at else ''
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f'Export exam results error: {str(e)}')
            raise Exception(f'导出考试结果失败: {str(e)}')
    
    @staticmethod
    def export_statistics(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """导出统计数据"""
        try:
            # 基础查询条件
            base_query = db.session.query
            
            if start_date:
                start_dt = datetime.fromisoformat(start_date)
            else:
                start_dt = datetime.now() - timedelta(days=30)
            
            if end_date:
                end_dt = datetime.fromisoformat(end_date)
            else:
                end_dt = datetime.now()
            
            # 用户统计
            user_stats = pd.DataFrame([{
                '总用户数': User.query.count(),
                '管理员数': User.query.filter(User.role == 'admin').count(),
                '普通用户数': User.query.filter(User.role == 'user').count(),
                '活跃用户数': User.query.filter(User.status == 'active').count()
            }])
            
            # 科目统计
            subject_stats = pd.DataFrame([{
                '总科目数': Subject.query.count(),
                '活跃科目数': Subject.query.filter(Subject.status == 'active').count(),
                '免费科目数': Subject.query.filter(Subject.is_free == True).count(),
                '收费科目数': Subject.query.filter(Subject.is_free == False).count()
            }])
            
            # 试题统计
            question_stats = pd.DataFrame([{
                '总试题数': Question.query.count(),
                '单选题数': Question.query.filter(Question.type == 'single').count(),
                '多选题数': Question.query.filter(Question.type == 'multiple').count(),
                '判断题数': Question.query.filter(Question.type == 'judge').count(),
                '填空题数': Question.query.filter(Question.type == 'fill').count(),
                '简答题数': Question.query.filter(Question.type == 'essay').count()
            }])
            
            # 考试统计
            exam_stats = pd.DataFrame([{
                '总考试数': Exam.query.count(),
                '已发布考试数': Exam.query.filter(Exam.status == 'published').count(),
                '进行中考试数': Exam.query.filter(Exam.status == 'ongoing').count(),
                '已完成考试数': Exam.query.filter(Exam.status == 'finished').count()
            }])
            
            return {
                '用户统计': user_stats,
                '科目统计': subject_stats,
                '试题统计': question_stats,
                '考试统计': exam_stats
            }
            
        except Exception as e:
            logger.error(f'Export statistics error: {str(e)}')
            raise Exception(f'导出统计数据失败: {str(e)}')
    
    @staticmethod
    def create_user_template() -> pd.DataFrame:
        """创建用户导入模板"""
        return pd.DataFrame({
            'username': ['示例用户名'],
            'email': ['example@email.com'],
            'password': ['123456'],
            'real_name': ['真实姓名'],
            'role': ['user'],
            'phone': ['手机号码（可选）']
        })
    
    @staticmethod
    def create_subject_template() -> pd.DataFrame:
        """创建科目导入模板"""
        return pd.DataFrame({
            'name': ['示例科目'],
            'code': ['SUBJECT001'],
            'description': ['科目描述'],
            'category': ['分类（可选）'],
            'is_free': [True],
            'price': [0.00]
        })
    
    @staticmethod
    def create_question_template() -> pd.DataFrame:
        """创建试题导入模板"""
        return pd.DataFrame({
            'type': ['single'],
            'title': ['示例题目'],
            'content': ['题目内容（可选）'],
            'option_1': ['选项A'],
            'option_2': ['选项B'],
            'option_3': ['选项C'],
            'option_4': ['选项D'],
            'answer': ['A'],
            'explanation': ['解析（可选）'],
            'difficulty': ['medium'],
            'points': [1]
        })
    
    @staticmethod
    def get_import_records(page: int = 1, size: int = 10, import_type: Optional[str] = None) -> Dict[str, Any]:
        """获取导入记录"""
        try:
            query = ImportRecord.query
            
            if import_type:
                query = query.filter(ImportRecord.import_type == import_type)
            
            pagination = query.order_by(ImportRecord.created_at.desc()).paginate(
                page=page,
                per_page=size,
                error_out=False
            )
            
            return {
                'items': [record.to_dict() for record in pagination.items],
                'total': pagination.total,
                'page': page,
                'size': size,
                'pages': pagination.pages
            }
            
        except Exception as e:
            logger.error(f'Get import records error: {str(e)}')
            raise Exception(f'获取导入记录失败: {str(e)}')
