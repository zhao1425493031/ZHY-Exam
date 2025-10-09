#!/usr/bin/env python3
"""
ExamSphere 考试管理系统启动脚本
"""
import os
from app import create_app, db

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Shell 上下文处理器"""
    return {
        'db': db,
        'app': app
    }

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 启动应用
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )
