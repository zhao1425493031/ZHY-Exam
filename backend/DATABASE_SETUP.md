# 数据库配置说明

## 环境要求
- MySQL 8.0+
- Python 3.11+
- PyMySQL 1.1.0+

## 数据库配置

### 1. 创建数据库
```sql
CREATE DATABASE examsphere CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 创建用户（可选）
```sql
CREATE USER 'examsphere'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON examsphere.* TO 'examsphere'@'localhost';
FLUSH PRIVILEGES;
```

### 3. 环境变量配置
复制 `.env.example` 为 `.env` 并修改以下配置：

```bash
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=examsphere

# 或者使用完整的数据库URL
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/examsphere
```

## 初始化数据库

### 方法1：使用初始化脚本
```bash
cd backend
python init_db.py
```

### 方法2：使用Flask-Migrate
```bash
cd backend

# 初始化迁移
python migrate.py init

# 创建迁移文件
python migrate.py create "Initial migration"

# 执行迁移
python migrate.py upgrade
```

### 方法3：使用Flask CLI
```bash
cd backend

# 初始化迁移
flask db init

# 创建迁移文件
flask db migrate -m "Initial migration"

# 执行迁移
flask db upgrade
```

## 默认数据

系统会自动创建默认管理员用户：
- 用户名: `admin`
- 密码: `admin123`
- 邮箱: `admin@examsphere.com`
- 角色: `admin`

**重要：请在生产环境中及时修改默认密码！**

## 数据库表结构

### 核心表
- `users` - 用户表
- `subjects` - 科目表
- `questions` - 试题表
- `exams` - 考试表
- `exam_records` - 考试记录表

### 设计特点
- 无外键约束，所有关联关系在业务层处理
- 使用JSON字段存储复杂数据结构
- 关键字段建立索引提高查询性能
- 支持软删除（通过status字段）

## 备份和恢复

### 备份数据库
```bash
mysqldump -u root -p examsphere > examsphere_backup.sql
```

### 恢复数据库
```bash
mysql -u root -p examsphere < examsphere_backup.sql
```

## 性能优化建议

### 1. 索引优化
- 为经常查询的字段添加索引
- 避免过多索引影响写入性能

### 2. 查询优化
- 使用分页查询避免大量数据加载
- 合理使用JOIN查询
- 避免SELECT *，只查询需要的字段

### 3. 连接池配置
```python
# 在配置文件中添加
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}
```

## 故障排除

### 常见问题

1. **连接失败**
   - 检查MySQL服务是否启动
   - 验证用户名密码是否正确
   - 确认数据库是否存在

2. **字符编码问题**
   - 确保数据库使用utf8mb4字符集
   - 检查连接字符串中的字符集设置

3. **权限问题**
   - 确保用户有足够的数据库权限
   - 检查防火墙设置

### 日志查看
```bash
# 查看MySQL错误日志
tail -f /var/log/mysql/error.log

# 查看应用日志
tail -f app.log
```
