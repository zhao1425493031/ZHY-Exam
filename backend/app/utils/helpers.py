# 工具函数
import os
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

def generate_uuid() -> str:
    """生成UUID字符串"""
    return str(uuid.uuid4())

def generate_hash(text: str) -> str:
    """生成文本的MD5哈希值"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def format_datetime(dt: datetime, format_str: str = '%Y-%m-%d %H:%M:%S') -> str:
    """格式化日期时间"""
    if dt is None:
        return ''
    return dt.strftime(format_str)

def parse_datetime(date_str: str, format_str: str = '%Y-%m-%d %H:%M:%S') -> Optional[datetime]:
    """解析日期时间字符串"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, format_str)
    except ValueError:
        return None

def get_timestamp() -> int:
    """获取当前时间戳"""
    return int(datetime.now().timestamp())

def is_valid_email(email: str) -> bool:
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone: str) -> bool:
    """验证手机号格式"""
    import re
    pattern = r'^1[3-9]\d{9}$'
    return re.match(pattern, phone) is not None

def paginate_query(query, page: int = 1, per_page: int = 10):
    """分页查询"""
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def build_response(code: int = 200, message: str = 'success', data: Any = None) -> Dict[str, Any]:
    """构建统一响应格式"""
    return {
        'code': code,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }

def build_error_response(code: int = 400, message: str = 'error', errors: Any = None) -> Dict[str, Any]:
    """构建错误响应格式"""
    return {
        'code': code,
        'message': message,
        'errors': errors,
        'timestamp': datetime.now().isoformat()
    }

def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """安全获取字典值"""
    return data.get(key, default)

def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """清理字典，移除None值"""
    return {k: v for k, v in data.items() if v is not None}

def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """合并多个字典"""
    result = {}
    for d in dicts:
        result.update(d)
    return result

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filename)[1].lower()

def is_allowed_file(filename: str, allowed_extensions: set) -> bool:
    """检查文件扩展名是否允许"""
    return get_file_extension(filename) in allowed_extensions

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def generate_random_string(length: int = 8) -> str:
    """生成随机字符串"""
    import string
    import random
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def mask_sensitive_data(data: str, mask_char: str = '*', visible_chars: int = 2) -> str:
    """掩码敏感数据"""
    if len(data) <= visible_chars:
        return mask_char * len(data)
    
    return data[:visible_chars] + mask_char * (len(data) - visible_chars)

def validate_json_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """验证JSON数据是否符合schema"""
    try:
        from jsonschema import validate
        validate(instance=data, schema=schema)
        return True
    except Exception:
        return False

def convert_to_dict(obj) -> Dict[str, Any]:
    """将对象转换为字典"""
    if hasattr(obj, 'to_dict'):
        return obj.to_dict()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return {}

def get_client_ip(request) -> str:
    """获取客户端IP地址"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def log_operation(user_id: int, operation: str, details: str = '', ip: str = '') -> None:
    """记录操作日志"""
    # TODO: 实现操作日志记录
    print(f"[{datetime.now()}] User {user_id} performed {operation}: {details} from {ip}")

def create_upload_folder(folder_path: str) -> bool:
    """创建上传文件夹"""
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return True
    except Exception:
        return False
