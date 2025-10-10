# 数据库初始化脚本
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def create_database():
    """创建数据库"""
    try:
        # 从环境变量获取数据库配置
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '3306')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'examsphere')
        
        # 创建数据库连接（不指定数据库名）
        engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/')
        
        # 检查数据库是否存在
        with engine.connect() as conn:
            result = conn.execute(text(f"SHOW DATABASES LIKE '{db_name}'"))
            if result.fetchone():
                print(f"数据库 '{db_name}' 已存在")
                return True
            
            # 创建数据库
            conn.execute(text(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"数据库 '{db_name}' 创建成功")
            return True
            
    except SQLAlchemyError as e:
        print(f"创建数据库失败: {e}")
        return False
    except Exception as e:
        print(f"未知错误: {e}")
        return False

def create_tables():
    """创建数据表"""
    try:
        from app import create_app, db
        
        app = create_app()
        with app.app_context():
            # 创建所有表
            db.create_all()
            print("数据表创建成功")
            return True
            
    except Exception as e:
        print(f"创建数据表失败: {e}")
        return False

def insert_initial_data():
    """插入初始数据"""
    try:
        from app import create_app, db
        from app.models.user import User
        
        app = create_app()
        with app.app_context():
            # 检查是否已有管理员用户
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                print("管理员用户已存在")
                return True
            
            # 创建默认管理员用户
            admin = User(
                username='admin',
                email='admin@examsphere.com',
                real_name='系统管理员',
                role='admin',
                status='active'
            )
            admin.set_password('admin123')
            
            db.session.add(admin)
            db.session.commit()
            
            print("默认管理员用户创建成功")
            print("用户名: admin")
            print("密码: admin123")
            print("请及时修改默认密码！")
            return True
            
    except Exception as e:
        print(f"插入初始数据失败: {e}")
        return False

def main():
    """主函数"""
    print("开始初始化数据库...")
    
    # 创建数据库
    if not create_database():
        sys.exit(1)
    
    # 创建数据表
    if not create_tables():
        sys.exit(1)
    
    # 插入初始数据
    if not insert_initial_data():
        sys.exit(1)
    
    print("数据库初始化完成！")

if __name__ == '__main__':
    main()

