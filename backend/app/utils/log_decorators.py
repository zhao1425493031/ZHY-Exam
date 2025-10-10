"""
简化的日志装饰器 - 只使用文件和控制台输出
"""
import time
import logging
from functools import wraps
from flask import request, g
from flask_jwt_extended import get_jwt_identity
from app.services.log_service import LogService


def log_operation(operation_type: str, description: str = None):
    """
    记录操作日志的装饰器
    
    Args:
        operation_type: 操作类型
        description: 操作描述
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            user_id = None
            ip_address = None
            
            try:
                # 获取用户信息
                try:
                    user_id = get_jwt_identity()
                except:
                    pass
                
                # 获取请求信息
                ip_address = request.remote_addr
                
                # 执行原函数
                result = f(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # 记录成功日志
                LogService.log_operation(
                    operation=operation_type,
                    user=str(user_id) if user_id else 'anonymous',
                    details=f"{description or operation_type}操作成功 | IP:{ip_address} | 耗时:{execution_time:.3f}秒"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # 记录错误日志
                LogService.log_error(
                    message=f"{description or operation_type}操作失败: {str(e)} | IP:{ip_address} | 耗时:{execution_time:.3f}秒",
                    module='OPERATION'
                )
                
                raise
        
        return decorated_function
    return decorator


def log_api_access():
    """
    记录API访问日志的装饰器
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            user_id = None
            ip_address = None
            
            try:
                # 获取用户信息
                try:
                    user_id = get_jwt_identity()
                except:
                    pass
                
                # 获取请求信息
                ip_address = request.remote_addr
                
                # 执行原函数
                result = f(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # 记录API访问日志
                LogService.log_api_access(
                    method=request.method,
                    path=request.path,
                    user=str(user_id) if user_id else 'anonymous',
                    status=200
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                # 记录API错误日志
                LogService.log_error(
                    message=f"API错误: {request.method} {request.path} - {str(e)} | IP:{ip_address} | 耗时:{execution_time:.3f}秒",
                    module='API'
                )
                
                raise
        
        return decorated_function
    return decorator


def log_user_action(action: str, description: str = None):
    """
    记录用户行为日志
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            user_id = None
            ip_address = None
            
            try:
                user_id = get_jwt_identity()
                ip_address = request.remote_addr
                
                result = f(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # 记录用户行为日志
                LogService.log_user_action(
                    action=action,
                    user=str(user_id) if user_id else 'anonymous',
                    details=f"{description or '用户操作'} | IP:{ip_address} | 耗时:{execution_time:.3f}秒"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                LogService.log_error(
                    message=f"用户行为失败: {action} - {str(e)} | IP:{ip_address} | 耗时:{execution_time:.3f}秒",
                    module='USER_ACTION'
                )
                
                raise
        
        return decorated_function
    return decorator


def log_database_operation(operation: str, table: str = None):
    """
    记录数据库操作日志
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # 记录数据库操作日志
                LogService.log_database_operation(
                    operation=operation,
                    table=table,
                    details=f"操作成功 | 耗时:{execution_time:.3f}秒"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                LogService.log_error(
                    message=f"数据库操作失败: {operation} - {str(e)} | 耗时:{execution_time:.3f}秒",
                    module='DATABASE'
                )
                
                raise
        
        return decorated_function
    return decorator


def log_file_operation(operation: str, filename: str = None):
    """
    记录文件操作日志
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # 记录文件操作日志
                LogService.log_file_operation(
                    operation=operation,
                    filename=filename,
                    details=f"操作成功 | 耗时:{execution_time:.3f}秒"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                LogService.log_error(
                    message=f"文件操作失败: {operation} - {str(e)} | 耗时:{execution_time:.3f}秒",
                    module='FILE'
                )
                
                raise
        
        return decorated_function
    return decorator


def log_exam_event(event: str, exam_id: str = None):
    """
    记录考试事件日志
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            user_id = None
            
            try:
                user_id = get_jwt_identity()
                result = f(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # 记录考试事件日志
                LogService.log_exam_event(
                    event=event,
                    exam_id=exam_id,
                    user=str(user_id) if user_id else 'anonymous',
                    details=f"事件成功 | 耗时:{execution_time:.3f}秒"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                LogService.log_error(
                    message=f"考试事件失败: {event} - {str(e)} | 耗时:{execution_time:.3f}秒",
                    module='EXAM'
                )
                
                raise
        
        return decorated_function
    return decorator


def log_performance(operation: str):
    """
    记录性能监控日志
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = f(*args, **kwargs)
                
                execution_time = time.time() - start_time
                
                # 记录性能日志
                LogService.log_performance(
                    operation=operation,
                    duration=execution_time,
                    details="操作完成"
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                LogService.log_error(
                    message=f"性能监控: {operation} - {str(e)} | 耗时:{execution_time:.3f}秒",
                    module='PERFORMANCE'
                )
                
                raise
        
        return decorated_function
    return decorator
