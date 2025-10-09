# ExamSphere 考试管理系统

## 📋 项目简介

ExamSphere 是一个基于 Web 的在线考试管理系统，支持用户管理、科目管理、试题管理、考试管理等功能。系统采用前后端分离架构，提供完整的在线考试解决方案。

## 🎯 功能特性

### 核心功能
- **用户管理**: 用户注册/登录、角色权限管理（管理员、普通用户）、用户信息管理
- **科目管理**: 科目创建、分类管理、状态管理
- **试题管理**: 多种题型支持（单选、多选、判断、填空、简答）、试题分类和标签
- **考试管理**: 考试创建和配置、随机组卷、考试监控、结果统计
- **考试履历**: 考试记录查询、成绩分析、错题记录和复习

### 高级功能
- **管理员功能**: 用户管理、科目管理、试题管理、考试管理、题库管理、考试创建、考试分析
- **系统管理**: 系统参数配置、数据备份恢复、日志管理
- **消息通知**: 站内消息、邮件通知、考试提醒
- **文件管理**: 文件上传下载、图片资源管理
- **统计分析**: 考试数据统计、用户行为分析、试题难度分析
- **防作弊**: 切屏检测、答题时间监控、异常行为记录
- **移动端适配**: 响应式设计、移动端考试支持
- **权限管理**: 基于角色的权限控制（管理员、普通用户）
- **数据导入导出**: Excel批量导入、数据导出功能
- **考试模板**: 模板创建、复用功能、快速组卷
- **学习路径**: 学习计划制定、进度跟踪、个性化推荐
- **在线答疑**: 实时聊天、问题分类、管理员答疑

## 🛠 技术架构

### 前端技术栈
- **Vue 3**: 现代化前端框架
- **JavaScript**: 纯JavaScript开发，无TypeScript
- **Element Plus**: UI组件库
- **Pinia**: 状态管理
- **Vue Router**: 路由管理
- **Axios**: HTTP客户端

### 后端技术栈
- **Python 3.11+**: 编程语言
- **Flask**: Web框架
- **SQLAlchemy**: ORM框架
- **Flask-RESTful**: RESTful API框架
- **Flask-JWT-Extended**: JWT认证
- **Flask-CORS**: 跨域支持
- **Marshmallow**: 数据验证

### 数据库
- **MySQL 8.0+**: 主数据库
- **Redis**: 缓存和会话存储

### 部署
- **Apache HTTPD**: Web服务器
- **Gunicorn**: WSGI服务器（Linux）
- **Windows/Linux**: 跨平台部署支持

## 📁 项目结构

```
ExamSphere/
├── backend/                    # 后端项目
│   ├── app/
│   │   ├── models/            # 数据模型
│   │   ├── api/               # API接口
│   │   ├── services/          # 业务逻辑
│   │   ├── utils/             # 工具函数
│   │   └── config/            # 配置文件
│   ├── requirements.txt       # Python依赖
│   ├── env.example           # 环境变量示例
│   └── run.py               # 启动脚本
├── frontend/                  # 前端项目
│   ├── src/
│   │   ├── api/              # API接口
│   │   ├── components/       # 公共组件
│   │   ├── views/            # 页面组件
│   │   ├── stores/           # 状态管理
│   │   ├── router/           # 路由配置
│   │   └── utils/            # 工具函数
│   ├── package.json          # Node.js依赖
│   └── vue.config.js         # Vue配置
├── .cursor/
│   └── rules/                # Cursor开发规范
├── ExamSphere_Development_Specification.md  # 开发规范文档
└── ExamSphere_Development_Timeline.md       # 开发时间计划
```

## 🚀 快速开始

### 环境要求
- Python 3.11+
- Node.js 16+
- MySQL 8.0+
- Redis 6.0+

### 后端部署

1. **克隆项目**
```bash
git clone <repository-url>
cd ExamSphere/backend
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

5. **初始化数据库**
```bash
# 创建数据库
mysql -u root -p
CREATE DATABASE examsphere CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 初始化Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **启动应用**
```bash
python run.py
```

### 前端部署

1. **进入前端目录**
```bash
cd ../frontend
```

2. **安装依赖**
```bash
npm install
```

3. **启动开发服务器**
```bash
npm run serve
```

4. **构建生产版本**
```bash
npm run build
```

## 📊 数据库设计

### 核心表结构
- **users**: 用户表（管理员、普通用户）
- **subjects**: 科目表
- **questions**: 试题表
- **exams**: 考试表
- **exam_records**: 考试记录表
- **user_favorites**: 用户收藏表
- **wrong_answers**: 错题记录表

### 设计特点
- **无外键约束**: 所有关联关系在业务层处理
- **JSON字段**: 支持复杂数据结构存储
- **索引优化**: 关键字段建立索引
- **软删除**: 重要数据支持软删除

## 🔧 开发规范

### 代码规范
- **Python**: PEP 8 规范
- **JavaScript**: ES6+ 标准
- **Vue**: Vue 3 Composition API
- **Git**: 约定式提交规范

### 项目规范
- **导航栏统一管理**: 只在 AppLayout.vue 中定义
- **API统一响应格式**: 标准化JSON响应
- **错误处理**: 全局异常处理机制
- **权限控制**: 基于角色的权限管理（管理员、普通用户）

### 开发约束
- **禁止生成**: 测试文件、文档文件、配置文件
- **必须生成**: 核心业务文件、必要配置文件
- **代码质量**: 统一代码模板、必要注释说明

## 📈 开发计划

### 第一阶段：基础架构搭建 (第1-2周)
- 项目环境搭建
- 用户认证系统
- 用户管理模块
- 科目管理模块

### 第二阶段：试题和考试核心功能 (第3-5周)
- 试题管理模块
- 考试管理模块
- 在线考试功能
- 考试监控和评分

### 第三阶段：用户体验和高级功能 (第6-8周)
- 考试履历和统计分析
- 消息通知和文件管理
- 权限管理和数据导入导出

### 第四阶段：高级功能和优化 (第9-11周)
- 防作弊和移动端适配
- 学习路径和在线答疑
- 系统优化和性能提升

### 第五阶段：测试和部署 (第12周)
- 功能测试
- 性能测试
- 安全测试
- 生产环境部署

## 🔒 安全特性

- **JWT认证**: 无状态身份验证
- **密码加密**: bcrypt密码哈希
- **输入验证**: 数据验证和清理
- **SQL注入防护**: ORM参数化查询
- **XSS防护**: 输出转义
- **CSRF防护**: 跨站请求伪造防护
- **访问控制**: 基于角色的权限管理

## 📱 移动端支持

- **响应式设计**: 适配各种屏幕尺寸
- **触屏优化**: 移动端交互优化
- **离线缓存**: 支持离线数据缓存
- **PWA支持**: 渐进式Web应用

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目链接: [https://github.com/username/ExamSphere](https://github.com/username/ExamSphere)
- 问题反馈: [Issues](https://github.com/username/ExamSphere/issues)

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

---

**ExamSphere** - 让在线考试更简单、更高效！ 🎓
