#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于创建数据库和表结构
"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def get_database_config():
    """获取数据库配置"""
    # 从环境变量获取数据库配置
    database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost:3306/exam_system')
    
    # 解析数据库URL
    if '://' in database_url:
        # 格式: mysql+pymysql://username:password@host:port/database
        parts = database_url.split('://')[1]
        if '@' in parts:
            auth, host_db = parts.split('@')
            username, password = auth.split(':')
            if ':' in host_db:
                host, port_db = host_db.split(':')
                if '/' in port_db:
                    port, database = port_db.split('/')
                else:
                    port = port_db
                    database = 'exam_system'
            else:
                host = host_db.split('/')[0]
                port = 3306
                database = host_db.split('/')[1] if '/' in host_db else 'exam_system'
        else:
            username = 'root'
            password = 'password'
            host = 'localhost'
            port = 3306
            database = 'exam_system'
    else:
        # 默认配置
        username = 'root'
        password = 'password'
        host = 'localhost'
        port = 3306
        database = 'exam_system'
    
    return {
        'host': host,
        'port': int(port),
        'user': username,
        'password': password,
        'database': database
    }

def create_database():
    """创建数据库"""
    config = get_database_config()
    database_name = config['database']
    
    # 连接MySQL服务器（不指定数据库）
    connection = pymysql.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # 创建数据库
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ 数据库 {database_name} 创建成功")
            
            # 使用数据库
            cursor.execute(f"USE {database_name}")
            
            # 创建表
            create_tables(cursor)
            
        connection.commit()
        print("✅ 数据库初始化完成")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False
    finally:
        connection.close()
    
    return True

def create_tables(cursor):
    """创建表结构"""
    
    # 用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            password_hash VARCHAR(128) NOT NULL,
            role ENUM('admin', 'user') DEFAULT 'user',
            is_verified BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 用户表创建成功")
    
    # 验证码表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_codes (
            id INT PRIMARY KEY AUTO_INCREMENT,
            email VARCHAR(120) NOT NULL,
            code VARCHAR(6) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            is_used BOOLEAN DEFAULT FALSE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 验证码表创建成功")
    
    # 题目表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            content TEXT NOT NULL,
            type ENUM('single', 'multiple', 'text', 'audio', 'video') NOT NULL,
            options JSON,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 题目表创建成功")
    
    # 考试表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exams (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            time_limit INT DEFAULT 60,
            total_questions INT DEFAULT 50,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 考试表创建成功")
    
    # 考试记录表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_records (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            exam_id INT NOT NULL,
            score INT DEFAULT 0,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            status ENUM('in_progress', 'completed', 'timeout') DEFAULT 'in_progress',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 考试记录表创建成功")
    
    # 答题记录表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INT PRIMARY KEY AUTO_INCREMENT,
            exam_record_id INT NOT NULL,
            question_id INT NOT NULL,
            user_answer TEXT,
            is_correct BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (exam_record_id) REFERENCES exam_records(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 答题记录表创建成功")
    
    # 错题表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wrong_questions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            question_id INT NOT NULL,
            exam_record_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
            FOREIGN KEY (exam_record_id) REFERENCES exam_records(id) ON DELETE CASCADE,
            UNIQUE KEY uk_user_question (user_id, question_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 错题表创建成功")
    
    # 收藏题目表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorite_questions (
            id INT PRIMARY KEY AUTO_INCREMENT,
            user_id INT NOT NULL,
            question_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
            UNIQUE KEY uk_user_question (user_id, question_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
    """)
    print("✅ 收藏题目表创建成功")

def create_default_admin():
    """创建默认管理员用户"""
    config = get_database_config()
    
    connection = pymysql.connect(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            # 检查管理员用户是否已存在
            cursor.execute("SELECT id FROM users WHERE email = 'admin@example.com'")
            if cursor.fetchone():
                print("✅ 管理员用户已存在")
                return
            
            # 创建管理员用户
            from werkzeug.security import generate_password_hash
            password_hash = generate_password_hash('admin123')
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role, is_verified) 
                VALUES (%s, %s, %s, %s, %s)
            """, ('admin', 'admin@example.com', password_hash, 'admin', True))
            
            connection.commit()
            print("✅ 默认管理员用户创建成功: admin@example.com / admin123")
            
    except Exception as e:
        print(f"❌ 创建管理员用户失败: {e}")
    finally:
        connection.close()

def main():
    """主函数"""
    print("🚀 开始初始化数据库...")
    
    try:
        # 创建数据库和表
        if create_database():
            # 创建默认管理员用户
            create_default_admin()
            print("\n🎉 数据库初始化完成！")
            print("📋 默认管理员账号: admin@example.com")
            print("🔑 默认管理员密码: admin123")
        else:
            print("\n❌ 数据库初始化失败！")
            
    except Exception as e:
        print(f"\n❌ 初始化过程中出现错误: {e}")

if __name__ == '__main__':
    main()
