"""
简化的日志管理服务 - 只使用文件和控制台输出
"""
import os
import logging
import logging.handlers
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from app import db
from app.models.log_config import LogConfig


class LogConfigService:
    """日志配置服务"""
    
    @staticmethod
    def get_all_configs() -> List[Dict[str, Any]]:
        """获取所有日志配置"""
        try:
            configs = LogConfig.query.filter_by(is_active=True).all()
            return [config.to_dict() for config in configs]
        except:
            # 如果数据库不可用，返回默认配置
            return LogConfigService.get_default_configs()
    
    @staticmethod
    def get_config(key: str) -> Optional[Dict[str, Any]]:
        """获取指定配置"""
        try:
            config = LogConfig.query.filter_by(config_key=key, is_active=True).first()
            return config.to_dict() if config else None
        except:
            # 如果数据库不可用，返回默认配置
            default_configs = LogConfigService.get_default_configs()
            return next((c for c in default_configs if c['config_key'] == key), None)
    
    @staticmethod
    def get_default_configs() -> List[Dict[str, Any]]:
        """获取默认配置"""
        return [
            {
                'config_key': 'LOG_LEVEL',
                'config_value': 'INFO',
                'description': '日志级别'
            },
            {
                'config_key': 'LOG_MAX_SIZE',
                'config_value': '10485760',
                'description': '单个日志文件最大大小（字节）'
            },
            {
                'config_key': 'LOG_BACKUP_COUNT',
                'config_value': '30',
                'description': '日志文件备份数量'
            },
            {
                'config_key': 'LOG_FORMAT',
                'config_value': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'description': '日志格式'
            },
            {
                'config_key': 'LOG_ENABLE_FILE',
                'config_value': 'true',
                'description': '是否启用文件日志'
            },
            {
                'config_key': 'LOG_ENABLE_DATABASE',
                'config_value': 'false',
                'description': '是否启用数据库日志'
            },
            {
                'config_key': 'LOG_ENABLE_CONSOLE',
                'config_value': 'true',
                'description': '是否启用控制台日志'
            },
            {
                'config_key': 'LOG_ENABLE_ERROR_FILE',
                'config_value': 'true',
                'description': '是否启用错误日志单独文件'
            },
            {
                'config_key': 'LOG_ENABLE_ROTATION',
                'config_value': 'true',
                'description': '是否启用日志轮转'
            }
        ]


