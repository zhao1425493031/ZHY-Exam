# 数据库迁移脚本
import os
import sys
from flask_migrate import Migrate, MigrateCommand, init, migrate, upgrade
from flask.cli import FlaskGroup
from app import create_app, db

def create_cli():
    """创建CLI命令组"""
    app = create_app()
    migrate = Migrate(app, db)
    
    cli = FlaskGroup(app)
    cli.add_command('db', MigrateCommand)
    
    return cli

def init_migration():
    """初始化迁移"""
    try:
        app = create_app()
        with app.app_context():
            init()
            print("迁移初始化成功")
            return True
    except Exception as e:
        print(f"迁移初始化失败: {e}")
        return False

def create_migration(message="Initial migration"):
    """创建迁移"""
    try:
        app = create_app()
        with app.app_context():
            migrate(message=message)
            print(f"迁移文件创建成功: {message}")
            return True
    except Exception as e:
        print(f"创建迁移失败: {e}")
        return False

def upgrade_database():
    """升级数据库"""
    try:
        app = create_app()
        with app.app_context():
            upgrade()
            print("数据库升级成功")
            return True
    except Exception as e:
        print(f"数据库升级失败: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python migrate.py [init|create|upgrade] [message]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'init':
        if not init_migration():
            sys.exit(1)
    elif command == 'create':
        message = sys.argv[2] if len(sys.argv) > 2 else "Auto migration"
        if not create_migration(message):
            sys.exit(1)
    elif command == 'upgrade':
        if not upgrade_database():
            sys.exit(1)
    else:
        print("未知命令")
        sys.exit(1)

if __name__ == '__main__':
    main()

