-- 在线考试系统数据库DDL
-- 创建时间: 2024
-- 数据库: MySQL 8.0+

-- 创建数据库
CREATE DATABASE IF NOT EXISTS exam_system 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE exam_system;

-- 用户表
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    username VARCHAR(80) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(120) NOT NULL UNIQUE COMMENT '邮箱地址',
    password_hash VARCHAR(128) NOT NULL COMMENT '密码哈希',
    role ENUM('admin', 'user') DEFAULT 'user' COMMENT '用户角色',
    is_verified BOOLEAN DEFAULT FALSE COMMENT '是否已验证邮箱',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 验证码表
CREATE TABLE verification_codes (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '验证码ID',
    email VARCHAR(120) NOT NULL COMMENT '邮箱地址',
    code VARCHAR(6) NOT NULL COMMENT '验证码',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    expires_at TIMESTAMP NOT NULL COMMENT '过期时间',
    is_used BOOLEAN DEFAULT FALSE COMMENT '是否已使用'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='验证码表';

-- 题目表
CREATE TABLE questions (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '题目ID',
    content TEXT NOT NULL COMMENT '题目内容',
    type ENUM('single', 'multiple', 'text', 'audio', 'video') NOT NULL COMMENT '题目类型',
    options JSON COMMENT '选项（JSON格式）',
    correct_answer TEXT NOT NULL COMMENT '正确答案',
    explanation TEXT COMMENT '题目解析',
    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium' COMMENT '难度等级',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='题目表';

-- 考试表
CREATE TABLE exams (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '考试ID',
    title VARCHAR(200) NOT NULL COMMENT '考试标题',
    description TEXT COMMENT '考试描述',
    time_limit INT DEFAULT 60 COMMENT '时间限制（分钟）',
    total_questions INT DEFAULT 50 COMMENT '题目总数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试表';

-- 考试记录表
CREATE TABLE exam_records (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '用户ID',
    exam_id INT NOT NULL COMMENT '考试ID',
    score INT DEFAULT 0 COMMENT '得分',
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '开始时间',
    end_time TIMESTAMP NULL COMMENT '结束时间',
    status ENUM('in_progress', 'completed', 'timeout') DEFAULT 'in_progress' COMMENT '考试状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试记录表';

-- 答题记录表
CREATE TABLE answers (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '答案ID',
    exam_record_id INT NOT NULL COMMENT '考试记录ID',
    question_id INT NOT NULL COMMENT '题目ID',
    user_answer TEXT COMMENT '用户答案',
    is_correct BOOLEAN DEFAULT FALSE COMMENT '是否正确',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='答题记录表';

-- 错题表
CREATE TABLE wrong_questions (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '错题ID',
    user_id INT NOT NULL COMMENT '用户ID',
    question_id INT NOT NULL COMMENT '题目ID',
    exam_record_id INT NOT NULL COMMENT '考试记录ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_question (user_id, question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='错题表';

-- 收藏题目表
CREATE TABLE favorite_questions (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '收藏ID',
    user_id INT NOT NULL COMMENT '用户ID',
    question_id INT NOT NULL COMMENT '题目ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_question (user_id, question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收藏题目表';

-- 系统配置表
CREATE TABLE system_config (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '配置ID',
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    description VARCHAR(255) COMMENT '配置描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 操作日志表
CREATE TABLE operation_logs (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '日志ID',
    user_id INT COMMENT '用户ID',
    operation VARCHAR(100) NOT NULL COMMENT '操作类型',
    description TEXT COMMENT '操作描述',
    ip_address VARCHAR(45) COMMENT 'IP地址',
    user_agent TEXT COMMENT '用户代理',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- 插入默认管理员用户
INSERT INTO users (username, email, password_hash, role, is_verified) VALUES 
('admin', 'admin@example.com', 'pbkdf2:sha256:260000$...', 'admin', TRUE);

-- 插入默认系统配置
INSERT INTO system_config (config_key, config_value, description) VALUES 
('site_name', '在线考试系统', '网站名称'),
('site_description', '专业的在线考试平台', '网站描述'),
('max_upload_size', '16777216', '最大上传文件大小（字节）'),
('exam_timeout', '3600', '考试超时时间（秒）'),
('verification_code_expire', '300', '验证码过期时间（秒）');

-- 创建视图：用户考试统计
CREATE VIEW user_exam_stats AS
SELECT 
    u.id as user_id,
    u.username,
    u.email,
    COUNT(er.id) as total_exams,
    COALESCE(AVG(er.score), 0) as avg_score,
    MAX(er.score) as best_score,
    MIN(er.score) as worst_score,
    COUNT(wq.id) as wrong_questions_count,
    COUNT(fq.id) as favorite_questions_count
FROM users u
LEFT JOIN exam_records er ON u.id = er.user_id AND er.status = 'completed'
LEFT JOIN wrong_questions wq ON u.id = wq.user_id
LEFT JOIN favorite_questions fq ON u.id = fq.user_id
GROUP BY u.id, u.username, u.email;

-- 创建视图：题目统计
CREATE VIEW question_stats AS
SELECT 
    q.id as question_id,
    q.content,
    q.type,
    q.difficulty,
    COUNT(a.id) as total_attempts,
    COUNT(CASE WHEN a.is_correct = TRUE THEN 1 END) as correct_attempts,
    ROUND(COUNT(CASE WHEN a.is_correct = TRUE THEN 1 END) * 100.0 / COUNT(a.id), 2) as correct_rate,
    COUNT(wq.id) as wrong_count,
    COUNT(fq.id) as favorite_count
FROM questions q
LEFT JOIN answers a ON q.id = a.question_id
LEFT JOIN wrong_questions wq ON q.id = wq.question_id
LEFT JOIN favorite_questions fq ON q.id = fq.question_id
GROUP BY q.id, q.content, q.type, q.difficulty;