class LogService:
    """简化的日志服务 - 只使用文件和控制台输出"""
    
    @staticmethod
    def setup_logging():
        """设置日志配置"""
        # 创建logs目录
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 获取配置
        config_service = LogConfigService()
        configs = config_service.get_all_configs()
        config_dict = {config['config_key']: config['config_value'] for config in configs}
        
        # 设置默认值
        log_level = config_dict.get('LOG_LEVEL', 'INFO')
        log_max_size = int(config_dict.get('LOG_MAX_SIZE', '10485760'))
        log_backup_count = int(config_dict.get('LOG_BACKUP_COUNT', '30'))
        log_format = config_dict.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        enable_file = config_dict.get('LOG_ENABLE_FILE', 'true').lower() == 'true'
        enable_console = config_dict.get('LOG_ENABLE_CONSOLE', 'true').lower() == 'true'
        enable_error_file = config_dict.get('LOG_ENABLE_ERROR_FILE', 'true').lower() == 'true'
        
        # 配置根日志器
        logger = logging.getLogger()
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # 清除现有处理器
        logger.handlers.clear()
        
        # 控制台处理器
        if enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, log_level.upper()))
            console_formatter = logging.Formatter(log_format)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # 文件处理器（按日期和大小分割）
        if enable_file:
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=os.path.join(log_dir, 'examsphere.log'),
                when='midnight',
                interval=1,
                backupCount=log_backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_formatter = logging.Formatter(log_format)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            # 错误日志单独文件
            if enable_error_file:
                error_handler = logging.handlers.RotatingFileHandler(
                    filename=os.path.join(log_dir, 'error.log'),
                    maxBytes=log_max_size,
                    backupCount=log_backup_count,
                    encoding='utf-8'
                )
                error_handler.setLevel(logging.ERROR)
                error_formatter = logging.Formatter(log_format)
                error_handler.setFormatter(error_formatter)
                logger.addHandler(error_handler)
    
    @staticmethod
    def log_info(message: str, module: str = 'SYSTEM'):
        """记录信息日志"""
        logger = logging.getLogger(module)
        logger.info(message)
    
    @staticmethod
    def log_warning(message: str, module: str = 'SYSTEM'):
        """记录警告日志"""
        logger = logging.getLogger(module)
        logger.warning(message)
    
    @staticmethod
    def log_error(message: str, module: str = 'SYSTEM'):
        """记录错误日志"""
        logger = logging.getLogger(module)
        logger.error(message)
    
    @staticmethod
    def log_debug(message: str, module: str = 'SYSTEM'):
        """记录调试日志"""
        logger = logging.getLogger(module)
        logger.debug(message)
    
    @staticmethod
    def log_critical(message: str, module: str = 'SYSTEM'):
        """记录严重错误日志"""
        logger = logging.getLogger(module)
        logger.critical(message)
    
    @staticmethod
    def log_operation(operation: str, user: str = None, details: str = None):
        """记录操作日志"""
        message = f"操作: {operation}"
        if user:
            message += f" | 用户: {user}"
        if details:
            message += f" | 详情: {details}"
        LogService.log_info(message, 'OPERATION')
    
    @staticmethod
    def log_api_access(method: str, path: str, user: str = None, status: int = None):
        """记录API访问日志"""
        message = f"API访问: {method} {path}"
        if user:
            message += f" | 用户: {user}"
        if status:
            message += f" | 状态: {status}"
        LogService.log_info(message, 'API')
    
    @staticmethod
    def log_user_action(action: str, user: str, details: str = None):
        """记录用户行为日志"""
        message = f"用户行为: {action} | 用户: {user}"
        if details:
            message += f" | 详情: {details}"
        LogService.log_info(message, 'USER_ACTION')
    
    @staticmethod
    def log_system_event(event: str, details: str = None):
        """记录系统事件日志"""
        message = f"系统事件: {event}"
        if details:
            message += f" | 详情: {details}"
        LogService.log_info(message, 'SYSTEM')
    
    @staticmethod
    def log_security_event(event: str, user: str = None, ip: str = None):
        """记录安全事件日志"""
        message = f"安全事件: {event}"
        if user:
            message += f" | 用户: {user}"
        if ip:
            message += f" | IP: {ip}"
        LogService.log_warning(message, 'SECURITY')
    
    @staticmethod
    def log_database_operation(operation: str, table: str = None, details: str = None):
        """记录数据库操作日志"""
        message = f"数据库操作: {operation}"
        if table:
            message += f" | 表: {table}"
        if details:
            message += f" | 详情: {details}"
        LogService.log_info(message, 'DATABASE')
    
    @staticmethod
    def log_file_operation(operation: str, filename: str = None, details: str = None):
        """记录文件操作日志"""
        message = f"文件操作: {operation}"
        if filename:
            message += f" | 文件: {filename}"
        if details:
            message += f" | 详情: {details}"
        LogService.log_info(message, 'FILE')
    
    @staticmethod
    def log_exam_event(event: str, exam_id: str = None, user: str = None, details: str = None):
        """记录考试事件日志"""
        message = f"考试事件: {event}"
        if exam_id:
            message += f" | 考试ID: {exam_id}"
        if user:
            message += f" | 用户: {user}"
        if details:
            message += f" | 详情: {details}"
        LogService.log_info(message, 'EXAM')
    
    @staticmethod
    def log_performance(operation: str, duration: float, details: str = None):
        """记录性能日志"""
        message = f"性能监控: {operation} | 耗时: {duration:.3f}秒"
        if details:
            message += f" | 详情: {details}"
        LogService.log_info(message, 'PERFORMANCE')
    
    @staticmethod
    def log_exception(exception: Exception, context: str = None):
        """记录异常日志"""
        message = f"异常: {type(exception).__name__}: {str(exception)}"
        if context:
            message += f" | 上下文: {context}"
        LogService.log_error(message, 'EXCEPTION')
    
    @staticmethod
    def log_startup(message: str):
        """记录启动日志"""
        LogService.log_info(f"系统启动: {message}", 'STARTUP')
    
    @staticmethod
    def log_shutdown(message: str):
        """记录关闭日志"""
        LogService.log_info(f"系统关闭: {message}", 'SHUTDOWN')
