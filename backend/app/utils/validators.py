# 数据验证器
from marshmallow import Schema, fields, validate, ValidationError, validates_schema

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
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'banned']))

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
    is_free = fields.Bool(missing=True)
    price = fields.Decimal(places=2, validate=validate.Range(min=0, max=99999.99), missing=0)
    original_price = fields.Decimal(places=2, validate=validate.Range(min=0, max=99999.99), missing=0)
    discount_rate = fields.Integer(validate=validate.Range(min=1, max=100), missing=100)
    
    @validates_schema
    def validate_pricing(self, data, **kwargs):
        """验证价格逻辑"""
        # 如果是免费科目，跳过价格验证
        if data.get('is_free', True):
            data['price'] = 0
            data['original_price'] = 0
            data['discount_rate'] = 100
            return
        
        # 如果是收费科目，必须有原价
        original_price = float(data.get('original_price', 0))
        price = float(data.get('price', 0))
        discount_rate = int(data.get('discount_rate', 100))
        
        # 验证原价
        if original_price <= 0:
            raise ValidationError('收费科目的原价必须大于0', field_name='original_price')
        
        # 验证现价不能高于原价
        if price > original_price:
            raise ValidationError('现价不能高于原价', field_name='price')
        
        # 验证折扣率
        if discount_rate < 1 or discount_rate > 100:
            raise ValidationError('折扣率必须在1-100之间', field_name='discount_rate')
        
        # 验证价格计算是否合理（允许1%的误差）
        calculated_price = original_price * discount_rate / 100
        price_difference = abs(price - calculated_price)
        max_allowed_difference = original_price * 0.01  # 1%的误差
        
        if price_difference > max_allowed_difference:
            raise ValidationError(
                f'价格计算不匹配: 原价 {original_price} × 折扣率 {discount_rate}% = {calculated_price:.2f}, 但现价为 {price}',
                field_name='price'
            )

class QuestionSchema(Schema):
    """试题数据验证器"""
    subject_id = fields.Int(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(['single', 'multiple', 'judge', 'fill', 'essay']))
    title = fields.Str(required=True, validate=validate.Length(min=5, max=1000))
    content = fields.Str(validate=validate.Length(max=2000), allow_none=True)
    options = fields.List(fields.Str(), allow_none=True)
    answer = fields.Str(required=True)
    explanation = fields.Str(validate=validate.Length(max=1000), allow_none=True)
    difficulty = fields.Str(validate=validate.OneOf(['easy', 'medium', 'hard']), allow_none=True)
    tags = fields.List(fields.Str(), allow_none=True)
    points = fields.Int(validate=validate.Range(min=1, max=100), allow_none=True)
    status = fields.Str(validate=validate.OneOf(['draft', 'published', 'archived']), allow_none=True)

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
    keyword = fields.Str(validate=validate.Length(max=100), allow_none=True)
    status = fields.Str(validate=validate.OneOf(['active', 'inactive', 'banned', 'draft', 'published', 'ongoing', 'finished', 'cancelled']), allow_none=True)
    role = fields.Str(validate=validate.OneOf(['admin', 'user']), allow_none=True)
    subject_id = fields.Int(allow_none=True)
    type = fields.Str(validate=validate.OneOf(['single', 'multiple', 'judge', 'fill', 'essay']), allow_none=True)
    difficulty = fields.Str(validate=validate.OneOf(['easy', 'medium', 'hard']), allow_none=True)
    category = fields.Str(validate=validate.Length(max=50), allow_none=True)
    # 添加分页字段
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    size = fields.Int(missing=10, validate=validate.Range(min=1, max=100))
    sort = fields.Str(missing='id')
    order = fields.Str(missing='desc', validate=validate.OneOf(['asc', 'desc']))
