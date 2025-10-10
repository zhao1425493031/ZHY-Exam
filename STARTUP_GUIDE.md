# ExamSphere 启动说明

## 🚀 快速启动

### 1. 环境准备
- Python 3.11+
- MySQL 8.0+
- Node.js 16+

### 2. 数据库配置
创建数据库并配置连接信息：
```sql
CREATE DATABASE examsphere CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 后端启动
```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy env.example .env
# 编辑 .env 文件，配置数据库连接

# 启动应用（自动初始化）
python run.py
```

### 4. 前端启动
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run serve

# 或构建生产版本
npm run build
```

## 📋 启动过程说明

运行 `python run.py` 时，系统会自动执行以下初始化步骤：

### ✅ 系统初始化流程
1. **数据库连接检查** - 验证数据库连接是否正常
2. **数据库表创建** - 自动创建所有必要的数据库表
3. **系统配置初始化** - 创建默认系统配置
4. **日志配置初始化** - 设置日志管理参数
5. **默认管理员创建** - 创建系统管理员账户
6. **日志系统设置** - 配置日志记录功能

### 📝 默认账户信息
- **管理员账户**：
  - 用户名：`admin`
  - 密码：`admin123`
  - 邮箱：`admin@examsphere.com`

### 🌐 访问地址
- **后端API**：http://localhost:5000
- **前端界面**：http://localhost:8080

## 🔧 日志功能

系统启动后会自动配置日志功能：

### 日志文件位置
- **应用日志**：`backend/logs/examsphere.log`
- **错误日志**：`backend/logs/error.log`

### 日志配置
- **日志级别**：INFO
- **文件大小**：10MB（超过自动分割）
- **保留天数**：30天
- **备份数量**：30个文件

### 日志特性
- ✅ 按日期自动分割
- ✅ 按大小自动分割
- ✅ 敏感信息自动脱敏
- ✅ 多级别日志记录
- ✅ 数据库日志存储

## 🛠 故障排除

### 常见问题

#### 1. 数据库连接失败
```
❌ 数据库连接失败: (2003, "Can't connect to MySQL server")
```
**解决方案**：
- 检查MySQL服务是否启动
- 验证数据库连接配置
- 确认数据库用户权限

#### 2. 端口占用
```
❌ Address already in use
```
**解决方案**：
- 检查5000端口是否被占用
- 修改端口配置
- 终止占用端口的进程

#### 3. 依赖安装失败
```
❌ Failed to install requirements
```
**解决方案**：
- 检查Python版本（需要3.11+）
- 更新pip版本
- 使用虚拟环境

### 日志查看
```bash
# 查看应用日志
tail -f backend/logs/examsphere.log

# 查看错误日志
tail -f backend/logs/error.log

# 查看实时日志
tail -f backend/logs/examsphere.log | grep ERROR
```

## 📞 技术支持

如遇到问题，请检查：
1. 系统日志文件
2. 数据库连接状态
3. 环境变量配置
4. 依赖包版本

---

**ExamSphere 考试管理系统** - 让考试管理更简单！
