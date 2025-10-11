# ExamSphere 考试管理系统开发规范

## 1. 项目概述

### 1.1 项目简介
ExamSphere 是一个基于 Web 的在线考试管理系统，支持用户管理、科目管理、试题管理、考试管理等功能。

### 1.2 技术架构
- **前端**: Vue 3 + JavaScript + Element Plus + Pinia
- **后端**: Python Flask + SQLAlchemy + Flask-RESTful
- **数据库**: MySQL 8.0+
- **部署**: Apache HTTPD (Windows/Linux)

## 2. 功能需求

### 2.1 用户管理模块
- 用户注册/登录/登出
- 用户信息管理（个人资料、密码修改）
- 用户角色管理（管理员、普通用户）
- 用户权限控制

### 2.2 科目管理模块
- 科目创建、编辑、删除
- 科目分类管理
- 科目状态管理（启用/禁用）
- 科目收费设置（免费/收费）
- 科目价格管理

### 2.3 试题管理模块
- 试题创建（单选、多选、判断、填空、简答）
- 试题分类和标签
- 试题难度等级
- 试题导入/导出
- 试题审核流程

### 2.4 考试管理模块
- 考试创建和配置
- 考试时间控制
- 随机组卷
- 考试监控
- 考试结果统计

### 2.5 考试履历模块
- 考试记录查询
- 成绩统计和分析
- 错题记录和复习
- 学习进度跟踪

### 2.6 前台用户功能
- 在线考试
- 题目收藏
- 考试结果查看
- 重复考试
- 错题自动记录
- 学习报告

### 2.7 管理员功能模块
- 用户管理（创建、编辑、删除用户）
- 科目管理（创建、编辑、删除科目）
- 试题管理（创建、编辑、删除试题）
- 考试管理（创建、编辑、删除考试）
- 题库管理（试题分类、标签管理）
- 考试创建（手动组卷、随机组卷）
- 考试分析（成绩统计、数据分析）
- 系统参数配置
- 数据备份与恢复
- 系统日志管理
- 操作日志记录
- 系统监控面板

### 2.8 消息通知模块
- 站内消息系统
- 邮件通知功能
- 考试提醒通知
- 成绩发布通知
- 系统公告管理

### 2.9 文件管理模块
- 文件上传下载
- 图片资源管理
- 试题附件管理
- 用户头像上传
- 文件存储管理

### 2.10 统计分析模块
- 考试数据统计
- 用户行为分析
- 试题难度分析
- 成绩分布统计
- 学习效果评估
- 仪表盘统计展示
- 多维度数据分析
- 图表可视化展示
- 数据筛选和查询
- 个人学习统计

### 2.11 防作弊模块
- 考试时间限制
- 切屏检测
- 答题时间监控
- 异常行为记录
- 考试环境检测

### 2.12 移动端适配
- 响应式设计
- 移动端考试
- 触屏操作优化
- 离线缓存支持

### 2.13 权限管理模块
- 角色权限配置（管理员、普通用户）
- 菜单权限控制
- 按钮权限控制
- 数据权限过滤
- 权限继承机制
- 细粒度权限控制
- 权限分配管理
- 权限验证机制

### 2.14 数据导入导出模块
- Excel 批量导入用户
- 试题批量导入导出
- 考试结果导出
- 统计分析数据导出
- 模板下载功能
- 导入记录管理
- 数据验证和清洗
- 批量操作支持
- 导入进度跟踪
- 错误处理和回滚

### 2.15 考试模板模块
- 考试模板创建
- 模板复用功能
- 模板分类管理
- 快速组卷功能
- 模板分享机制

### 2.16 学习路径模块
- 学习计划制定
- 知识点关联
- 学习进度跟踪
- 个性化推荐
- 学习路径优化

### 2.17 在线答疑模块
- 实时聊天功能
- 问题分类管理
- 管理员在线答疑
- 常见问题库
- 答疑记录统计

### 2.18 收费课程模块
- 课程收费设置（免费/收费）
- 课程价格管理
- 用户购买记录
- 支付方式管理（支付宝、微信、PayPal、联系管理员）
- 订单管理
- 退款处理

### 2.19 支付管理模块
- 支付接口集成（支付宝、微信、PayPal）
- 支付状态跟踪
- 支付回调处理
- 订单状态管理
- 支付记录查询
- 退款申请处理

### 2.20 日志管理模块
- 系统日志记录（操作日志、错误日志、访问日志）
- 日志按日期自动分割
- 日志文件大小控制（超过指定大小自动分割）
- 日志保留策略配置
- 敏感信息自动脱敏
- 日志查询和分析功能
- 日志备份和清理
- 日志级别配置（DEBUG、INFO、WARNING、ERROR、CRITICAL）

#### 2.20.1 日志使用方式

**装饰器方式（推荐）**：
```python
from app.utils.log_decorators import log_operation, log_api_access, log_user_action

# 记录操作日志
@log_operation('USER_LOGIN', '用户登录')
def login():
    # 登录逻辑
    pass

# 记录API访问日志
@log_api_access()
def api_endpoint():
    # API逻辑
    pass

# 记录用户行为日志
@log_user_action('EXAM_START', '开始考试')
def start_exam():
    # 考试开始逻辑
    pass
```

**直接调用方式**：
```python
from app.services.log_service import LogService

# 记录日志到数据库
LogService.log_to_database(
    level='INFO',
    module='USER_MANAGEMENT',
    message='用户创建成功',
    user_id=1,
    ip_address='192.168.1.100',
    execution_time=0.5
)
```

**Python标准日志**：
```python
import logging

# 获取日志器
logger = logging.getLogger(__name__)

# 记录日志
logger.info('这是一条信息日志')
logger.warning('这是一条警告日志')
logger.error('这是一条错误日志')
```

**日志配置管理**：
```python
from app.services.log_service import LogConfigService

# 获取所有日志配置
configs = LogConfigService.get_all_configs()

# 更新日志配置
LogConfigService.update_config('LOG_LEVEL', 'DEBUG')

# 重新设置日志系统
LogService.setup_logging()
```

**日志查询和分析**：
```python
from app.services.log_service import LogService

# 获取日志列表
logs = LogService.get_logs(
    page=1,
    per_page=20,
    level='ERROR',
    module='AUTH',
    start_date='2024-01-01',
    end_date='2024-01-31'
)

# 搜索日志
search_results = LogService.search_logs('登录失败')

# 获取日志统计
stats = LogService.get_log_statistics()

# 清理旧日志
deleted_count = LogService.cleanup_old_logs(days=30)
```

#### 2.20.2 日志文件位置
- **应用日志**: `backend/logs/examsphere.log`
- **错误日志**: `backend/logs/error.log`
- **日志备份**: `backend/logs/examsphere.log.2024-01-01` 等

#### 2.20.3 日志配置参数
```env
# 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# 单个日志文件最大大小（字节）
LOG_MAX_SIZE=10485760

# 日志文件备份数量
LOG_BACKUP_COUNT=30

# 日志格式
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# 是否启用文件日志
LOG_ENABLE_FILE=true

# 是否启用数据库日志
LOG_ENABLE_DATABASE=true

# 日志保留天数
LOG_RETENTION_DAYS=30

# 是否启用控制台日志
LOG_ENABLE_CONSOLE=true

# 是否启用错误日志单独文件
LOG_ENABLE_ERROR_FILE=true

# 是否启用日志轮转
LOG_ENABLE_ROTATION=true
```

## 3. 技术规范

### 3.1 后端技术栈

#### 3.1.1 核心框架
```python
# requirements.txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-RESTful==0.3.10
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
```

#### 3.1.2 数据库相关
```python
PyMySQL==1.1.0
SQLAlchemy==2.0.21
Alembic==1.12.0
```

#### 3.1.3 工具库
```python
python-dotenv==1.0.0
marshmallow==3.20.1
celery==5.3.2
redis==5.0.1
```

#### 3.1.4 支付相关库
```python
# 支付宝支付
alipay-sdk-python==3.7.0

# 微信支付
wechatpay-python==1.2.0

# PayPal支付
paypalrestsdk==1.13.3

# 加密和签名
cryptography==41.0.4
pycryptodome==3.19.0

# HTTP请求
requests==2.31.0
urllib3==2.0.7
```

