# 试题导入导出服务
import pandas as pd
import json
from io import BytesIO
from flask import send_file
from app.models.question import Question
from app.models.subject import Subject
from app.models import db
from app.utils.helpers import build_response, build_error_response, log_operation, get_client_ip
from datetime import datetime

class QuestionImportExportService:
    """试题导入导出服务"""
    
    @staticmethod
    def export_questions_to_excel(subject_id=None, question_ids=None):
        """导出试题到Excel"""
        try:
            # 构建查询
            query = Question.query
            if subject_id:
                query = query.filter_by(subject_id=subject_id)
            if question_ids:
                query = query.filter(Question.id.in_(question_ids))
            
            questions = query.all()
            
            if not questions:
                raise Exception('没有找到要导出的试题')
            
            # 准备数据
            data = []
            for q in questions:
                # 获取科目信息
                subject = Subject.query.get(q.subject_id)
                subject_name = subject.name if subject else '未知科目'
                
                # 处理选项
                options_text = ''
                if q.options:
                    if isinstance(q.options, list):
                        options_text = '|'.join(q.options)
                    else:
                        options_text = str(q.options)
                
                # 处理标签
                tags_text = ''
                if q.tags:
                    if isinstance(q.tags, list):
                        tags_text = '|'.join(q.tags)
                    else:
                        tags_text = str(q.tags)
                
                data.append({
                    'ID': q.id,
                    '科目名称': subject_name,
                    '科目代码': subject.code if subject else '',
                    '题型': q.type,
                    '题目': q.title,
                    '内容': q.content or '',
                    '选项': options_text,
                    '答案': q.answer,
                    '解析': q.explanation or '',
                    '难度': q.difficulty,
                    '标签': tags_text,
                    '分值': q.points,
                    '状态': q.status,
                    '创建时间': q.created_at.strftime('%Y-%m-%d %H:%M:%S') if q.created_at else ''
                })
            
            # 创建DataFrame
            df = pd.DataFrame(data)
            
            # 创建Excel文件
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='试题列表', index=False)
            
            output.seek(0)
            
            # 生成文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'questions_export_{timestamp}.xlsx'
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
            
        except Exception as e:
            raise Exception(f'导出试题失败: {str(e)}')
    
    @staticmethod
    def import_questions_from_excel(file, subject_id, user_id):
        """从Excel导入试题"""
        try:
            # 读取Excel文件
            df = pd.read_excel(file)
            
            # 验证必要的列
            required_columns = ['题型', '题目', '答案']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise Exception(f'缺少必要的列: {", ".join(missing_columns)}')
            
            # 验证科目是否存在
            subject = Subject.query.get(subject_id)
            if not subject:
                raise Exception('科目不存在')
            
            success_count = 0
            error_count = 0
            errors = []
            
            for index, row in df.iterrows():
                try:
                    # 解析数据
                    question_type = str(row['题型']).strip()
                    title = str(row['题目']).strip()
                    answer = str(row['答案']).strip()
                    
                    # 验证题型
                    valid_types = ['single', 'multiple', 'judge', 'fill', 'essay']
                    if question_type not in valid_types:
                        raise Exception(f'无效的题型: {question_type}')
                    
                    # 处理选项
                    options = []
                    if '选项' in row and pd.notna(row['选项']):
                        options_text = str(row['选项']).strip()
                        if options_text:
                            options = [opt.strip() for opt in options_text.split('|') if opt.strip()]
                    
                    # 处理标签
                    tags = []
                    if '标签' in row and pd.notna(row['标签']):
                        tags_text = str(row['标签']).strip()
                        if tags_text:
                            tags = [tag.strip() for tag in tags_text.split('|') if tag.strip()]
                    
                    # 处理其他字段
                    content = str(row['内容']).strip() if '内容' in row and pd.notna(row['内容']) else ''
                    explanation = str(row['解析']).strip() if '解析' in row and pd.notna(row['解析']) else ''
                    difficulty = str(row['难度']).strip() if '难度' in row and pd.notna(row['难度']) else 'medium'
                    points = int(row['分值']) if '分值' in row and pd.notna(row['分值']) else 1
                    status = str(row['状态']).strip() if '状态' in row and pd.notna(row['状态']) else 'draft'
                    
                    # 验证难度
                    valid_difficulties = ['easy', 'medium', 'hard']
                    if difficulty not in valid_difficulties:
                        difficulty = 'medium'
                    
                    # 验证状态
                    valid_statuses = ['draft', 'published', 'archived']
                    if status not in valid_statuses:
                        status = 'draft'
                    
                    # 创建试题
                    question = Question(
                        subject_id=subject_id,
                        type=question_type,
                        title=title,
                        content=content,
                        options=options,
                        answer=answer,
                        explanation=explanation,
                        difficulty=difficulty,
                        tags=tags,
                        points=points,
                        status=status,
                        created_by=user_id
                    )
                    
                    db.session.add(question)
                    success_count += 1
                    
                except Exception as e:
                    error_count += 1
                    errors.append(f'第{index+2}行: {str(e)}')
            
            # 提交事务
            db.session.commit()
            
            return {
                'success_count': success_count,
                'error_count': error_count,
                'errors': errors
            }
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f'导入试题失败: {str(e)}')
    
    @staticmethod
    def get_import_template():
        """获取导入模板"""
        try:
            # 创建模板数据
            template_data = [
                {
                    '题型': 'single',
                    '题目': '以下哪个是Python的数据类型？',
                    '内容': '请选择正确的Python数据类型',
                    '选项': 'int|str|list|dict',
                    '答案': 'int',
                    '解析': 'int是Python的整数类型',
                    '难度': 'easy',
                    '标签': 'Python|数据类型',
                    '分值': 1,
                    '状态': 'draft'
                },
                {
                    '题型': 'multiple',
                    '题目': '以下哪些是Python的内置函数？',
                    '内容': '请选择所有正确的Python内置函数',
                    '选项': 'print|len|max|min',
                    '答案': 'print|len|max|min',
                    '解析': '这些都是Python的内置函数',
                    '难度': 'medium',
                    '标签': 'Python|内置函数',
                    '分值': 2,
                    '状态': 'draft'
                },
                {
                    '题型': 'judge',
                    '题目': 'Python是一种解释型语言',
                    '内容': '',
                    '选项': '',
                    '答案': 'true',
                    '解析': 'Python确实是解释型语言',
                    '难度': 'easy',
                    '标签': 'Python|语言特性',
                    '分值': 1,
                    '状态': 'draft'
                }
            ]
            
            # 创建DataFrame
            df = pd.DataFrame(template_data)
            
            # 创建Excel文件
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='试题模板', index=False)
                
                # 添加说明工作表
                instructions = [
                    ['字段名', '说明', '示例'],
                    ['题型', 'single(单选)/multiple(多选)/judge(判断)/fill(填空)/essay(简答)', 'single'],
                    ['题目', '试题题目内容', '以下哪个是Python的数据类型？'],
                    ['内容', '试题补充内容（可选）', '请选择正确的Python数据类型'],
                    ['选项', '选项内容，多个选项用|分隔', 'int|str|list|dict'],
                    ['答案', '正确答案', 'int'],
                    ['解析', '答案解析（可选）', 'int是Python的整数类型'],
                    ['难度', 'easy(简单)/medium(中等)/hard(困难)', 'easy'],
                    ['标签', '试题标签，多个标签用|分隔', 'Python|数据类型'],
                    ['分值', '试题分值', '1'],
                    ['状态', 'draft(草稿)/published(发布)/archived(归档)', 'draft']
                ]
                
                instructions_df = pd.DataFrame(instructions[1:], columns=instructions[0])
                instructions_df.to_excel(writer, sheet_name='字段说明', index=False)
            
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='question_import_template.xlsx'
            )
            
        except Exception as e:
            raise Exception(f'生成模板失败: {str(e)}')

