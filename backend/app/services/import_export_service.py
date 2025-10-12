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
from app.services.excel_style_service import ExcelStyleService

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
                filename=file.filename,
                file_path='',  # 文件路径
                total_count=len(df),
                success_count=success_count,
                failed_count=len(errors),
                error_details='; '.join(errors) if errors else None,
                status='completed' if len(errors) == 0 else 'failed'
            )
            db.session.add(import_record)
            db.session.commit()
            
            return {
                'total_count': len(df),
                'success_count': success_count,
                'failed_count': len(errors),
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
                filename=file.filename,
                file_path='',  # 文件路径
                total_count=len(df),
                success_count=success_count,
                failed_count=len(errors),
                error_details='; '.join(errors) if errors else None,
                status='completed' if len(errors) == 0 else 'failed'
            )
            db.session.add(import_record)
            db.session.commit()
            
            return {
                'total_count': len(df),
                'success_count': success_count,
                'failed_count': len(errors),
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
            
            # 记录原始列名
            from app.services.log_service import LogService
            LogService.log_info(f"[IMPORT_QUESTIONS_SERVICE] Excel原始列名: {list(df.columns)}", 'IMPORT_EXPORT')
            
            # 列名映射（中文到英文）
            column_mapping = {
                '题型': 'type',
                '题目': 'title', 
                '内容': 'content',
                '选项': 'options',
                '答案': 'answer',
                '解析': 'explanation',
                '难度': 'difficulty',
                '标签': 'tags',
                '分值': 'points',
                '状态': 'status',
                '科目ID': 'subject_id',
                '科目名称': 'subject_name'
            }
            
            # 重命名列
            df = df.rename(columns=column_mapping)
            
            # 记录映射后的列名
            LogService.log_info(f"[IMPORT_QUESTIONS_SERVICE] 映射后列名: {list(df.columns)}", 'IMPORT_EXPORT')
            
            # 验证列名
            required_columns = ['type', 'title', 'answer']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                LogService.log_error(f"[IMPORT_QUESTIONS_SERVICE] 缺少必要列: {missing_columns}", 'IMPORT_EXPORT')
                raise Exception(f'缺少必要列: {", ".join(missing_columns)}')
            
            LogService.log_info(f"[IMPORT_QUESTIONS_SERVICE] 开始处理 {len(df)} 行数据", 'IMPORT_EXPORT')
            
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
                        if 'options' in df.columns and pd.notna(row['options']):
                            options_str = str(row['options']).strip()
                            if options_str:
                                # 支持用|分隔的格式
                                if '|' in options_str:
                                    options = [opt.strip() for opt in options_str.split('|') if opt.strip()]
                                else:
                                    # 尝试解析JSON格式
                                    try:
                                        import json
                                        options = json.loads(options_str)
                                        if not isinstance(options, list):
                                            options = [options_str]
                                    except:
                                        options = [options_str]
                    
                    # 处理标签
                    tags = []
                    if 'tags' in df.columns and pd.notna(row['tags']):
                        tags_str = str(row['tags']).strip()
                        if tags_str:
                            # 支持用|分隔的格式
                            if '|' in tags_str:
                                tags = [tag.strip() for tag in tags_str.split('|') if tag.strip()]
                            else:
                                tags = [tags_str]
                    
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
                        points=int(row.get('points', 1)) if pd.notna(row.get('points')) else 1,
                        tags=tags
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
                filename=file.filename,
                file_path='',  # 文件路径
                total_count=len(df),
                success_count=success_count,
                failed_count=len(errors),
                error_details='; '.join(errors) if errors else None,
                status='completed' if len(errors) == 0 else 'failed'
            )
            db.session.add(import_record)
            db.session.commit()
            
            return {
                'total_count': len(df),
                'success_count': success_count,
                'failed_count': len(errors),
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
    def export_exams(keyword: Optional[str] = None, subject_id: Optional[int] = None, 
                    status: Optional[str] = None) -> pd.DataFrame:
        """导出考试数据"""
        try:
            from app.models.exam import Exam
            
            query = Exam.query
            
            if keyword:
                keyword_filter = f"%{keyword}%"
                query = query.filter(
                    Exam.title.like(keyword_filter) |
                    Exam.description.like(keyword_filter)
                )
            
            if subject_id:
                query = query.filter(Exam.subject_id == subject_id)
            
            if status:
                query = query.filter(Exam.status == status)
            
            exams = query.all()
            
            # 获取所有相关科目的映射
            from app.models.subject import Subject
            subject_ids = [exam.subject_id for exam in exams]
            subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
            subject_map = {subject.id: subject.name for subject in subjects}
            
            # 构建DataFrame
            data = []
            for exam in exams:
                # 获取科目名称
                subject_name = subject_map.get(exam.subject_id, '未知科目')
                
                data.append({
                    'ID': exam.id,
                    '考试标题': exam.title,
                    '科目': subject_name,
                    '描述': exam.description or '',
                    '总分': exam.total_points,
                    '题目数量': exam.question_count,
                    '考试时长': f"{exam.duration}分钟",
                    '开始时间': exam.start_time.strftime('%Y-%m-%d %H:%M:%S') if exam.start_time else '',
                    '结束时间': exam.end_time.strftime('%Y-%m-%d %H:%M:%S') if exam.end_time else '',
                    '状态': exam.status,
                    '创建时间': exam.created_at.strftime('%Y-%m-%d %H:%M:%S') if exam.created_at else ''
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            logger.error(f'Export exams error: {str(e)}')
            raise Exception(f'导出考试数据失败: {str(e)}')
    
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
    
    # ==================== 美化导出方法 ====================
    
    @staticmethod
    def export_users_styled(role: Optional[str] = None, status: Optional[str] = None):
        """导出用户数据（美化版）"""
        try:
            # 获取原始数据
            df = ImportExportService.export_users(role=role, status=status)
            
            # 创建美化Excel
            wb = ExcelStyleService.create_user_export_excel(df)
            
            # 转换为字节流
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            
            return output
            
        except Exception as e:
            logger.error(f'Export users styled error: {str(e)}')
            raise Exception(f'导出用户数据失败: {str(e)}')
    
    @staticmethod
    def export_subjects_styled(status: Optional[str] = None):
        """导出科目数据（美化版）"""
        try:
            # 获取原始数据
            df = ImportExportService.export_subjects(status=status)
            
            # 创建美化Excel
            wb = ExcelStyleService.create_subject_export_excel(df)
            
            # 转换为字节流
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            
            return output
            
        except Exception as e:
            logger.error(f'Export subjects styled error: {str(e)}')
            raise Exception(f'导出科目数据失败: {str(e)}')
    
    @staticmethod
    def export_questions_styled(subject_id: Optional[int] = None, question_type: Optional[str] = None, 
                               difficulty: Optional[str] = None):
        """导出试题数据（美化版）"""
        try:
            # 获取原始数据
            df = ImportExportService.export_questions(
                subject_id=subject_id,
                question_type=question_type,
                difficulty=difficulty
            )
            
            # 创建美化Excel
            wb = ExcelStyleService.create_question_export_excel(df)
            
            # 转换为字节流
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            
            return output
            
        except Exception as e:
            logger.error(f'Export questions styled error: {str(e)}')
            raise Exception(f'导出试题数据失败: {str(e)}')
    
    @staticmethod
    def export_exam_results_styled(exam_id: Optional[int] = None, user_id: Optional[int] = None,
                                  start_date: Optional[str] = None, end_date: Optional[str] = None):
        """导出考试结果数据（美化版）"""
        try:
            # 获取原始数据
            df = ImportExportService.export_exam_results(
                exam_id=exam_id,
                user_id=user_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # 创建美化Excel
            wb = ExcelStyleService.create_exam_result_export_excel(df)
            
            # 转换为字节流
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            
            return output
            
        except Exception as e:
            logger.error(f'Export exam results styled error: {str(e)}')
            raise Exception(f'导出考试结果失败: {str(e)}')
    
    @staticmethod
    def export_exams_styled(keyword: Optional[str] = None, subject_id: Optional[int] = None, 
                           status: Optional[str] = None):
        """导出考试数据（美化版）"""
        try:
            # 获取原始数据
            df = ImportExportService.export_exams(keyword=keyword, subject_id=subject_id, status=status)
            
            # 创建美化Excel
            wb = ExcelStyleService.create_exam_export_excel(df)
            
            # 转换为字节流
            output = io.BytesIO()
            wb.save(output)
            output.seek(0)
            
            return output
            
        except Exception as e:
            logger.error(f'Export exams styled error: {str(e)}')
            raise Exception(f'导出考试数据失败: {str(e)}')