### 3.2 前端技术栈

#### 3.2.1 核心框架
```json
{
  "vue": "^3.3.4",
  "@vue/cli-service": "^5.0.8",
  "pinia": "^2.1.6",
  "vue-router": "^4.2.4"
}
```

#### 3.2.2 UI 组件库
```json
{
  "element-plus": "^2.3.8",
  "@element-plus/icons-vue": "^2.1.0"
}
```

#### 3.2.3 工具库
```json
{
  "axios": "^1.4.0",
  "dayjs": "^1.11.9",
  "lodash": "^4.17.21"
}
```

## 4. 项目结构规范

### 4.1 后端项目结构
```
backend/
├── app/
│   ├── __init__.py
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── subject.py
│   │   ├── question.py
│   │   ├── exam.py
│   │   └── exam_record.py
│   ├── api/                    # API 接口
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── subjects.py
│   │   ├── questions.py
│   │   ├── exams.py
│   │   └── exam_records.py
│   ├── services/               # 业务逻辑
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── exam_service.py
│   │   └── question_service.py
│   ├── utils/                  # 工具函数
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   └── helpers.py
│   ├── config/                 # 配置文件
│   │   ├── __init__.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   └── migrations/             # 数据库迁移
├── tests/                      # 测试文件
├── requirements.txt
├── .env.example
├── .gitignore
└── run.py
```

### 4.2 前端项目结构
```
frontend/
├── public/
├── src/
│   ├── api/                    # API 接口
│   │   ├── index.js
│   │   ├── auth.js
│   │   ├── users.js
│   │   ├── subjects.js
│   │   ├── questions.js
│   │   ├── exams.js
│   │   └── exam_records.js
│   ├── components/             # 公共组件
│   │   ├── common/
│   │   │   ├── BaseTable.vue
│   │   │   ├── BaseForm.vue
│   │   │   ├── BaseDialog.vue
│   │   │   └── BasePagination.vue
│   │   ├── layout/
│   │   │   ├── AppLayout.vue   # 主布局组件（包含导航栏）
│   │   │   ├── Header.vue
│   │   │   ├── Sidebar.vue
│   │   │   └── Footer.vue
│   │   └── exam/
│   │       ├── QuestionCard.vue
│   │       ├── Timer.vue
│   │       └── AnswerSheet.vue
│   ├── views/                  # 页面组件
│   │   ├── auth/
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── admin/
│   │   │   ├── UserManagement.vue
│   │   │   ├── SubjectManagement.vue
│   │   │   ├── QuestionManagement.vue
│   │   │   ├── ExamManagement.vue
│   │   │   ├── QuestionBank.vue
│   │   │   ├── ExamCreation.vue
│   │   │   └── ExamAnalysis.vue
│   │   └── user/
│   │       ├── ExamList.vue
│   │       ├── ExamTaking.vue
│   │       ├── ExamResult.vue
│   │       └── MyRecords.vue
│   ├── stores/                 # Pinia 状态管理
│   │   ├── index.js
│   │   ├── auth.js
│   │   ├── user.js
│   │   ├── exam.js
│   │   └── question.js
│   ├── router/                 # 路由配置
│   │   ├── index.js
│   │   ├── admin.js
│   │   ├── student.js
│   │   └── teacher.js
│   ├── utils/                  # 工具函数
│   │   ├── request.js
│   │   ├── auth.js
│   │   ├── storage.js
│   │   ├── format.js
│   │   └── validation.js
│   ├── styles/                 # 样式文件
│   │   ├── index.scss
│   │   ├── variables.scss
│   │   └── mixins.scss
│   ├── App.vue
│   └── main.js
├── package.json
├── vue.config.js
└── .env.example
```

## 5. 数据库设计

### 5.1 用户表 (users)
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    real_name VARCHAR(50),
    role ENUM('admin', 'user') DEFAULT 'user',
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active',
    avatar_url VARCHAR(255),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.2 科目表 (subjects)
```sql
CREATE TABLE subjects (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(50),
    status ENUM('active', 'inactive') DEFAULT 'active',
    is_free BOOLEAN DEFAULT TRUE COMMENT '是否免费',
    price DECIMAL(10,2) DEFAULT 0.00 COMMENT '价格（元）',
    original_price DECIMAL(10,2) DEFAULT 0.00 COMMENT '原价（元）',
    discount_rate DECIMAL(5,2) DEFAULT 100.00 COMMENT '折扣率（%）',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.3 试题表 (questions)
```sql
CREATE TABLE questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    subject_id INT NOT NULL,
    type ENUM('single', 'multiple', 'judge', 'fill', 'essay') NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    options JSON,
    answer TEXT NOT NULL,
    explanation TEXT,
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
    tags JSON,
    points INT DEFAULT 1,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 5.4 考试表 (exams)
```sql
CREATE TABLE exams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    subject_id INT NOT NULL,
    description TEXT,
    duration INT NOT NULL COMMENT '考试时长(分钟)',
    total_points INT NOT NULL,
    question_count INT NOT NULL,
    question_ids JSON NOT NULL COMMENT '试题ID列表',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status ENUM('draft', 'published', 'ongoing', 'finished', 'cancelled') DEFAULT 'draft',
    settings JSON COMMENT '考试设置',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 5.5 考试记录表 (exam_records)
```sql
CREATE TABLE exam_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exam_id INT NOT NULL,
    user_id INT NOT NULL,
    start_time TIMESTAMP,
    submit_time TIMESTAMP,
    answers JSON COMMENT '用户答案',
    score DECIMAL(5,2),
    status ENUM('in_progress', 'submitted', 'timeout', 'cancelled') DEFAULT 'in_progress',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE KEY unique_exam_user (exam_id, user_id)
);
```

### 5.6 用户收藏表 (user_favorites)
```sql
CREATE TABLE user_favorites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (question_id) REFERENCES questions(id),
    UNIQUE KEY unique_user_question (user_id, question_id)
);
```

### 5.7 错题记录表 (wrong_answers)
```sql
CREATE TABLE wrong_answers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    exam_record_id INT,
    user_answer TEXT,
    correct_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (exam_record_id) REFERENCES exam_records(id)
);
```

### 5.8 系统配置表 (system_configs)
```sql
CREATE TABLE system_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT,
    config_type ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.9 消息通知表 (notifications)
```sql
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    type ENUM('system', 'exam', 'score', 'announcement') DEFAULT 'system',
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 5.10 文件管理表 (files)
```sql
CREATE TABLE files (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INT NOT NULL,
    file_type VARCHAR(100),
    uploader_id INT NOT NULL,
    related_type VARCHAR(50) COMMENT 'question, user, exam等',
    related_id INT COMMENT '关联记录ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploader_id) REFERENCES users(id)
);
```

### 5.11 操作日志表 (operation_logs)
```sql
CREATE TABLE operation_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    operation_type VARCHAR(50) NOT NULL,
    operation_desc TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_data JSON,
    response_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 5.12 考试监控表 (exam_monitoring)
```sql
CREATE TABLE exam_monitoring (
    id INT PRIMARY KEY AUTO_INCREMENT,
    exam_record_id INT NOT NULL,
    event_type ENUM('start', 'pause', 'resume', 'submit', 'timeout', 'cheat') NOT NULL,
    event_data JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (exam_record_id) REFERENCES exam_records(id)
);
```

### 5.13 系统公告表 (announcements)
```sql
CREATE TABLE announcements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    type ENUM('system', 'exam', 'maintenance') DEFAULT 'system',
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    publish_time TIMESTAMP,
    expire_time TIMESTAMP,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 5.14 权限表 (permissions)
```sql
CREATE TABLE permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(100) UNIQUE NOT NULL,
    type ENUM('menu', 'button', 'api', 'data') DEFAULT 'menu',
    parent_id INT DEFAULT 0,
    path VARCHAR(200),
    icon VARCHAR(100),
    sort_order INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES permissions(id)
);
```

### 5.15 角色权限关联表 (role_permissions)
```sql
CREATE TABLE role_permissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    role VARCHAR(50) NOT NULL,
    permission_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (permission_id) REFERENCES permissions(id),
    UNIQUE KEY unique_role_permission (role, permission_id)
);
```

### 5.16 考试模板表 (exam_templates)
```sql
CREATE TABLE exam_templates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    subject_id INT NOT NULL,
    template_config JSON NOT NULL COMMENT '模板配置',
    question_rules JSON COMMENT '选题规则',
    is_public BOOLEAN DEFAULT FALSE,
    usage_count INT DEFAULT 0,
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 5.17 学习路径表 (learning_paths)
```sql
CREATE TABLE learning_paths (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    subject_id INT NOT NULL,
    path_config JSON NOT NULL COMMENT '学习路径配置',
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    estimated_hours INT DEFAULT 0,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 5.18 用户学习路径表 (user_learning_paths)
```sql
CREATE TABLE user_learning_paths (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    learning_path_id INT NOT NULL,
    progress JSON COMMENT '学习进度',
    current_step INT DEFAULT 0,
    completed_steps JSON COMMENT '已完成步骤',
    start_time TIMESTAMP,
    completion_time TIMESTAMP,
    status ENUM('in_progress', 'completed', 'paused', 'abandoned') DEFAULT 'in_progress',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (learning_path_id) REFERENCES learning_paths(id),
    UNIQUE KEY unique_user_path (user_id, learning_path_id)
);
```

### 5.19 在线答疑表 (qa_sessions)
```sql
CREATE TABLE qa_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    teacher_id INT,
    subject_id INT NOT NULL,
    question_title VARCHAR(200) NOT NULL,
    question_content TEXT NOT NULL,
    answer_content TEXT,
    status ENUM('pending', 'answered', 'closed') DEFAULT 'pending',
    priority ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium',
    category VARCHAR(100),
    tags JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    answered_at TIMESTAMP,
    closed_at TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (teacher_id) REFERENCES users(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);
```

### 5.21 用户购买记录表 (user_purchases)
```sql
CREATE TABLE user_purchases (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    order_id VARCHAR(50) UNIQUE NOT NULL COMMENT '订单号',
    payment_method ENUM('alipay', 'wechat', 'paypal', 'admin') NOT NULL COMMENT '支付方式',
    amount DECIMAL(10,2) NOT NULL COMMENT '支付金额',
    original_amount DECIMAL(10,2) NOT NULL COMMENT '原价',
    discount_amount DECIMAL(10,2) DEFAULT 0.00 COMMENT '优惠金额',
    status ENUM('pending', 'paid', 'cancelled', 'refunded') DEFAULT 'pending' COMMENT '支付状态',
    payment_time TIMESTAMP NULL COMMENT '支付时间',
    expire_time TIMESTAMP NULL COMMENT '到期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.22 支付订单表 (payment_orders)
```sql
CREATE TABLE payment_orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id VARCHAR(50) UNIQUE NOT NULL COMMENT '订单号',
    user_id INT NOT NULL,
    subject_id INT NOT NULL,
    payment_method ENUM('alipay', 'wechat', 'paypal', 'admin') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'CNY' COMMENT '货币类型',
    status ENUM('pending', 'paid', 'cancelled', 'refunded', 'failed') DEFAULT 'pending',
    third_party_order_id VARCHAR(100) COMMENT '第三方支付订单号',
    payment_url TEXT COMMENT '支付链接',
    callback_data JSON COMMENT '支付回调数据',
    paid_at TIMESTAMP NULL COMMENT '支付完成时间',
    expired_at TIMESTAMP NULL COMMENT '订单过期时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.23 退款记录表 (refund_records)
```sql
CREATE TABLE refund_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id VARCHAR(50) NOT NULL,
    user_id INT NOT NULL,
    refund_amount DECIMAL(10,2) NOT NULL COMMENT '退款金额',
    refund_reason TEXT COMMENT '退款原因',
    refund_method ENUM('alipay', 'wechat', 'paypal', 'manual') NOT NULL COMMENT '退款方式',
    status ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending',
    admin_id INT COMMENT '处理管理员ID',
    admin_note TEXT COMMENT '管理员备注',
    processed_at TIMESTAMP NULL COMMENT '处理时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.24 优惠券表 (coupons)
```sql
CREATE TABLE coupons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) UNIQUE NOT NULL COMMENT '优惠券代码',
    name VARCHAR(100) NOT NULL COMMENT '优惠券名称',
    type ENUM('percentage', 'fixed') NOT NULL COMMENT '优惠类型：百分比/固定金额',
    value DECIMAL(10,2) NOT NULL COMMENT '优惠值',
    min_amount DECIMAL(10,2) DEFAULT 0.00 COMMENT '最低消费金额',
    max_discount DECIMAL(10,2) DEFAULT 0.00 COMMENT '最大优惠金额',
    usage_limit INT DEFAULT 1 COMMENT '使用次数限制',
    used_count INT DEFAULT 0 COMMENT '已使用次数',
    valid_from TIMESTAMP NOT NULL COMMENT '有效期开始',
    valid_to TIMESTAMP NOT NULL COMMENT '有效期结束',
    status ENUM('active', 'inactive', 'expired') DEFAULT 'active',
    created_by INT NOT NULL COMMENT '创建者ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 5.25 用户优惠券表 (user_coupons)
```sql
CREATE TABLE user_coupons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    coupon_id INT NOT NULL,
    order_id VARCHAR(50) COMMENT '使用的订单号',
    used_at TIMESTAMP NULL COMMENT '使用时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_coupon (user_id, coupon_id)
);
```

### 5.26 系统日志表 (system_logs)
```sql
CREATE TABLE system_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    log_level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL,
    module VARCHAR(100) NOT NULL COMMENT '模块名称',
    message TEXT NOT NULL COMMENT '日志消息',
    user_id INT COMMENT '操作用户ID',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    request_data JSON COMMENT '请求数据',
    response_data JSON COMMENT '响应数据',
    execution_time DECIMAL(10,3) COMMENT '执行时间(秒)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_log_level (log_level),
    INDEX idx_module (module),
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### 5.27 日志配置表 (log_configs)
```sql
CREATE TABLE log_configs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL COMMENT '配置键',
    config_value TEXT NOT NULL COMMENT '配置值',
    description TEXT COMMENT '配置描述',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 6. API 接口规范

### 6.1 统一响应格式
```json
{
    "code": 200,
    "message": "success",
    "data": {},
    "timestamp": "2023-12-01T10:00:00Z"
}
```

### 6.2 错误码规范
```python
# 成功
SUCCESS = 200

# 客户端错误
BAD_REQUEST = 400
UNAUTHORIZED = 401
FORBIDDEN = 403
NOT_FOUND = 404
VALIDATION_ERROR = 422

# 服务器错误
INTERNAL_ERROR = 500
DATABASE_ERROR = 501
```

### 6.3 认证接口
```python
# POST /api/auth/login
{
    "username": "string",
    "password": "string"
}

# POST /api/auth/register
{
    "username": "string",
    "email": "string",
    "password": "string",
    "real_name": "string",
    "role": "user"
}

# POST /api/auth/logout
# GET /api/auth/profile
# PUT /api/auth/profile
```

### 6.4 用户管理接口
```python
# GET /api/users?page=1&size=10&role=user
# POST /api/users
# GET /api/users/{id}
# PUT /api/users/{id}
# DELETE /api/users/{id}
```

### 6.5 科目管理接口
```python
# GET /api/subjects
# POST /api/subjects
# GET /api/subjects/{id}
# PUT /api/subjects/{id}
# DELETE /api/subjects/{id}
```

### 6.6 试题管理接口
```python
# GET /api/questions?subject_id=1&type=single&page=1&size=10
# POST /api/questions
# GET /api/questions/{id}
# PUT /api/questions/{id}
# DELETE /api/questions/{id}
# POST /api/questions/batch-import
```

### 6.7 考试管理接口
```python
# GET /api/exams?status=published&page=1&size=10
# POST /api/exams
# GET /api/exams/{id}
# PUT /api/exams/{id}
# DELETE /api/exams/{id}
# POST /api/exams/{id}/start
# POST /api/exams/{id}/submit
```

### 6.8 考试记录接口
```python
# GET /api/exam-records?user_id=1&page=1&size=10
# GET /api/exam-records/{id}
# GET /api/exam-records/{id}/answers
```

### 6.9 系统管理接口
```python
# GET /api/system/configs
# PUT /api/system/configs/{key}
# GET /api/system/logs?page=1&size=10
# POST /api/system/backup
# POST /api/system/restore
```

### 6.10 消息通知接口
```python
# GET /api/notifications?page=1&size=10
# POST /api/notifications
# PUT /api/notifications/{id}/read
# DELETE /api/notifications/{id}
```

### 6.11 文件管理接口
```python
# POST /api/files/upload
# GET /api/files/{id}
# DELETE /api/files/{id}
# GET /api/files?related_type=question&related_id=1
```

### 6.12 统计分析接口
```python
# GET /api/statistics/exam-data
# GET /api/statistics/user-behavior
# GET /api/statistics/question-analysis
# GET /api/statistics/score-distribution
```

### 6.13 考试监控接口
```python
# POST /api/exam-monitoring/events
# GET /api/exam-monitoring/{exam_record_id}/events
# GET /api/exam-monitoring/suspicious-behavior
```

### 6.14 系统公告接口
```python
# GET /api/announcements?status=published
# POST /api/announcements
# GET /api/announcements/{id}
# PUT /api/announcements/{id}
# DELETE /api/announcements/{id}
```

### 6.15 权限管理接口
```python
# GET /api/permissions
# POST /api/permissions
# PUT /api/permissions/{id}
# DELETE /api/permissions/{id}
# GET /api/role-permissions/{role}
# POST /api/role-permissions
# DELETE /api/role-permissions/{role}/{permission_id}
```

### 6.16 考试模板接口
```python
# GET /api/exam-templates?subject_id=1&is_public=true
# POST /api/exam-templates
# GET /api/exam-templates/{id}
# PUT /api/exam-templates/{id}
# DELETE /api/exam-templates/{id}
# POST /api/exam-templates/{id}/use
```

### 6.17 学习路径接口
```python
# GET /api/learning-paths?subject_id=1&difficulty=beginner
# POST /api/learning-paths
# GET /api/learning-paths/{id}
# PUT /api/learning-paths/{id}
# DELETE /api/learning-paths/{id}
# GET /api/user-learning-paths?user_id=1
# POST /api/user-learning-paths
# PUT /api/user-learning-paths/{id}/progress
```

### 6.18 在线答疑接口
```python
# GET /api/qa-sessions?student_id=1&status=pending
# POST /api/qa-sessions
# GET /api/qa-sessions/{id}
# PUT /api/qa-sessions/{id}/answer
# PUT /api/qa-sessions/{id}/close
# GET /api/qa-sessions/teacher/{teacher_id}
```

### 6.19 数据导入导出接口
```python
# POST /api/import/users
# POST /api/import/questions
# POST /api/import/subjects
# GET /api/import/records?type=users&page=1&size=10
# GET /api/export/users
# GET /api/export/questions
# GET /api/export/exam-results
# GET /api/export/statistics
```

### 6.20 收费课程接口
```python
# GET /api/subjects?is_free=false&page=1&size=10
# PUT /api/subjects/{id}/pricing
# GET /api/subjects/{id}/pricing-info
# POST /api/subjects/{id}/purchase
# GET /api/user-purchases?page=1&size=10
# GET /api/user-purchases/{id}
# POST /api/user-purchases/{id}/refund
```

### 6.21 支付管理接口
```python
# POST /api/payments/create-order
# POST /api/payments/alipay/callback
# POST /api/payments/wechat/callback
# POST /api/payments/paypal/callback
# GET /api/payments/orders?page=1&size=10
# GET /api/payments/orders/{order_id}
# PUT /api/payments/orders/{order_id}/status
# POST /api/payments/refund
# GET /api/payments/refunds?page=1&size=10
```

### 6.22 优惠券接口
```python
# GET /api/coupons?page=1&size=10
# POST /api/coupons
# GET /api/coupons/{id}
# PUT /api/coupons/{id}
# DELETE /api/coupons/{id}
# POST /api/coupons/validate
# GET /api/user-coupons?page=1&size=10
# POST /api/user-coupons/claim
```

### 6.23 日志管理接口
```python
# GET /api/logs?level=INFO&module=auth&page=1&size=10
# GET /api/logs/{id}
# POST /api/logs/search
# GET /api/log-configs
# PUT /api/log-configs/{key}
# POST /api/logs/cleanup
# GET /api/logs/statistics
```

#### 6.23.1 日志配置接口
```python
# 获取所有日志配置
GET /api/log-configs
Response: {
    "code": 200,
    "message": "获取日志配置成功",
    "data": [
        {
            "id": 1,
            "config_key": "LOG_LEVEL",
            "config_value": "INFO",
            "description": "日志级别",
            "is_active": true
        }
    ]
}

# 创建日志配置
POST /api/log-configs
Request: {
    "config_key": "LOG_LEVEL",
    "config_value": "DEBUG",
    "description": "日志级别"
}

# 更新日志配置
PUT /api/log-configs/{config_key}
Request: {
    "config_value": "ERROR",
    "description": "更新日志级别"
}
```

#### 6.23.2 日志查询接口
```python
# 获取日志列表
GET /api/logs?level=ERROR&module=auth&page=1&per_page=20&start_date=2024-01-01&end_date=2024-01-31
Response: {
    "code": 200,
    "message": "获取日志列表成功",
    "data": {
        "items": [
            {
                "id": 1,
                "log_level": "ERROR",
                "module": "AUTH",
                "message": "用户登录失败",
                "user_id": 1,
                "user_name": "admin",
                "ip_address": "192.168.1.100",
                "execution_time": 0.5,
                "created_at": "2024-01-01T10:00:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "per_page": 20,
        "pages": 5
    }
}

# 获取日志详情
GET /api/logs/{id}
Response: {
    "code": 200,
    "message": "获取日志详情成功",
    "data": {
        "id": 1,
        "log_level": "ERROR",
        "module": "AUTH",
        "message": "用户登录失败",
        "user_id": 1,
        "ip_address": "192.168.1.100",
        "request_data": {"username": "admin"},
        "response_data": {"error": "密码错误"},
        "execution_time": 0.5,
        "created_at": "2024-01-01T10:00:00Z"
    }
}

# 搜索日志
POST /api/logs/search
Request: {
    "keyword": "登录失败",
    "page": 1,
    "per_page": 20
}
Response: {
    "code": 200,
    "message": "搜索日志成功",
    "data": {
        "items": [...],
        "total": 50,
        "page": 1,
        "per_page": 20,
        "pages": 3
    }
}
```

#### 6.23.3 日志统计接口
```python
# 获取日志统计信息
GET /api/logs/statistics
Response: {
    "code": 200,
    "message": "获取日志统计成功",
    "data": {
        "level_stats": {
            "INFO": 1000,
            "WARNING": 100,
            "ERROR": 50,
            "CRITICAL": 5
        },
        "module_stats": {
            "AUTH": 500,
            "USER_MANAGEMENT": 300,
            "EXAM_MANAGEMENT": 200
        },
        "recent_logs": {
            "2024-01-01": 100,
            "2024-01-02": 120,
            "2024-01-03": 90
        }
    }
}
```

#### 6.23.4 日志清理接口
```python
# 清理旧日志
POST /api/logs/cleanup
Request: {
    "days": 30
}
Response: {
    "code": 200,
    "message": "清理日志成功，删除了1000条记录",
    "data": {
        "deleted_count": 1000
    }
}

# 重新设置日志系统
POST /api/logs/setup
Response: {
    "code": 200,
    "message": "日志配置设置成功"
}
```

## 7. 前端开发规范

### 7.1 组件命名规范
- 组件名使用 PascalCase
- 文件名使用 PascalCase.vue
- 组件目录使用 kebab-case

### 7.2 导航栏统一管理规范
**重要：导航栏只在 AppLayout.vue 中定义一次，其他页面不要重复定义导航栏**

```vue
<!-- components/layout/AppLayout.vue -->
<template>
  <div class="app-layout">
    <el-container>
      <!-- 顶部导航栏 - 只在这里定义 -->
      <el-header class="header">
        <Header />
      </el-header>
      
      <el-container>
        <!-- 侧边栏 - 只在这里定义 -->
        <el-aside class="sidebar">
          <Sidebar />
        </el-aside>
        
        <!-- 主内容区域 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import Header from './Header.vue'
import Sidebar from './Sidebar.vue'

export default {
  name: 'AppLayout',
  components: {
    Header,
    Sidebar
  }
}
</script>
```

**页面组件规范：**
```vue
<!-- views/admin/UserManagement.vue -->
<template>
  <div class="user-management">
    <!-- 页面内容，不要包含导航栏 -->
    <h1>用户管理</h1>
    <!-- 其他页面内容 -->
  </div>
</template>

<script>
export default {
  name: 'UserManagement'
  // 页面逻辑
}
</script>
```

### 7.3 API 调用规范
```javascript
// api/base.js
import axios from 'axios'

const request = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
  timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      // 处理未授权
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default request
```

### 7.4 状态管理规范
```javascript
// stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isLoggedIn: false
  }),
  
  getters: {
    userRole: (state) => state.user?.role,
    isAdmin: (state) => state.user?.role === 'admin'
  },
  
  actions: {
    async login(credentials) {
      // 登录逻辑
    },
    
    async logout() {
      // 登出逻辑
    }
  }
})
```

### 7.5 表单验证规范
```javascript
// utils/validation.js
export const rules = {
  required: (message = '此字段为必填项') => ({
    required: true,
    message,
    trigger: 'blur'
  }),
  
  email: () => ({
    type: 'email',
    message: '请输入正确的邮箱地址',
    trigger: 'blur'
  }),
  
  minLength: (min, message) => ({
    min,
    message: message || `长度不能少于${min}个字符`,
    trigger: 'blur'
  }),
  
  username: () => ({
    pattern: /^[a-zA-Z0-9_]{3,20}$/,
    message: '用户名只能包含字母、数字、下划线，长度3-20位',
    trigger: 'blur'
  })
}
```

### 7.6 通用组件规范
```vue
<!-- components/common/BaseTable.vue -->
<template>
  <div class="base-table">
    <el-table
      :data="data"
      :loading="loading"
      v-bind="$attrs"
      @selection-change="handleSelectionChange"
    >
      <slot></slot>
    </el-table>
    
    <el-pagination
      v-if="showPagination"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      @current-change="handlePageChange"
      @size-change="handleSizeChange"
    />
  </div>
</template>

<script>
export default {
  name: 'BaseTable',
  props: {
    data: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    showPagination: {
      type: Boolean,
      default: true
    },
    currentPage: {
      type: Number,
      default: 1
    },
    pageSize: {
      type: Number,
      default: 10
    },
    total: {
      type: Number,
      default: 0
    }
  },
  emits: ['selection-change', 'page-change', 'size-change'],
  methods: {
    handleSelectionChange(selection) {
      this.$emit('selection-change', selection)
    },
    handlePageChange(page) {
      this.$emit('page-change', page)
    },
    handleSizeChange(size) {
      this.$emit('size-change', size)
    }
  }
}
</script>
```

## 8. 后端开发规范

### 8.1 模型定义规范
```python
# models/base.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
```

### 8.2 API 装饰器规范
```python
# utils/decorators.py
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

def require_roles(*roles):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()
            if current_user.role not in roles:
                return jsonify({'message': '权限不足'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_json(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                data = request.get_json()
                validated_data = schema.load(data)
                request.validated_data = validated_data
                return f(*args, **kwargs)
            except ValidationError as e:
                return jsonify({'message': '数据验证失败', 'errors': e.messages}), 422
        return decorated_function
    return decorator
```

### 8.3 服务层规范
```python
# services/base_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

class BaseService:
    def __init__(self, model_class):
        self.model_class = model_class
    
    def create(self, data: Dict[str, Any]) -> Any:
        instance = self.model_class(**data)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def get_by_id(self, id: int) -> Optional[Any]:
        return self.model_class.query.get(id)
    
    def get_all(self, page: int = 1, per_page: int = 10, **filters) -> List[Any]:
        query = self.model_class.query
        for key, value in filters.items():
            if hasattr(self.model_class, key) and value is not None:
                query = query.filter(getattr(self.model_class, key) == value)
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    def update(self, id: int, data: Dict[str, Any]) -> Optional[Any]:
        instance = self.get_by_id(id)
        if instance:
            for key, value in data.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.session.commit()
        return instance
    
    def delete(self, id: int) -> bool:
        instance = self.get_by_id(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False
```

### 8.4 数据验证规范
```python
# utils/validators.py
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True, validate=[
        validate.Length(min=3, max=20),
        validate.Regexp(r'^[a-zA-Z0-9_]+$', error='用户名只能包含字母、数字、下划线')
    ])
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    real_name = fields.Str(validate=validate.Length(max=50))
    role = fields.Str(validate=validate.OneOf(['admin', 'user']))

class QuestionSchema(Schema):
    subject_id = fields.Int(required=True)
    type = fields.Str(required=True, validate=validate.OneOf(['single', 'multiple', 'judge', 'fill', 'essay']))
    title = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    content = fields.Str()
    options = fields.List(fields.Str())
    answer = fields.Str(required=True)
    explanation = fields.Str()
    difficulty = fields.Str(validate=validate.OneOf(['easy', 'medium', 'hard']))
    points = fields.Int(validate=validate.Range(min=1, max=100))
```

### 8.5 日志装饰器规范
```python
# utils/log_decorators.py
from app.utils.log_decorators import log_operation, log_api_access, log_user_action

# 操作日志装饰器
@log_operation('USER_LOGIN', '用户登录')
def login():
    """用户登录功能"""
    # 登录逻辑
    pass

# API访问日志装饰器
@log_api_access()
def api_endpoint():
    """API接口"""
    # API逻辑
    pass

# 用户行为日志装饰器
@log_user_action('EXAM_START', '开始考试')
def start_exam():
    """开始考试功能"""
    # 考试开始逻辑
    pass

# 在API接口中使用
from flask_restful import Resource
from app.utils.log_decorators import log_operation

class UserAPI(Resource):
    @log_operation('USER_CREATE', '创建用户')
    def post(self):
        """创建用户"""
        # 创建用户逻辑
        pass
    
    @log_operation('USER_UPDATE', '更新用户')
    def put(self, user_id):
        """更新用户"""
        # 更新用户逻辑
        pass
    
    @log_operation('USER_DELETE', '删除用户')
    def delete(self, user_id):
        """删除用户"""
        # 删除用户逻辑
        pass
```

### 8.6 日志服务规范
```python
# services/log_service.py
from app.services.log_service import LogService, LogConfigService

# 记录日志到数据库
LogService.log_to_database(
    level='INFO',
    module='USER_MANAGEMENT',
    message='用户创建成功',
    user_id=1,
    ip_address='192.168.1.100',
    user_agent='Mozilla/5.0...',
    request_data={'username': 'test'},
    response_data={'user_id': 1},
    execution_time=0.5
)

# 获取日志列表
logs = LogService.get_logs(
    page=1,
    per_page=20,
    level='ERROR',
    module='AUTH',
    user_id=1,
    start_date='2024-01-01',
    end_date='2024-01-31'
)

# 搜索日志
search_results = LogService.search_logs(
    keyword='登录失败',
    page=1,
    per_page=20
)

# 获取日志统计
stats = LogService.get_log_statistics()

# 清理旧日志
deleted_count = LogService.cleanup_old_logs(days=30)

# 日志配置管理
configs = LogConfigService.get_all_configs()
LogConfigService.update_config('LOG_LEVEL', 'DEBUG')
LogService.setup_logging()
```

## 9. 第三方支付API集成规范

### 9.1 支付宝支付集成

#### 9.1.1 支付宝开放平台配置
```python
# 支付宝配置
ALIPAY_APP_ID = "your_app_id"
ALIPAY_PRIVATE_KEY = "your_private_key"
ALIPAY_PUBLIC_KEY = "alipay_public_key"
ALIPAY_GATEWAY = "https://openapi.alipay.com/gateway.do"  # 正式环境
# ALIPAY_GATEWAY = "https://openapi.alipaydev.com/gateway.do"  # 沙箱环境
```

#### 9.1.2 支付宝支付实现
```python
# app/services/payment/alipay_service.py
from alipay import AliPay
from app import app

class AlipayService:
    def __init__(self):
        self.app_id = app.config['ALIPAY_APP_ID']
        self.private_key = app.config['ALIPAY_PRIVATE_KEY']
        self.alipay_public_key = app.config['ALIPAY_PUBLIC_KEY']
        self.gateway = app.config['ALIPAY_GATEWAY']
        
        self.alipay = AliPay(
            appid=self.app_id,
            app_notify_url=None,
            app_private_key_string=self.private_key,
            alipay_public_key_string=self.alipay_public_key,
            sign_type="RSA2",
            debug=False
        )
    
    def create_order(self, order_id, amount, subject, return_url, notify_url):
        """创建支付订单"""
        order_string = self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(amount),
            subject=subject,
            return_url=return_url,
            notify_url=notify_url
        )
        return f"{self.gateway}?{order_string}"
    
    def verify_notify(self, data):
        """验证支付回调"""
        return self.alipay.verify(data, data.get('sign'))
    
    def query_order(self, order_id):
        """查询订单状态"""
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        return result
```

#### 9.1.3 支付宝回调处理
```python
# app/api/payments.py
@payments_bp.route('/alipay/callback', methods=['POST'])
def alipay_callback():
    """支付宝支付回调"""
    try:
        data = request.form.to_dict()
        alipay_service = AlipayService()
        
        if alipay_service.verify_notify(data):
            order_id = data.get('out_trade_no')
            trade_status = data.get('trade_status')
            
            if trade_status == 'TRADE_SUCCESS':
                # 更新订单状态为已支付
                order = PaymentOrder.query.filter_by(order_id=order_id).first()
                if order:
                    order.status = 'paid'
                    order.paid_at = datetime.utcnow()
                    order.third_party_order_id = data.get('trade_no')
                    db.session.commit()
                    
                    # 开通用户课程权限
                    activate_user_course(order.user_id, order.subject_id)
            
            return 'success'
        else:
            return 'fail'
    except Exception as e:
        logger.error(f"支付宝回调处理失败: {e}")
        return 'fail'
```

### 9.2 微信支付集成

#### 9.2.1 微信支付配置
```python
# 微信支付配置
WECHAT_APP_ID = "your_app_id"
WECHAT_MCH_ID = "your_mch_id"
WECHAT_API_KEY = "your_api_key"
WECHAT_CERT_PATH = "path/to/cert.pem"
WECHAT_KEY_PATH = "path/to/key.pem"
WECHAT_NOTIFY_URL = "https://yourdomain.com/api/payments/wechat/callback"
```

#### 9.2.2 微信支付实现
```python
# app/services/payment/wechat_service.py
from wechatpay_python import WeChatPay
from wechatpay_python.utils import get_signature
import xml.etree.ElementTree as ET

class WechatPayService:
    def __init__(self):
        self.app_id = app.config['WECHAT_APP_ID']
        self.mch_id = app.config['WECHAT_MCH_ID']
        self.api_key = app.config['WECHAT_API_KEY']
        self.cert_path = app.config['WECHAT_CERT_PATH']
        self.key_path = app.config['WECHAT_KEY_PATH']
        self.notify_url = app.config['WECHAT_NOTIFY_URL']
        
        self.wechatpay = WeChatPay(
            appid=self.app_id,
            mch_id=self.mch_id,
            api_key=self.api_key,
            cert_path=self.cert_path,
            key_path=self.key_path
        )
    
    def create_order(self, order_id, amount, subject, user_ip):
        """创建支付订单"""
        order_data = {
            'appid': self.app_id,
            'mch_id': self.mch_id,
            'nonce_str': generate_nonce_str(),
            'body': subject,
            'out_trade_no': order_id,
            'total_fee': int(amount * 100),  # 微信支付金额单位为分
            'spbill_create_ip': user_ip,
            'notify_url': self.notify_url,
            'trade_type': 'NATIVE'  # 扫码支付
        }
        
        # 生成签名
        order_data['sign'] = get_signature(order_data, self.api_key)
        
        # 调用统一下单API
        response = self.wechatpay.unified_order(order_data)
        
        if response.get('return_code') == 'SUCCESS':
            return response.get('code_url')  # 二维码链接
        else:
            raise Exception(f"微信支付下单失败: {response.get('return_msg')}")
    
    def verify_notify(self, data):
        """验证支付回调"""
        return self.wechatpay.verify_notify(data)
```

#### 9.2.3 微信支付回调处理
```python
# app/api/payments.py
@payments_bp.route('/wechat/callback', methods=['POST'])
def wechat_callback():
    """微信支付回调"""
    try:
        xml_data = request.data
        root = ET.fromstring(xml_data)
        
        data = {}
        for child in root:
            data[child.tag] = child.text
        
        wechat_service = WechatPayService()
        
        if wechat_service.verify_notify(data):
            order_id = data.get('out_trade_no')
            transaction_id = data.get('transaction_id')
            
            # 更新订单状态
            order = PaymentOrder.query.filter_by(order_id=order_id).first()
            if order:
                order.status = 'paid'
                order.paid_at = datetime.utcnow()
                order.third_party_order_id = transaction_id
                db.session.commit()
                
                # 开通用户课程权限
                activate_user_course(order.user_id, order.subject_id)
            
            # 返回成功响应
            return '''<xml>
                <return_code><![CDATA[SUCCESS]]></return_code>
                <return_msg><![CDATA[OK]]></return_msg>
            </xml>'''
        else:
            return '''<xml>
                <return_code><![CDATA[FAIL]]></return_code>
                <return_msg><![CDATA[签名验证失败]]></return_msg>
            </xml>'''
    except Exception as e:
        logger.error(f"微信支付回调处理失败: {e}")
        return '''<xml>
            <return_code><![CDATA[FAIL]]></return_code>
            <return_msg><![CDATA[系统错误]]></return_msg>
        </xml>'''
```

### 9.3 PayPal支付集成

#### 9.3.1 PayPal配置
```python
# PayPal配置
PAYPAL_CLIENT_ID = "your_client_id"
PAYPAL_CLIENT_SECRET = "your_client_secret"
PAYPAL_MODE = "live"  # live 或 sandbox
PAYPAL_RETURN_URL = "https://yourdomain.com/payment/success"
PAYPAL_CANCEL_URL = "https://yourdomain.com/payment/cancel"
```

#### 9.3.2 PayPal支付实现
```python
# app/services/payment/paypal_service.py
import paypalrestsdk

class PayPalService:
    def __init__(self):
        paypalrestsdk.configure({
            "mode": app.config['PAYPAL_MODE'],
            "client_id": app.config['PAYPAL_CLIENT_ID'],
            "client_secret": app.config['PAYPAL_CLIENT_SECRET']
        })
    
    def create_payment(self, order_id, amount, currency, subject, return_url, cancel_url):
        """创建PayPal支付"""
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": subject,
                        "sku": order_id,
                        "price": str(amount),
                        "currency": currency,
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(amount),
                    "currency": currency
                },
                "description": subject
            }]
        })
        
        if payment.create():
            approval_url = None
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    break
            
            return {
                'payment_id': payment.id,
                'approval_url': approval_url
            }
        else:
            raise Exception(f"PayPal支付创建失败: {payment.error}")
    
    def execute_payment(self, payment_id, payer_id):
        """执行PayPal支付"""
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            return payment
        else:
            raise Exception(f"PayPal支付执行失败: {payment.error}")
```

#### 9.3.3 PayPal支付处理
```python
# app/api/payments.py
@payments_bp.route('/paypal/create', methods=['POST'])
def paypal_create_payment():
    """创建PayPal支付"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        amount = data.get('amount')
        currency = data.get('currency', 'USD')
        subject = data.get('subject')
        
        paypal_service = PayPalService()
        
        result = paypal_service.create_payment(
            order_id=order_id,
            amount=amount,
            currency=currency,
            subject=subject,
            return_url=f"{app.config['PAYPAL_RETURN_URL']}?order_id={order_id}",
            cancel_url=f"{app.config['PAYPAL_CANCEL_URL']}?order_id={order_id}"
        )
        
        # 保存PayPal支付ID到订单
        order = PaymentOrder.query.filter_by(order_id=order_id).first()
        if order:
            order.third_party_order_id = result['payment_id']
            db.session.commit()
        
        return jsonify(build_response(
            message='PayPal支付创建成功',
            data=result
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'PayPal支付创建失败: {str(e)}')), 500

@payments_bp.route('/paypal/execute', methods=['POST'])
def paypal_execute_payment():
    """执行PayPal支付"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        payer_id = data.get('payer_id')
        order_id = data.get('order_id')
        
        paypal_service = PayPalService()
        payment = paypal_service.execute_payment(payment_id, payer_id)
        
        # 更新订单状态
        order = PaymentOrder.query.filter_by(order_id=order_id).first()
        if order:
            order.status = 'paid'
            order.paid_at = datetime.utcnow()
            db.session.commit()
            
            # 开通用户课程权限
            activate_user_course(order.user_id, order.subject_id)
        
        return jsonify(build_response(
            message='PayPal支付成功',
            data={'payment_id': payment.id}
        ))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'PayPal支付执行失败: {str(e)}')), 500
```

### 9.4 联系管理员支付方式

#### 9.4.1 管理员支付处理
```python
# app/api/payments.py
@payments_bp.route('/admin/payment', methods=['POST'])
@jwt_required()
@require_roles('admin')
def admin_payment():
    """管理员确认支付"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        admin_note = data.get('admin_note', '')
        current_user_id = get_jwt_identity()
        
        order = PaymentOrder.query.filter_by(order_id=order_id).first()
        if not order:
            return jsonify(build_error_response(404, '订单不存在')), 404
        
        if order.payment_method != 'admin':
            return jsonify(build_error_response(400, '该订单不是管理员支付方式')), 400
        
        # 更新订单状态
        order.status = 'paid'
        order.paid_at = datetime.utcnow()
        order.callback_data = {'admin_id': current_user_id, 'note': admin_note}
        db.session.commit()
        
        # 开通用户课程权限
        activate_user_course(order.user_id, order.subject_id)
        
        # 记录操作日志
        log_operation(
            user_id=current_user_id,
            operation='admin_payment_confirm',
            details=f'管理员确认支付订单: {order_id}',
            ip=get_client_ip(request)
        )
        
        return jsonify(build_response(message='支付确认成功'))
        
    except Exception as e:
        return jsonify(build_error_response(500, f'支付确认失败: {str(e)}')), 500
```

### 9.5 支付安全规范

#### 9.5.1 签名验证
```python
# app/utils/payment_security.py
import hashlib
import hmac
import time

def generate_signature(params, secret_key):
    """生成支付签名"""
    # 排序参数
    sorted_params = sorted(params.items())
    # 拼接字符串
    query_string = '&'.join([f"{k}={v}" for k, v in sorted_params if v])
    # 添加密钥
    query_string += f"&key={secret_key}"
    # MD5加密
    return hashlib.md5(query_string.encode('utf-8')).hexdigest().upper()

def verify_signature(params, signature, secret_key):
    """验证支付签名"""
    expected_signature = generate_signature(params, secret_key)
    return hmac.compare_digest(signature, expected_signature)
```

#### 9.5.2 订单号生成
```python
# app/utils/order_utils.py
import uuid
import time

def generate_order_id():
    """生成唯一订单号"""
    timestamp = int(time.time())
    random_str = str(uuid.uuid4()).replace('-', '')[:8]
    return f"EX{timestamp}{random_str}"

def generate_payment_id():
    """生成支付流水号"""
    timestamp = int(time.time() * 1000)
    random_str = str(uuid.uuid4()).replace('-', '')[:6]
    return f"PAY{timestamp}{random_str}"
```

### 9.6 支付环境配置

#### 9.6.1 环境变量配置
```bash
# .env.example
# 支付宝配置
ALIPAY_APP_ID=your_alipay_app_id
ALIPAY_PRIVATE_KEY=your_alipay_private_key
ALIPAY_PUBLIC_KEY=alipay_public_key
ALIPAY_GATEWAY=https://openapi.alipay.com/gateway.do

# 微信支付配置
WECHAT_APP_ID=your_wechat_app_id
WECHAT_MCH_ID=your_wechat_mch_id
WECHAT_API_KEY=your_wechat_api_key
WECHAT_CERT_PATH=path/to/cert.pem
WECHAT_KEY_PATH=path/to/key.pem

# PayPal配置
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox
```

#### 9.6.2 支付配置类
```python
# app/config/payment.py
import os

class PaymentConfig:
    # 支付宝配置
    ALIPAY_APP_ID = os.getenv('ALIPAY_APP_ID')
    ALIPAY_PRIVATE_KEY = os.getenv('ALIPAY_PRIVATE_KEY')
    ALIPAY_PUBLIC_KEY = os.getenv('ALIPAY_PUBLIC_KEY')
    ALIPAY_GATEWAY = os.getenv('ALIPAY_GATEWAY', 'https://openapi.alipay.com/gateway.do')
    
    # 微信支付配置
    WECHAT_APP_ID = os.getenv('WECHAT_APP_ID')
    WECHAT_MCH_ID = os.getenv('WECHAT_MCH_ID')
    WECHAT_API_KEY = os.getenv('WECHAT_API_KEY')
    WECHAT_CERT_PATH = os.getenv('WECHAT_CERT_PATH')
    WECHAT_KEY_PATH = os.getenv('WECHAT_KEY_PATH')
    
    # PayPal配置
    PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
    PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')
    
    # 支付回调URL
    PAYMENT_RETURN_URL = os.getenv('PAYMENT_RETURN_URL', 'https://yourdomain.com/payment/success')
    PAYMENT_CANCEL_URL = os.getenv('PAYMENT_CANCEL_URL', 'https://yourdomain.com/payment/cancel')
    PAYMENT_NOTIFY_URL = os.getenv('PAYMENT_NOTIFY_URL', 'https://yourdomain.com/api/payments/callback')
```

## 10. 部署规范

### 10.1 Windows 环境部署

#### 9.1.1 后端部署
```bash
# 1. 安装 Python 3.11+
# 2. 安装 MySQL 8.0+
# 3. 安装 Redis

# 4. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 配置环境变量
copy .env.example .env
# 编辑 .env 文件配置数据库连接

# 7. 初始化数据库
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 8. 启动应用
python run.py
```

#### 9.1.2 前端部署
```bash
# 1. 安装 Node.js 16+
# 2. 安装依赖
npm install

# 3. 构建生产版本
npm run build

# 4. 将 dist 目录内容部署到 Apache
```

#### 9.1.3 Apache HTTPD 配置
```apache
# httpd.conf 或虚拟主机配置
<VirtualHost *:80>
    ServerName examsphere.local
    DocumentRoot "C:/path/to/examsphere/frontend/dist"
    
    # 前端静态文件
    <Directory "C:/path/to/examsphere/frontend/dist">
        AllowOverride All
        Require all granted
        
        # Vue Router 历史模式支持
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
    
    # API 代理到后端
    ProxyPreserveHost On
    ProxyPass /api/ http://localhost:9999/api/
    ProxyPassReverse /api/ http://localhost:9999/api/
    
    # 静态资源
    ProxyPass /static/ http://localhost:9999/static/
    ProxyPassReverse /static/ http://localhost:9999/static/
</VirtualHost>
```

### 9.2 Linux 环境部署

#### 9.2.1 后端部署
```bash
# 1. 安装 Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# 2. 安装 MySQL 8.0+
sudo apt install mysql-server mysql-client

# 3. 安装 Redis
sudo apt install redis-server

# 4. 创建项目目录
sudo mkdir -p /var/www/examsphere
sudo chown $USER:$USER /var/www/examsphere

# 5. 创建虚拟环境
cd /var/www/examsphere
python3.11 -m venv venv
source venv/bin/activate

# 6. 安装依赖
pip install -r requirements.txt

# 7. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 8. 初始化数据库
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# 9. 使用 Gunicorn 启动
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:9999 run:app
```

#### 9.2.2 前端部署
```bash
# 1. 安装 Node.js 16+
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. 安装依赖
npm install

# 3. 构建生产版本
npm run build

# 4. 部署到 Apache 目录
sudo cp -r dist/* /var/www/html/examsphere/
```

#### 9.2.3 Apache HTTPD 配置
```apache
# /etc/apache2/sites-available/examsphere.conf
<VirtualHost *:80>
    ServerName examsphere.local
    DocumentRoot /var/www/html/examsphere
    
    # 前端静态文件
    <Directory /var/www/html/examsphere>
        AllowOverride All
        Require all granted
        
        # Vue Router 历史模式支持
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
    
    # API 代理到后端
    ProxyPreserveHost On
    ProxyPass /api/ http://localhost:9999/api/
    ProxyPassReverse /api/ http://localhost:9999/api/
    
    # 静态资源
    ProxyPass /static/ http://localhost:9999/static/
    ProxyPassReverse /static/ http://localhost:9999/static/
    
    # 启用必要的模块
    LoadModule rewrite_module modules/mod_rewrite.so
    LoadModule proxy_module modules/mod_proxy.so
    LoadModule proxy_http_module modules/mod_proxy_http.so
</VirtualHost>

# 启用站点
sudo a2ensite examsphere.conf
sudo systemctl reload apache2
```

### 9.3 生产环境优化

#### 9.3.1 后端优化
```python
# 使用 Gunicorn 配置
# gunicorn.conf.py
bind = "0.0.0.0:9999"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
```

#### 9.3.2 前端优化
```javascript
// vue.config.js
module.exports = {
  publicPath: process.env.NODE_ENV === 'production' ? '/examsphere/' : '/',
  outputDir: 'dist',
  assetsDir: 'static',
  productionSourceMap: false,
  
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          }
        }
      }
    }
  }
}
```

#### 9.3.3 系统服务配置
```ini
# /etc/systemd/system/examsphere.service
[Unit]
Description=ExamSphere Backend
After=network.target mysql.service redis.service

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/var/www/examsphere
Environment=PATH=/var/www/examsphere/venv/bin
ExecStart=/var/www/examsphere/venv/bin/gunicorn -c gunicorn.conf.py run:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl enable examsphere.service
sudo systemctl start examsphere.service
```

### 9.4 环境变量配置
```bash
# .env.example
# 数据库配置
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/examsphere

# Redis 配置
REDIS_URL=redis://localhost:6379/0

# JWT 配置
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600

# Flask 配置
FLASK_ENV=development
SECRET_KEY=your-flask-secret-key

# 文件上传配置
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

## 10. 开发流程规范

### 10.1 Git 工作流
1. 主分支：`main` - 生产环境代码
2. 开发分支：`develop` - 开发环境代码
3. 功能分支：`feature/功能名称` - 新功能开发
4. 修复分支：`hotfix/问题描述` - 紧急修复

### 10.2 提交规范
```
feat: 新功能
fix: 修复问题
docs: 文档更新
style: 代码格式调整
refactor: 代码重构
test: 测试相关
chore: 构建过程或辅助工具的变动
```

### 10.3 代码审查规范
1. 所有代码必须经过 Code Review
2. 确保代码符合项目规范
3. 确保测试覆盖率达标
4. 确保文档更新完整

## 11. 开发约束规范

### 11.1 禁止生成的内容
**重要：开发过程中禁止生成以下内容**

1. **测试文件**
   - 不要生成 `*.test.js`、`*.spec.js` 文件
   - 不要生成 `tests/` 目录
   - 不要生成测试相关的配置和依赖

2. **文档文件**
   - 不要生成 `README.md`、`CHANGELOG.md` 等文档
   - 不要生成 `docs/` 目录
   - 不要生成 API 文档文件

3. **配置文件**
   - 不要生成 `jest.config.js`、`cypress.config.js` 等测试配置
   - 不要生成 `webpack.config.js`（使用 vue.config.js）
   - 不要生成 `babel.config.js`（Vue CLI 已包含）

4. **示例和演示文件**
   - 不要生成 `examples/`、`demo/` 目录
   - 不要生成示例数据文件
   - 不要生成演示页面

5. **开发工具配置**
   - 不要生成 `.eslintrc.js`、`.prettierrc` 等代码规范配置
   - 不要生成 `husky`、`lint-staged` 等 Git hooks 配置
   - 不要生成 `nodemon.json` 等开发工具配置

### 11.2 必须生成的内容
**开发过程中必须生成的内容**

1. **核心业务文件**
   - 模型文件（models/）
   - API 接口文件（api/）
   - 页面组件（views/）
   - 公共组件（components/）

2. **配置文件**
   - `package.json`（前端）
   - `requirements.txt`（后端）
   - `.env.example`
   - `vue.config.js`

3. **数据库文件**
   - 数据库迁移文件
   - 初始化脚本

### 11.3 代码生成规范
1. **只生成必要的业务代码**
2. **使用统一的代码模板**
3. **遵循项目结构规范**
4. **包含必要的注释说明**

## 12. 性能优化规范

### 12.1 数据库优化
- 合理使用索引
- 避免 N+1 查询问题
- 使用数据库连接池
- 定期清理无用数据

### 12.2 前端优化
- 使用路由懒加载
- 组件按需加载
- 图片懒加载
- 合理使用缓存

### 12.3 API 优化
- 使用分页查询
- 实现接口缓存
- 使用异步处理
- 合理设置超时时间

## 13. 安全规范

### 13.1 认证安全
- 使用 JWT 进行身份认证
- 密码加密存储
- 实现登录失败锁定
- 定期更新密钥

### 13.2 数据安全
- 输入数据验证
- SQL 注入防护
- XSS 攻击防护
- CSRF 攻击防护

### 13.3 接口安全
- 接口访问频率限制
- 敏感操作权限验证
- 数据脱敏处理
- 日志记录和监控

## 14. 监控和日志规范

### 14.1 日志规范
```python
# utils/logger.py
import logging
from datetime import datetime

def setup_logger(name, level='INFO'):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
```

### 14.2 错误监控
- 实现全局异常处理
- 记录详细错误信息
- 设置错误告警机制
- 定期分析错误日志

---

## 项目完成状态

### ✅ 开发完成情况
ExamSphere 考试管理系统已经全部开发完成！所有20个功能模块均已实现，包括：

- ✅ 用户管理模块 (100%)
- ✅ 科目管理模块 (100%)
- ✅ 试题管理模块 (100%)
- ✅ 考试管理模块 (100%)
- ✅ 考试履历模块 (100%)
- ✅ 前台用户功能 (100%)
- ✅ 管理员功能模块 (100%)
- ✅ 消息通知模块 (100%)
- ✅ 文件管理模块 (100%)
- ✅ 统计分析模块 (100%)
- ✅ 防作弊模块 (100%)
- ✅ 移动端适配 (100%)
- ✅ 权限管理模块 (100%)
- ✅ 数据导入导出模块 (100%)
- ✅ 考试模板模块 (100%)
- ✅ 学习路径模块 (100%)
- ✅ 在线答疑模块 (100%)
- ✅ 收费课程模块 (100%)
- ✅ 支付管理模块 (100%)
- ✅ 日志管理模块 (100%)

### 📊 技术成果
- **前端页面**: 20+个Vue组件
- **后端API**: 23组RESTful接口
- **数据模型**: 27个数据库表
- **服务模块**: 16+个业务服务
- **开发周期**: 8周（提前完成）

### 🎯 项目特色
1. **功能完整**: 涵盖考试管理全流程
2. **技术先进**: Vue 3 + Flask + MySQL架构
3. **用户体验**: 现代化UI设计
4. **系统安全**: 完善的权限控制
5. **数据管理**: 强大的导入导出功能
6. **统计分析**: 多维度数据分析
7. **扩展性强**: 模块化设计架构
8. **日志管理**: 完善的日志记录和分析系统

---

## 总结

ExamSphere 考试管理系统是一个功能完整、技术先进的企业级在线考试管理系统。系统采用现代化的技术架构，提供完整的考试管理解决方案，支持大规模用户并发，具备良好的扩展性和维护性。

**项目状态**: ✅ 开发完成，可投入生产使用
