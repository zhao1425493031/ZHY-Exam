"""
日志管理API接口
"""
from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import Schema, fields, validate
from app.services.log_service import LogService, LogConfigService
from app.services.user_service import UserService
from app.utils.decorators import require_roles
from app.utils.helpers import build_response, build_error_response


class LogConfigSchema(Schema):
    """日志配置验证模式"""
    config_key = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    config_value = fields.Str(required=True)
    description = fields.Str(validate=validate.Length(max=500))


class LogSearchSchema(Schema):
    """日志搜索验证模式"""
    keyword = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    page = fields.Int(validate=validate.Range(min=1, max=1000))
    per_page = fields.Int(validate=validate.Range(min=1, max=100))


class LogConfigAPI(Resource):
    """日志配置API"""
    
    @jwt_required()
    @require_roles('admin')
    def get(self):
        """获取所有日志配置"""
        try:
            configs = LogConfigService.get_all_configs()
            return jsonify(build_response(
                message='获取日志配置成功',
                data=configs
            ))
        except Exception as e:
            return jsonify(build_error_response(500, f'获取日志配置失败: {str(e)}')), 500
    
    @jwt_required()
    @require_roles('admin')
    def post(self):
        """创建日志配置"""
        try:
            schema = LogConfigSchema()
            data = schema.load(request.get_json())
            
            success = LogConfigService.create_config(
                key=data['config_key'],
                value=data['config_value'],
                description=data.get('description')
            )
            
            if success:
                return jsonify(build_response(message='创建日志配置成功'))
            else:
                return jsonify(build_error_response(400, '创建日志配置失败')), 400
                
        except Exception as e:
            return jsonify(build_error_response(500, f'创建日志配置失败: {str(e)}')), 500


class LogConfigDetailAPI(Resource):
    """日志配置详情API"""
    
    @jwt_required()
    @require_roles('admin')
    def get(self, config_key):
        """获取指定配置"""
        try:
            config = LogConfigService.get_config(config_key)
            if config:
                return jsonify(build_response(
                    message='获取日志配置成功',
                    data=config
                ))
            else:
                return jsonify(build_error_response(404, '日志配置不存在')), 404
        except Exception as e:
            return jsonify(build_error_response(500, f'获取日志配置失败: {str(e)}')), 500
    
    @jwt_required()
    @require_roles('admin')
    def put(self, config_key):
        """更新日志配置"""
        try:
            schema = LogConfigSchema()
            data = schema.load(request.get_json())
            
            success = LogConfigService.update_config(
                key=config_key,
                value=data['config_value'],
                description=data.get('description')
            )
            
            if success:
                return jsonify(build_response(message='更新日志配置成功'))
            else:
                return jsonify(build_error_response(404, '日志配置不存在')), 404
                
        except Exception as e:
            return jsonify(build_error_response(500, f'更新日志配置失败: {str(e)}')), 500


class LogListAPI(Resource):
    """日志列表API"""
    
    @jwt_required()
    @require_roles('admin')
    def get(self):
        """获取日志列表"""
        try:
            # 获取查询参数
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            level = request.args.get('level')
            module = request.args.get('module')
            user_id = request.args.get('user_id', type=int)
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            # 获取日志列表
            result = LogService.get_logs(
                page=page,
                per_page=per_page,
                level=level,
                module=module,
                user_id=user_id,
                start_date=start_date,
                end_date=end_date
            )
            
            return jsonify(build_response(
                message='获取日志列表成功',
                data=result
            ))
            
        except Exception as e:
            return jsonify(build_error_response(500, f'获取日志列表失败: {str(e)}')), 500


class LogDetailAPI(Resource):
    """日志详情API"""
    
    @jwt_required()
    @require_roles('admin')
    def get(self, log_id):
        """获取日志详情"""
        try:
            from app.models.log_config import SystemLog
            
            log = SystemLog.query.get(log_id)
            if log:
                return jsonify(build_response(
                    message='获取日志详情成功',
                    data=log.to_dict()
                ))
            else:
                return jsonify(build_error_response(404, '日志不存在')), 404
                
        except Exception as e:
            return jsonify(build_error_response(500, f'获取日志详情失败: {str(e)}')), 500


class LogSearchAPI(Resource):
    """日志搜索API"""
    
    @jwt_required()
    @require_roles('admin')
    def post(self):
        """搜索日志"""
        try:
            schema = LogSearchSchema()
            data = schema.load(request.get_json())
            
            result = LogService.search_logs(
                keyword=data['keyword'],
                page=data.get('page', 1),
                per_page=data.get('per_page', 20)
            )
            
            return jsonify(build_response(
                message='搜索日志成功',
                data=result
            ))
            
        except Exception as e:
            return jsonify(build_error_response(500, f'搜索日志失败: {str(e)}')), 500


class LogStatisticsAPI(Resource):
    """日志统计API"""
    
    @jwt_required()
    @require_roles('admin')
    def get(self):
        """获取日志统计信息"""
        try:
            stats = LogService.get_log_statistics()
            return jsonify(build_response(
                message='获取日志统计成功',
                data=stats
            ))
        except Exception as e:
            return jsonify(build_error_response(500, f'获取日志统计失败: {str(e)}')), 500


class LogCleanupAPI(Resource):
    """日志清理API"""
    
    @jwt_required()
    @require_roles('admin')
    def post(self):
        """清理旧日志"""
        try:
            data = request.get_json() or {}
            days = data.get('days', 30)
            
            deleted_count = LogService.cleanup_old_logs(days)
            
            return jsonify(build_response(
                message=f'清理日志成功，删除了{deleted_count}条记录',
                data={'deleted_count': deleted_count}
            ))
            
        except Exception as e:
            return jsonify(build_error_response(500, f'清理日志失败: {str(e)}')), 500


class LogSetupAPI(Resource):
    """日志设置API"""
    
    @jwt_required()
    @require_roles('admin')
    def post(self):
        """重新设置日志配置"""
        try:
            LogService.setup_logging()
            return jsonify(build_response(message='日志配置设置成功'))
        except Exception as e:
            return jsonify(build_error_response(500, f'日志配置设置失败: {str(e)}')), 500
