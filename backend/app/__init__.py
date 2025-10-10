# Flask 应用工厂模式
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__)
    
    # 配置
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    if config_name == 'development':
        app.config.from_object('app.config.development.DevelopmentConfig')
    elif config_name == 'production':
        app.config.from_object('app.config.production.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('app.config.testing.TestingConfig')
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
            "supports_credentials": True
        }
    })
    
    # 初始化限流器（开发环境禁用限制）
    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=[],  # 开发环境不设置限制
        storage_uri="memory://"
    )
    
    # 注册蓝图
    from app.api.auth import auth_bp
    from app.api.users import users_bp
    from app.api.subjects import subjects_bp
    from app.api.questions import questions_bp
    from app.api.exams import exams_bp
    from app.api.exam_records import exam_records_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(subjects_bp, url_prefix='/api/subjects')
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(exams_bp, url_prefix='/api/exams')
    app.register_blueprint(exam_records_bp, url_prefix='/api/exam-records')
    
    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {'code': 401, 'message': 'Token已过期', 'data': None}, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'code': 401, 'message': '无效的Token', 'data': None}, 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {'code': 401, 'message': '缺少认证Token', 'data': None}, 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return {'code': 401, 'message': '需要刷新Token', 'data': None}, 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {'code': 401, 'message': 'Token已被撤销', 'data': None}, 401
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return {'message': '资源未找到'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'message': '服务器内部错误'}, 500
    
    return app
