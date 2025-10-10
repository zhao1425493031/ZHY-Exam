# 数据验证器
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    """用户数据验证器"""
    username = fields.Str(required=True, validate=[
        validate.Length(min=3, max=20),
        validate.Regexp(r'^[a-zA-Z0-9_]+$', error='用户名只能包含字母、数字、下划线')
    ])
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    real_name = fields.Str(validate=validate.Length(max=50))
    role = fields.Str(validate=validate.OneOf(['admin', 'user']))
    phone = fields.Str(validate=validate.Length(max=20))

class UserUpdateSchema(Schema):
    """用户更新数据验证器"""
    username = fields.Str(validate=[
        validate.Length(min=3, max=20),
        validate.Regexp(r'^[a-zA-Z0-9_]+$', error='用户名只能包含字母、数字、下划线')
    ])
    email = fields.Email()
    real_name = fields.Str(validate=validate.Length(max=50))
    role = fields.Str(validate=validate.OneOf(['admin', 'user']))
    phone = fields.Str(validate=validate.Length(max=20))
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'banned']))

class LoginSchema(Schema):
    """登录数据验证器"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class ChangePasswordSchema(Schema):
    """修改密码数据验证器"""
    old_password = fields.Str(required=True)
    new_password = fields.Str(required=True, validate=validate.Length(min=6))

class SubjectSchema(Schema):
    """科目数据验证器"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    code = fields.Str(required=True, validate=[
        validate.Length(min=2, max=20),
        validate.Regexp(r'^[A-Z0-9_]+$', error='科目代码只能包含大写字母、数字、下划线')
    ])
    description = fields.Str(validate=validate.Length(max=500))
    category = fields.Str(validate=validate.Length(max=50))
    status = fields.Str(validate=validate.OneOf(['active', 'inactive']))

class QuestionSchema(Schema):
    """试题数据验证器"""
    subject_id = fields.Int(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(['single', 'multiple', 'judge', 'fill', 'essay']))
    title = fields.Str(required=True, validate=validate.Length(min=5, max=1000))
    content = fields.Str(validate=validate.Length(max=2000))
    options = fields.List(fields.Str())
    answer = fields.Str(required=True)
    explanation = fields.Str(validate=validate.Length(max=1000))
    difficulty = fields.Str(validate=validate.OneOf(['easy', 'medium', 'hard']))
    tags = fields.List(fields.Str())
    points = fields.Int(validate=validate.Range(min=1, max=100))
    status = fields.Str(validate=validate.OneOf(['draft', 'published', 'archived']))

class ExamSchema(Schema):
    """考试数据验证器"""
    title = fields.Str(required=True, validate=validate.Length(min=5, max=200))
    subject_id = fields.Int(required=True)
    description = fields.Str(validate=validate.Length(max=1000))
    duration = fields.Int(required=True, validate=validate.Range(min=5, max=300))
    total_points = fields.Int(required=True, validate=validate.Range(min=1, max=1000))
    question_count = fields.Int(required=True, validate=validate.Range(min=1, max=200))
    question_ids = fields.List(fields.Int(), required=True)
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    status = fields.Str(validate=validate.OneOf(['draft', 'published', 'ongoing', 'finished', 'cancelled']))
    settings = fields.Dict()

class ExamRecordSchema(Schema):
    """考试记录数据验证器"""
    exam_id = fields.Int(required=True)
    answers = fields.Dict(required=True)
    submit_time = fields.DateTime()

# 分页查询参数验证器
class PaginationSchema(Schema):
    """分页参数验证器"""
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    size = fields.Int(missing=10, validate=validate.Range(min=1, max=100))
    sort = fields.Str(missing='id')
    order = fields.Str(missing='desc', validate=validate.OneOf(['asc', 'desc']))

# 搜索参数验证器
class SearchSchema(Schema):
    """搜索参数验证器"""
    keyword = fields.Str(validate=validate.Length(max=100))
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'banned', 'draft', 'published', 'ongoing', 'finished', 'cancelled']))
    role = fields.Str(validate=validate.OneOf(['admin', 'user']))
    subject_id = fields.Int()
    type = fields.Str(validate=validate.OneOf(['single', 'multiple', 'judge', 'fill', 'essay']))
    difficulty = fields.Str(validate=validate.OneOf(['easy', 'medium', 'hard']))
    category = fields.Str(validate=validate.Length(max=50))
    # 添加分页字段
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    size = fields.Int(missing=10, validate=validate.Range(min=1, max=100))
    sort = fields.Str(missing='id')
    order = fields.Str(missing='desc', validate=validate.OneOf(['asc', 'desc']))
