#!/usr/bin/env python3
"""
ExamSphere 考试管理系统启动脚本
"""
import os
import sys
from app import create_app, db
from app.models.log_config import LogConfig
from app.services.log_service import LogService


def init_log_configs():
    """初始化日志配置"""
    print("正在初始化日志配置...")
    
    default_configs = [
        {
            'config_key': 'LOG_LEVEL',
            'config_value': 'INFO',
            'description': '日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)'
        },
        {
            'config_key': 'LOG_MAX_SIZE',
            'config_value': '10485760',
            'description': '单个日志文件最大大小（字节），默认10MB'
        },
        {
            'config_key': 'LOG_BACKUP_COUNT',
            'config_value': '30',
            'description': '日志文件备份数量，默认保留30个'
        },
        {
            'config_key': 'LOG_FORMAT',
            'config_value': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'description': '日志格式'
        },
        {
            'config_key': 'LOG_ENABLE_FILE',
            'config_value': 'true',
            'description': '是否启用文件日志 (true/false)'
        },
        {
            'config_key': 'LOG_ENABLE_DATABASE',
            'config_value': 'false',
            'description': '是否启用数据库日志 (true/false)'
        },
        {
            'config_key': 'LOG_RETENTION_DAYS',
            'config_value': '30',
            'description': '日志保留天数'
        },
        {
            'config_key': 'LOG_ENABLE_CONSOLE',
            'config_value': 'true',
            'description': '是否启用控制台日志 (true/false)'
        },
        {
            'config_key': 'LOG_ENABLE_ERROR_FILE',
            'config_value': 'true',
            'description': '是否启用错误日志单独文件 (true/false)'
        },
        {
            'config_key': 'LOG_ENABLE_ROTATION',
            'config_value': 'true',
            'description': '是否启用日志轮转 (true/false)'
        }
    ]
    
    added_count = 0
    for config_data in default_configs:
        existing_config = LogConfig.query.filter_by(
            config_key=config_data['config_key']
        ).first()
        
        if not existing_config:
            config = LogConfig(
                config_key=config_data['config_key'],
                config_value=config_data['config_value'],
                description=config_data['description']
            )
            db.session.add(config)
            added_count += 1
    
    try:
        db.session.commit()
        if added_count > 0:
            print(f"✅ 成功添加 {added_count} 个日志配置")
        else:
            print("✅ 日志配置已存在，无需重复添加")
    except Exception as e:
        db.session.rollback()
        print(f"❌ 日志配置初始化失败: {e}")
        return False
    
    return True


def init_system_configs():
    """初始化系统配置"""
    print("正在初始化系统配置...")
    
    try:
        from app.models.system_config import SystemConfig
        
        default_configs = [
            {
                'config_key': 'system_name',
                'config_value': 'ExamSphere 考试管理系统',
                'config_type': 'string',
                'description': '系统名称'
            },
            {
                'config_key': 'system_version',
                'config_value': '1.0.0',
                'config_type': 'string',
                'description': '系统版本'
            },
            {
                'config_key': 'max_file_size',
                'config_value': '10485760',
                'config_type': 'number',
                'description': '最大文件上传大小（字节）'
            },
            {
                'config_key': 'exam_time_limit',
                'config_value': '120',
                'config_type': 'number',
                'description': '默认考试时长（分钟）'
            },
            {
                'config_key': 'enable_registration',
                'config_value': 'true',
                'config_type': 'boolean',
                'description': '是否允许用户注册'
            },
            {
                'config_key': 'enable_notifications',
                'config_value': 'true',
                'config_type': 'boolean',
                'description': '是否启用通知功能'
            }
        ]
        
        added_count = 0
        for config_data in default_configs:
            existing_config = SystemConfig.query.filter_by(
                config_key=config_data['config_key']
            ).first()
            
            if not existing_config:
                config = SystemConfig(
                    config_key=config_data['config_key'],
                    config_value=config_data['config_value'],
                    config_type=config_data['config_type'],
                    description=config_data['description']
                )
                db.session.add(config)
                added_count += 1
        
        db.session.commit()
        if added_count > 0:
            print(f"✅ 成功添加 {added_count} 个系统配置")
        else:
            print("✅ 系统配置已存在，无需重复添加")
            
    except Exception as e:
        print(f"⚠️ 系统配置初始化跳过: {e}")
    
    return True


def init_default_admin():
    """初始化默认管理员账户"""
    print("正在检查默认管理员账户...")
    
    try:
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@examsphere.com',
                password_hash=generate_password_hash('admin123'),
                real_name='系统管理员',
                role='admin',
                status='active'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("✅ 成功创建默认管理员账户 (用户名: admin, 密码: admin123)")
        else:
            print("✅ 默认管理员账户已存在")
            
    except Exception as e:
        print(f"⚠️ 默认管理员账户初始化跳过: {e}")
    
    return True


def setup_logging():
    """设置日志系统"""
    print("正在设置日志系统...")
    
    try:
        LogService.setup_logging()
        print("✅ 日志系统设置成功")
        return True
    except Exception as e:
        print(f"❌ 日志系统设置失败: {e}")
        return False


def check_database_connection():
    """检查数据库连接"""
    print("正在检查数据库连接...")
    
    try:
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        print("✅ 数据库连接正常")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("💡 请检查以下配置：")
        print("   1. 确保MySQL服务已启动")
        print("   2. 检查.env文件中的DATABASE_URL配置")
        print("   3. 确认数据库用户名和密码正确")
        print("   4. 确认数据库'examsphere'已创建")
        print("   5. 检查数据库用户权限")
        return False


def initialize_system():
    """系统初始化"""
    print("🚀 开始初始化 ExamSphere 考试管理系统...")
    print("=" * 50)
    
    # 检查数据库连接
    if not check_database_connection():
        print("❌ 数据库连接失败，请检查数据库配置")
        return False
    
    # 创建数据库表
    print("正在创建数据库表...")
    try:
        db.create_all()
        print("✅ 数据库表创建成功")
    except Exception as e:
        print(f"❌ 数据库表创建失败: {e}")
        return False
    
    # 初始化系统配置
    init_system_configs()
    
    # 初始化日志配置
    if not init_log_configs():
        print("⚠️ 日志配置初始化失败，但系统将继续启动")
    
    # 初始化默认管理员
    init_default_admin()
    
    # 设置日志系统
    setup_logging()
    
    print("=" * 50)
    print("✅ ExamSphere 系统初始化完成！")
    print("📝 默认管理员账户: admin / admin123")
    print("🌐 系统访问地址: http://localhost:5000")
    print("=" * 50)
    
    return True


app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Shell 上下文处理器"""
    return {
        'db': db,
        'app': app
    }

if __name__ == '__main__':
    # 系统初始化
    with app.app_context():
        if not initialize_system():
            print("❌ 系统初始化失败，程序退出")
            sys.exit(1)
    
    # 启动应用
    print("🚀 启动 ExamSphere 考试管理系统...")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )

