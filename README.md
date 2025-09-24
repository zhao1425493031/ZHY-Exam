# 在线考试系统

一个功能完整的在线考试系统，支持多种题型、实时评分、错题复习等功能。

## 功能特色

- 🎯 **多种题型**：支持单选、多选、填空、音频、视频等题型
- ⏰ **实时评分**：提交后立即评分，查看详细解析
- 📚 **错题复习**：自动收集错题，支持顺序和随机复习
- 📊 **学习统计**：查看考试履历，分析学习进度
- 👥 **用户管理**：支持用户注册、登录、权限管理
- 🔧 **管理后台**：题目管理、考试管理、用户管理

## 技术栈

- **后端**：Flask + SQLAlchemy + MySQL
- **前端**：HTML5 + Bootstrap 5 + jQuery
- **数据库**：MySQL 8.0
- **邮件服务**：SMTP（支持QQ邮箱等）

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 8.0+
- 支持SMTP的邮箱账号

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd exam-system
```

2. 运行安装脚本
```bash
install.bat
```

3. 配置环境变量
编辑 `.env` 文件，配置以下信息：
```env
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/exam_system
MAIL_USERNAME=your_email@qq.com
MAIL_PASSWORD=your_email_auth_code
```

4. 启动服务
```bash
run.bat
```

### 生产环境启动

使用Gunicorn启动生产环境：
```bash
start_production.bat
```

### 访问系统

- 访问地址：http://localhost:5000
- 默认管理员账号：admin@example.com
- 默认管理员密码：admin123

## 配置说明

### 数据库配置

1. 安装MySQL 8.0
2. 创建数据库：
```sql
CREATE DATABASE exam_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
3. 修改 `.env` 文件中的 `DATABASE_URL`

### 邮箱配置

1. 获取邮箱授权码（以QQ邮箱为例）：
   - 登录QQ邮箱
   - 设置 → 账户 → 开启SMTP服务
   - 生成授权码
2. 修改 `.env` 文件中的邮箱配置

## 使用说明

### 管理员功能

1. **题目管理**
   - 添加题目（单选、多选、填空、音频、视频）
   - 编辑题目
   - 删除题目
   - 题目分类和搜索

2. **考试管理**
   - 创建考试
   - 设置考试参数（时间、题目数量等）
   - 管理考试状态

3. **用户管理**
   - 查看用户列表
   - 管理用户权限

### 用户功能

1. **参加考试**
   - 选择考试
   - 在线答题
   - 实时保存答案
   - 自动提交

2. **个人中心**
   - 查看考试履历
   - 管理错题
   - 收藏题目
   - 学习统计

3. **错题复习**
   - 顺序复习
   - 随机复习
   - 查看解析

## 项目结构

```
exam-system/
├── app.py                 # 主程序文件
├── config.py              # 配置文件
├── requirements.txt       # Python依赖
├── env.example           # 环境变量示例
├── install.bat           # 安装脚本
├── run.bat               # 开发环境启动脚本
├── start_production.bat  # 生产环境启动脚本
├── templates/            # HTML模板
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── exam.html
│   ├── profile.html
│   ├── review.html
│   └── admin/
│       ├── index.html
│       ├── questions.html
│       ├── add_question.html
│       ├── exams.html
│       └── add_exam.html
├── uploads/              # 上传文件目录
└── logs/                 # 日志目录
```

## 开发说明

### 添加新功能

1. 在 `app.py` 中添加路由
2. 在 `templates/` 中创建对应模板
3. 更新数据库模型（如需要）

### 自定义样式

修改 `templates/base.html` 中的CSS样式

### 添加新题型

1. 在 `Question` 模型中添加新类型
2. 在考试页面添加对应的渲染逻辑
3. 在评分逻辑中添加处理

## 常见问题

### Q: 无法连接数据库
A: 检查MySQL服务是否启动，数据库连接字符串是否正确

### Q: 邮件发送失败
A: 检查邮箱配置，确保授权码正确

### Q: 上传文件失败
A: 检查 `uploads` 目录权限，确保可写

### Q: 页面显示异常
A: 检查静态文件路径，确保模板文件完整

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请通过以下方式联系：
- 邮箱：your-email@example.com
- GitHub：your-github-username
