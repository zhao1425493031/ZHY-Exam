# API基础框架
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import require_roles, validate_json
from app.utils.validators import PaginationSchema, SearchSchema
from app.utils.helpers import build_response, build_error_response, paginate_query
from app.models import db

# 创建蓝图
auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)
subjects_bp = Blueprint('subjects', __name__)
questions_bp = Blueprint('questions', __name__)
exams_bp = Blueprint('exams', __name__)
exam_records_bp = Blueprint('exam_records', __name__)

# 通用错误处理
@auth_bp.errorhandler(404)
@users_bp.errorhandler(404)
@subjects_bp.errorhandler(404)
@questions_bp.errorhandler(404)
@exams_bp.errorhandler(404)
@exam_records_bp.errorhandler(404)
def not_found(error):
    return jsonify(build_error_response(404, '资源未找到')), 404

@auth_bp.errorhandler(500)
@users_bp.errorhandler(500)
@subjects_bp.errorhandler(500)
@questions_bp.errorhandler(500)
@exams_bp.errorhandler(500)
@exam_records_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify(build_error_response(500, '服务器内部错误')), 500

# 通用分页处理
def handle_pagination(query, schema_class=None):
    """处理分页查询"""
    try:
        # 验证分页参数
        pagination_schema = PaginationSchema()
        pagination_data = pagination_schema.load({
            'page': request.args.get('page', 1, type=int),
            'size': request.args.get('size', 10, type=int),
            'sort': request.args.get('sort', 'id'),
            'order': request.args.get('order', 'desc')
        })
        
        # 验证搜索参数
        search_data = {}
        if schema_class:
            search_schema = SearchSchema()
            search_data = search_schema.load(request.args)
        
        # 应用搜索过滤
        if search_data:
            for key, value in search_data.items():
                if value is not None and hasattr(query, key):
                    query = query.filter(getattr(query, key) == value)
        
        # 应用排序
        sort_field = pagination_data.get('sort', 'id')
        order = pagination_data.get('order', 'desc')
        
        if hasattr(query, sort_field):
            if order == 'desc':
                query = query.order_by(getattr(query, sort_field).desc())
            else:
                query = query.order_by(getattr(query, sort_field).asc())
        
        # 执行分页查询
        pagination = paginate_query(
            query,
            page=pagination_data.get('page', 1),
            per_page=pagination_data.get('size', 10)
        )
        
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
        
    except Exception as e:
        raise ValueError(f'分页查询失败: {str(e)}')

# 通用CRUD操作
class BaseAPI:
    """基础API类"""
    
    def __init__(self, model_class, schema_class):
        self.model_class = model_class
        self.schema_class = schema_class
    
    def get_list(self):
        """获取列表"""
        try:
            query = self.model_class.query
            result = handle_pagination(query, self.schema_class)
            return jsonify(build_response(data=result))
        except Exception as e:
            return jsonify(build_error_response(400, str(e))), 400
    
    def get_item(self, item_id):
        """获取单个项目"""
        try:
            item = self.model_class.query.get_or_404(item_id)
            return jsonify(build_response(data=item.to_dict()))
        except Exception as e:
            return jsonify(build_error_response(404, str(e))), 404
    
    def create_item(self):
        """创建项目"""
        try:
            data = request.get_json()
            validated_data = self.schema_class().load(data)
            
            item = self.model_class(**validated_data)
            db.session.add(item)
            db.session.commit()
            
            return jsonify(build_response(data=item.to_dict())), 201
        except Exception as e:
            db.session.rollback()
            return jsonify(build_error_response(400, str(e))), 400
    
    def update_item(self, item_id):
        """更新项目"""
        try:
            item = self.model_class.query.get_or_404(item_id)
            data = request.get_json()
            validated_data = self.schema_class().load(data, partial=True)
            
            for key, value in validated_data.items():
                setattr(item, key, value)
            
            db.session.commit()
            return jsonify(build_response(data=item.to_dict()))
        except Exception as e:
            db.session.rollback()
            return jsonify(build_error_response(400, str(e))), 400
    
    def delete_item(self, item_id):
        """删除项目"""
        try:
            item = self.model_class.query.get_or_404(item_id)
            db.session.delete(item)
            db.session.commit()
            return jsonify(build_response(message='删除成功'))
        except Exception as e:
            db.session.rollback()
            return jsonify(build_error_response(400, str(e))), 400

# 导出蓝图
__all__ = [
    'auth_bp',
    'users_bp', 
    'subjects_bp',
    'questions_bp',
    'exams_bp',
    'exam_records_bp',
    'BaseAPI',
    'handle_pagination'
]
