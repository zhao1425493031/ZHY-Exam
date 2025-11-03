-- ExamSphere 考试管理系统数据库DDL脚本
-- 创建时间: 2024年3月15日  
-- 数据库版本: MySQL 8.0+
-- 字符集: utf8mb4
-- 排序规则: utf8mb4_unicode_ci
-- 注意: 所有外键约束和CHECK约束已移除，在应用层进行逻辑验证

-- 设置字符集和排序规则
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS `examsphere` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `examsphere`;

-- =============================================
-- 1. 用户表 (users)
-- =============================================
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    `email` VARCHAR(100) UNIQUE NOT NULL COMMENT '邮箱',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `real_name` VARCHAR(50) COMMENT '真实姓名',
    `role` ENUM('admin', 'user') DEFAULT 'user' COMMENT '角色',
    `status` ENUM('active', 'inactive', 'banned') DEFAULT 'active' COMMENT '状态',
    `avatar_url` VARCHAR(255) COMMENT '头像URL',
    `phone` VARCHAR(20) COMMENT '手机号',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_username` (`username`),
    INDEX `idx_email` (`email`),
    INDEX `idx_role` (`role`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- =============================================
-- 2. 科目表 (subjects)
-- =============================================
DROP TABLE IF EXISTS `subjects`;
CREATE TABLE `subjects` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL COMMENT '科目名称',
    `code` VARCHAR(20) UNIQUE NOT NULL COMMENT '科目代码',
    `description` TEXT COMMENT '科目描述',
    `category` VARCHAR(50) COMMENT '科目分类',
    `status` ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
    `is_free` BOOLEAN DEFAULT TRUE COMMENT '是否免费',
    `price` DECIMAL(10,2) DEFAULT 0.00 COMMENT '现价（元）',
    `original_price` DECIMAL(10,2) DEFAULT 0.00 COMMENT '原价（元）',
    `discount_rate` INT DEFAULT 100 COMMENT '折扣率（%，1-100的整数）',
    `cover_image` VARCHAR(500) COMMENT '课程封面图片URL',
    `created_by` INT COMMENT '创建者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_name` (`name`),
    INDEX `idx_code` (`code`),
    INDEX `idx_status` (`status`),
    INDEX `idx_category` (`category`),
    INDEX `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='科目表';

-- =============================================
-- 3. 试题表 (questions)
-- =============================================
DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `type` ENUM('single', 'multiple', 'judge', 'fill', 'essay') NOT NULL COMMENT '题型',
    `title` TEXT NOT NULL COMMENT '题目标题',
    `content` TEXT COMMENT '题目内容',
    `options` JSON COMMENT '选项（JSON格式）',
    `answer` TEXT NOT NULL COMMENT '正确答案',
    `explanation` TEXT COMMENT '答案解析',
    `difficulty` ENUM('easy', 'medium', 'hard') DEFAULT 'medium' COMMENT '难度',
    `tags` JSON COMMENT '标签（JSON格式）',
    `points` INT DEFAULT 1 COMMENT '分值',
    `status` ENUM('draft', 'published', 'archived') DEFAULT 'draft' COMMENT '状态',
    `created_by` INT COMMENT '创建者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_type` (`type`),
    INDEX `idx_difficulty` (`difficulty`),
    INDEX `idx_status` (`status`),
    INDEX `idx_created_by` (`created_by`),
    INDEX `idx_points` (`points`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='试题表';

-- =============================================
-- 4. 考试表 (exams)
-- =============================================
DROP TABLE IF EXISTS `exams`;
CREATE TABLE `exams` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(200) NOT NULL COMMENT '考试标题',
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `description` TEXT COMMENT '考试描述',
    `duration` INT NOT NULL COMMENT '考试时长(分钟)',
    `total_points` INT NOT NULL COMMENT '总分',
    `passing_score` INT COMMENT '合格分数',
    `question_count` INT NOT NULL COMMENT '题目数量',
    `question_ids` JSON NOT NULL COMMENT '试题ID列表（JSON格式）',
    `start_time` TIMESTAMP COMMENT '开始时间',
    `end_time` TIMESTAMP COMMENT '结束时间',
    `status` ENUM('draft', 'published', 'ongoing', 'finished', 'cancelled') DEFAULT 'draft' COMMENT '状态',
    `settings` JSON COMMENT '考试设置（JSON格式）',
    `created_by` INT COMMENT '创建者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_created_by` (`created_by`),
    INDEX `idx_start_time` (`start_time`),
    INDEX `idx_end_time` (`end_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试表';

-- =============================================
-- 5. 考试记录表 (exam_records)
-- =============================================
DROP TABLE IF EXISTS `exam_records`;
CREATE TABLE `exam_records` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `exam_id` INT NOT NULL COMMENT '考试ID',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `start_time` TIMESTAMP COMMENT '开始时间',
    `submit_time` TIMESTAMP COMMENT '提交时间',
    `answers` JSON COMMENT '用户答案（JSON格式）',
    `score` DECIMAL(5,2) COMMENT '得分',
    `correct_count` INT DEFAULT 0 COMMENT '正确题数',
    `total_count` INT DEFAULT 0 COMMENT '总题数',
    `status` ENUM('in_progress', 'submitted', 'timeout', 'cancelled') DEFAULT 'in_progress' COMMENT '状态',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_exam_id` (`exam_id`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_start_time` (`start_time`),
    INDEX `idx_submit_time` (`submit_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试记录表 - 允许用户重复考试';

-- =============================================
-- 6. 用户收藏表 (user_favorites)
-- =============================================
DROP TABLE IF EXISTS `user_favorites`;
CREATE TABLE `user_favorites` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `question_id` INT NOT NULL COMMENT '试题ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_question_id` (`question_id`),
    UNIQUE KEY `unique_user_question` (`user_id`, `question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏表';

-- =============================================
-- 7. 错题记录表 (wrong_answers)
-- =============================================
DROP TABLE IF EXISTS `wrong_answers`;
CREATE TABLE `wrong_answers` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `question_id` INT NOT NULL COMMENT '试题ID',
    `exam_record_id` INT COMMENT '考试记录ID',
    `user_answer` TEXT COMMENT '用户答案',
    `correct_answer` TEXT COMMENT '正确答案',
    `is_reviewed` BOOLEAN DEFAULT FALSE COMMENT '是否已复习',
    `reviewed_at` TIMESTAMP NULL COMMENT '复习时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_question_id` (`question_id`),
    INDEX `idx_exam_record_id` (`exam_record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='错题记录表';

-- =============================================
-- 8. 系统配置表 (system_configs)
-- =============================================
DROP TABLE IF EXISTS `system_configs`;
CREATE TABLE `system_configs` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `config_key` VARCHAR(100) UNIQUE NOT NULL COMMENT '配置键',
    `config_value` TEXT COMMENT '配置值',
    `config_type` ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string' COMMENT '配置类型',
    `description` TEXT COMMENT '配置描述',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_config_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- =============================================
-- 9. 消息通知表 (notifications)
-- =============================================
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `title` VARCHAR(200) NOT NULL COMMENT '通知标题',
    `content` TEXT COMMENT '通知内容',
    `type` ENUM('system', 'exam', 'score', 'announcement') DEFAULT 'system' COMMENT '通知类型',
    `is_read` BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    `read_at` TIMESTAMP NULL COMMENT '阅读时间',
    `related_id` INT COMMENT '关联记录ID',
    `related_type` VARCHAR(50) COMMENT '关联记录类型',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_type` (`type`),
    INDEX `idx_is_read` (`is_read`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息通知表';

-- =============================================
-- 10. 文件管理表 (files)
-- =============================================
DROP TABLE IF EXISTS `files`;
CREATE TABLE `files` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `filename` VARCHAR(255) NOT NULL COMMENT '文件名',
    `original_name` VARCHAR(255) NOT NULL COMMENT '原始文件名',
    `file_path` VARCHAR(500) NOT NULL COMMENT '文件路径',
    `file_size` BIGINT NOT NULL COMMENT '文件大小（字节）',
    `file_type` VARCHAR(100) COMMENT '文件类型',
    `uploader_id` INT NOT NULL COMMENT '上传者ID',
    `related_type` VARCHAR(50) COMMENT '关联类型（question, user, exam等）',
    `related_id` INT COMMENT '关联记录ID',
    `description` TEXT COMMENT '文件描述',
    `is_public` BOOLEAN DEFAULT FALSE COMMENT '是否公开',
    `download_count` INT DEFAULT 0 COMMENT '下载次数',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_uploader_id` (`uploader_id`),
    INDEX `idx_related_type` (`related_type`),
    INDEX `idx_related_id` (`related_id`),
    INDEX `idx_file_type` (`file_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文件管理表';

-- =============================================
-- 11. 操作日志表 (operation_logs)
-- =============================================
DROP TABLE IF EXISTS `operation_logs`;
CREATE TABLE `operation_logs` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT COMMENT '用户ID',
    `operation_type` VARCHAR(50) NOT NULL COMMENT '操作类型',
    `operation_desc` TEXT COMMENT '操作描述',
    `ip_address` VARCHAR(45) COMMENT 'IP地址',
    `user_agent` TEXT COMMENT '用户代理',
    `request_data` JSON COMMENT '请求数据（JSON格式）',
    `response_data` JSON COMMENT '响应数据（JSON格式）',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_operation_type` (`operation_type`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='操作日志表';

-- =============================================
-- 12. 考试监控表 (exam_monitoring)
-- =============================================
DROP TABLE IF EXISTS `exam_monitoring`;
CREATE TABLE `exam_monitoring` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `exam_record_id` INT NOT NULL COMMENT '考试记录ID',
    `event_type` ENUM('start', 'pause', 'resume', 'submit', 'timeout', 'cheat') NOT NULL COMMENT '事件类型',
    `event_data` JSON COMMENT '事件数据（JSON格式）',
    `ip_address` VARCHAR(45) COMMENT 'IP地址',
    `user_agent` TEXT COMMENT '用户代理',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_exam_record_id` (`exam_record_id`),
    INDEX `idx_event_type` (`event_type`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试监控表';

-- =============================================
-- 13. 系统公告表 (announcements)
-- =============================================
DROP TABLE IF EXISTS `announcements`;
CREATE TABLE `announcements` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(200) NOT NULL COMMENT '公告标题',
    `content` TEXT NOT NULL COMMENT '公告内容',
    `type` ENUM('system', 'exam', 'maintenance') DEFAULT 'system' COMMENT '公告类型',
    `priority` ENUM('low', 'medium', 'high') DEFAULT 'medium' COMMENT '优先级',
    `status` ENUM('draft', 'published', 'archived') DEFAULT 'draft' COMMENT '状态',
    `publish_time` TIMESTAMP COMMENT '发布时间',
    `expire_time` TIMESTAMP COMMENT '过期时间',
    `view_count` INT DEFAULT 0 COMMENT '查看次数',
    `created_by` INT COMMENT '创建者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_type` (`type`),
    INDEX `idx_status` (`status`),
    INDEX `idx_priority` (`priority`),
    INDEX `idx_publish_time` (`publish_time`),
    INDEX `idx_expire_time` (`expire_time`),
    INDEX `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统公告表';

-- =============================================
-- 14. 权限表 (permissions)
-- =============================================
DROP TABLE IF EXISTS `permissions`;
CREATE TABLE `permissions` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL COMMENT '权限名称',
    `code` VARCHAR(100) UNIQUE NOT NULL COMMENT '权限代码',
    `type` ENUM('menu', 'button', 'api', 'data') DEFAULT 'menu' COMMENT '权限类型',
    `parent_id` INT DEFAULT 0 COMMENT '父权限ID',
    `path` VARCHAR(200) COMMENT '路径',
    `icon` VARCHAR(100) COMMENT '图标',
    `sort_order` INT DEFAULT 0 COMMENT '排序',
    `status` ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_code` (`code`),
    INDEX `idx_type` (`type`),
    INDEX `idx_parent_id` (`parent_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_sort_order` (`sort_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='权限表';

-- =============================================
-- 15. 角色权限关联表 (role_permissions)
-- =============================================
DROP TABLE IF EXISTS `role_permissions`;
CREATE TABLE `role_permissions` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `role` VARCHAR(50) NOT NULL COMMENT '角色',
    `permission_id` INT NOT NULL COMMENT '权限ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_role` (`role`),
    INDEX `idx_permission_id` (`permission_id`),
    UNIQUE KEY `unique_role_permission` (`role`, `permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色权限关联表';

-- =============================================
-- 16. 考试模板表 (exam_templates)
-- =============================================
DROP TABLE IF EXISTS `exam_templates`;
CREATE TABLE `exam_templates` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL COMMENT '模板名称',
    `description` TEXT COMMENT '模板描述',
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `template_config` JSON NOT NULL COMMENT '模板配置（JSON格式）',
    `question_rules` JSON COMMENT '选题规则（JSON格式）',
    `is_public` BOOLEAN DEFAULT FALSE COMMENT '是否公开',
    `usage_count` INT DEFAULT 0 COMMENT '使用次数',
    `created_by` INT COMMENT '创建者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_is_public` (`is_public`),
    INDEX `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考试模板表';

-- =============================================
-- 17. 学习路径表 (learning_paths)
-- =============================================
DROP TABLE IF EXISTS `learning_paths`;
CREATE TABLE `learning_paths` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(200) NOT NULL COMMENT '学习路径名称',
    `description` TEXT COMMENT '学习路径描述',
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `path_config` JSON NOT NULL COMMENT '学习路径配置（JSON格式）',
    `difficulty_level` ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner' COMMENT '难度等级',
    `estimated_hours` INT DEFAULT 0 COMMENT '预计学习时长（小时）',
    `status` ENUM('draft', 'published', 'archived') DEFAULT 'draft' COMMENT '状态',
    `created_by` INT COMMENT '创建者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_difficulty_level` (`difficulty_level`),
    INDEX `idx_status` (`status`),
    INDEX `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习路径表';

-- =============================================
-- 18. 用户学习路径表 (user_learning_paths)
-- =============================================
DROP TABLE IF EXISTS `user_learning_paths`;
CREATE TABLE `user_learning_paths` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `learning_path_id` INT NOT NULL COMMENT '学习路径ID',
    `progress` JSON COMMENT '学习进度（JSON格式）',
    `current_step` INT DEFAULT 0 COMMENT '当前步骤',
    `completed_steps` JSON COMMENT '已完成步骤（JSON格式）',
    `start_time` TIMESTAMP COMMENT '开始时间',
    `completion_time` TIMESTAMP COMMENT '完成时间',
    `status` ENUM('in_progress', 'completed', 'paused', 'abandoned') DEFAULT 'in_progress' COMMENT '状态',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_learning_path_id` (`learning_path_id`),
    INDEX `idx_status` (`status`),
    UNIQUE KEY `unique_user_path` (`user_id`, `learning_path_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户学习路径表';

-- =============================================
-- 19. 在线答疑表 (qa_sessions)
-- =============================================
DROP TABLE IF EXISTS `qa_sessions`;
CREATE TABLE `qa_sessions` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `student_id` INT NOT NULL COMMENT '学生ID',
    `teacher_id` INT COMMENT '教师ID',
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `question_title` VARCHAR(200) NOT NULL COMMENT '问题标题',
    `question_content` TEXT NOT NULL COMMENT '问题内容',
    `answer_content` TEXT COMMENT '回答内容',
    `status` ENUM('pending', 'answered', 'closed') DEFAULT 'pending' COMMENT '状态',
    `priority` ENUM('low', 'medium', 'high', 'urgent') DEFAULT 'medium' COMMENT '优先级',
    `category` VARCHAR(100) COMMENT '问题分类',
    `tags` JSON COMMENT '标签（JSON格式）',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `answered_at` TIMESTAMP COMMENT '回答时间',
    `closed_at` TIMESTAMP COMMENT '关闭时间',
    INDEX `idx_student_id` (`student_id`),
    INDEX `idx_teacher_id` (`teacher_id`),
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_priority` (`priority`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='在线答疑表';

-- =============================================
-- 20. 用户购买记录表 (user_purchases)
-- =============================================
DROP TABLE IF EXISTS `user_purchases`;
CREATE TABLE `user_purchases` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `order_id` VARCHAR(50) UNIQUE NOT NULL COMMENT '订单号',
    `payment_method` ENUM('alipay', 'wechat', 'paypal', 'admin') NOT NULL COMMENT '支付方式',
    `amount` DECIMAL(10,2) NOT NULL COMMENT '支付金额',
    `original_amount` DECIMAL(10,2) NOT NULL COMMENT '原价',
    `discount_amount` DECIMAL(10,2) DEFAULT 0.00 COMMENT '优惠金额',
    `status` ENUM('pending', 'paid', 'cancelled', 'refunded') DEFAULT 'pending' COMMENT '支付状态',
    `payment_time` TIMESTAMP COMMENT '支付时间',
    `expire_time` TIMESTAMP COMMENT '到期时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_order_id` (`order_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_payment_method` (`payment_method`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户购买记录表';

-- =============================================
-- 21. 支付订单表 (payment_orders)
-- =============================================
DROP TABLE IF EXISTS `payment_orders`;
CREATE TABLE `payment_orders` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `order_id` VARCHAR(50) UNIQUE NOT NULL COMMENT '订单号',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `payment_method` ENUM('alipay', 'wechat', 'paypal', 'admin') NOT NULL COMMENT '支付方式',
    `amount` DECIMAL(10,2) NOT NULL COMMENT '支付金额',
    `currency` VARCHAR(10) DEFAULT 'CNY' COMMENT '货币类型',
    `status` ENUM('pending', 'paid', 'cancelled', 'refunded', 'failed') DEFAULT 'pending' COMMENT '支付状态',
    `third_party_order_id` VARCHAR(100) COMMENT '第三方支付订单号',
    `payment_url` TEXT COMMENT '支付链接',
    `callback_data` JSON COMMENT '支付回调数据（JSON格式）',
    `paid_at` TIMESTAMP COMMENT '支付完成时间',
    `expired_at` TIMESTAMP COMMENT '订单过期时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_order_id` (`order_id`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_payment_method` (`payment_method`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='支付订单表';

-- =============================================
-- 22. 退款记录表 (refund_records)
-- =============================================
DROP TABLE IF EXISTS `refund_records`;
CREATE TABLE `refund_records` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `order_id` VARCHAR(50) NOT NULL COMMENT '订单号',
    `user_id` INT NOT NULL COMMENT '用户ID',
    `refund_amount` DECIMAL(10,2) NOT NULL COMMENT '退款金额',
    `refund_reason` TEXT COMMENT '退款原因',
    `refund_method` ENUM('alipay', 'wechat', 'paypal', 'manual') NOT NULL COMMENT '退款方式',
    `status` ENUM('pending', 'approved', 'rejected', 'completed') DEFAULT 'pending' COMMENT '退款状态',
    `admin_id` INT COMMENT '处理管理员ID',
    `admin_note` TEXT COMMENT '管理员备注',
    `processed_at` TIMESTAMP COMMENT '处理时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_order_id` (`order_id`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_refund_method` (`refund_method`),
    INDEX `idx_admin_id` (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='退款记录表';

-- =============================================
-- 23. 优惠券表 (coupons)
-- =============================================
DROP TABLE IF EXISTS `coupons`;
CREATE TABLE `coupons` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `code` VARCHAR(50) UNIQUE NOT NULL COMMENT '优惠券代码',
    `name` VARCHAR(100) NOT NULL COMMENT '优惠券名称',
    `type` ENUM('percentage', 'fixed') NOT NULL COMMENT '优惠类型：百分比/固定金额',
    `value` DECIMAL(10,2) NOT NULL COMMENT '优惠值',
    `min_amount` DECIMAL(10,2) DEFAULT 0.00 COMMENT '最低消费金额',
    `max_discount` DECIMAL(10,2) DEFAULT 0.00 COMMENT '最大优惠金额',
    `usage_limit` INT DEFAULT 1 COMMENT '使用次数限制',
    `used_count` INT DEFAULT 0 COMMENT '已使用次数',
    `valid_from` TIMESTAMP NOT NULL COMMENT '有效期开始',
    `valid_to` TIMESTAMP NOT NULL COMMENT '有效期结束',
    `status` ENUM('active', 'inactive', 'expired') DEFAULT 'active' COMMENT '状态',
    `created_by` INT NOT NULL COMMENT '创建者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_code` (`code`),
    INDEX `idx_status` (`status`),
    INDEX `idx_valid_from` (`valid_from`),
    INDEX `idx_valid_to` (`valid_to`),
    INDEX `idx_created_by` (`created_by`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='优惠券表';

-- =============================================
-- 24. 用户优惠券表 (user_coupons)
-- =============================================
DROP TABLE IF EXISTS `user_coupons`;
CREATE TABLE `user_coupons` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `coupon_id` INT NOT NULL COMMENT '优惠券ID',
    `order_id` VARCHAR(50) COMMENT '使用的订单号',
    `used_at` TIMESTAMP COMMENT '使用时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_coupon_id` (`coupon_id`),
    INDEX `idx_order_id` (`order_id`),
    UNIQUE KEY `unique_user_coupon` (`user_id`, `coupon_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户优惠券表';

-- =============================================
-- 25. 导入记录表 (import_records)
-- =============================================
DROP TABLE IF EXISTS `import_records`;
CREATE TABLE `import_records` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `import_type` ENUM('users', 'questions', 'subjects') NOT NULL COMMENT '导入类型',
    `filename` VARCHAR(255) NOT NULL COMMENT '文件名',
    `file_path` VARCHAR(500) NOT NULL COMMENT '文件路径',
    `total_count` INT DEFAULT 0 COMMENT '总记录数',
    `success_count` INT DEFAULT 0 COMMENT '成功记录数',
    `failed_count` INT DEFAULT 0 COMMENT '失败记录数',
    `error_details` JSON COMMENT '错误详情（JSON格式）',
    `status` ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending' COMMENT '状态',
    `imported_by` INT COMMENT '导入者ID',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX `idx_import_type` (`import_type`),
    INDEX `idx_status` (`status`),
    INDEX `idx_imported_by` (`imported_by`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='导入记录表';

-- =============================================
-- 26. 系统日志表 (system_logs)
-- =============================================
DROP TABLE IF EXISTS `system_logs`;
CREATE TABLE `system_logs` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `log_level` ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL COMMENT '日志级别',
    `module` VARCHAR(100) NOT NULL COMMENT '模块名称',
    `message` TEXT NOT NULL COMMENT '日志消息',
    `user_id` INT COMMENT '操作用户ID',
    `ip_address` VARCHAR(45) COMMENT 'IP地址',
    `user_agent` TEXT COMMENT '用户代理',
    `request_data` JSON COMMENT '请求数据（JSON格式）',
    `response_data` JSON COMMENT '响应数据（JSON格式）',
    `execution_time` DECIMAL(10,3) COMMENT '执行时间（秒）',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_log_level` (`log_level`),
    INDEX `idx_module` (`module`),
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统日志表';

-- =============================================
-- 27. 日志配置表 (log_configs)
-- =============================================
DROP TABLE IF EXISTS `log_configs`;
CREATE TABLE `log_configs` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `config_key` VARCHAR(100) UNIQUE NOT NULL COMMENT '配置键',
    `config_value` TEXT NOT NULL COMMENT '配置值',
    `description` TEXT COMMENT '配置描述',
    `is_active` BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='日志配置表';


-- 创建用户科目关联表
CREATE TABLE IF NOT EXISTS `user_subjects` (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL COMMENT '用户ID',
    `subject_id` INT NOT NULL COMMENT '科目ID',
    `is_free` BOOLEAN DEFAULT TRUE COMMENT '是否免费订阅',
    `purchased_at` TIMESTAMP NULL COMMENT '购买时间（付费课程）',
    `expires_at` TIMESTAMP NULL COMMENT '到期时间（付费课程）',
    `status` ENUM('active', 'expired', 'cancelled') DEFAULT 'active' COMMENT '订阅状态',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    
    -- 索引
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_subject_id` (`subject_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_expires_at` (`expires_at`),
    
    -- 唯一约束：一个用户只能订阅一个科目一次
    UNIQUE KEY `unique_user_subject` (`user_id`, `subject_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户科目关联表';

-- =============================================
-- 初始化数据
-- =============================================

-- 插入默认管理员用户
INSERT INTO `users` (`username`, `email`, `password_hash`, `real_name`, `role`, `status`) VALUES
('admin', 'admin@examsphere.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Qz8K2', '系统管理员', 'admin', 'active');

-- 插入系统配置
INSERT INTO `system_configs` (`config_key`, `config_value`, `config_type`, `description`) VALUES
('system_name', 'ExamSphere 考试管理系统', 'string', '系统名称'),
('system_version', '1.0.0', 'string', '系统版本'),
('max_file_size', '10485760', 'number', '最大文件上传大小（字节）'),
('exam_time_limit', '120', 'number', '默认考试时长（分钟）'),
('enable_registration', 'true', 'boolean', '是否允许用户注册'),
('enable_notifications', 'true', 'boolean', '是否启用通知功能');

-- 插入默认权限
INSERT INTO `permissions` (`name`, `code`, `type`, `parent_id`, `path`, `icon`, `sort_order`) VALUES
('用户管理', 'user_management', 'menu', 0, '/admin/users', 'User', 1),
('科目管理', 'subject_management', 'menu', 0, '/admin/subjects', 'Book', 2),
('试题管理', 'question_management', 'menu', 0, '/admin/questions', 'QuestionFilled', 3),
('考试管理', 'exam_management', 'menu', 0, '/admin/exams', 'Document', 4),
('统计分析', 'statistics_analysis', 'menu', 0, '/admin/statistics', 'TrendCharts', 5),
('权限管理', 'permission_management', 'menu', 0, '/admin/permissions', 'Lock', 6),
('数据导入导出', 'import_export', 'menu', 0, '/admin/import-export', 'Upload', 7),
('系统公告', 'announcement_management', 'menu', 0, '/admin/announcements', 'Bell', 8);

-- 为管理员角色分配所有权限
INSERT INTO `role_permissions` (`role`, `permission_id`) 
SELECT 'admin', `id` FROM `permissions`;

-- 为普通用户角色分配基础权限
INSERT INTO `role_permissions` (`role`, `permission_id`) 
SELECT 'user', `id` FROM `permissions` WHERE `code` IN ('subject_management', 'question_management', 'exam_management');

-- 插入默认日志配置
INSERT INTO `log_configs` (`config_key`, `config_value`, `description`) VALUES
('LOG_LEVEL', 'INFO', '日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)'),
('LOG_MAX_SIZE', '10485760', '单个日志文件最大大小（字节），默认10MB'),
('LOG_BACKUP_COUNT', '30', '日志文件备份数量，默认保留30个'),
('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s', '日志格式'),
('LOG_ENABLE_FILE', 'true', '是否启用文件日志 (true/false)'),
('LOG_ENABLE_DATABASE', 'true', '是否启用数据库日志 (true/false)'),
('LOG_RETENTION_DAYS', '30', '日志保留天数'),
('LOG_ENABLE_CONSOLE', 'true', '是否启用控制台日志 (true/false)'),
('LOG_ENABLE_ERROR_FILE', 'true', '是否启用错误日志单独文件 (true/false)'),
('LOG_ENABLE_ROTATION', 'true', '是否启用日志轮转 (true/false)');

-- 恢复外键检查
-- 用户设置表 (user_settings)
DROP TABLE IF EXISTS `user_settings`;
CREATE TABLE `user_settings` (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    email_notifications BOOLEAN DEFAULT TRUE NOT NULL,
    system_notifications BOOLEAN DEFAULT TRUE NOT NULL,
    exam_notifications BOOLEAN DEFAULT TRUE NOT NULL,
    score_notifications BOOLEAN DEFAULT TRUE NOT NULL,
    announcement_notifications BOOLEAN DEFAULT TRUE NOT NULL,
    theme VARCHAR(20) DEFAULT 'light' NOT NULL,
    language VARCHAR(10) DEFAULT 'zh' NOT NULL,
    timezone VARCHAR(50) DEFAULT 'Asia/Shanghai' NOT NULL,
    extra_settings JSON DEFAULT ('{}'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP NOT NULL
);

-- 添加索引
CREATE INDEX idx_user_settings_user_id ON user_settings(user_id);

-- 为现有用户创建默认设置
INSERT INTO user_settings (user_id, email_notifications, system_notifications, exam_notifications, score_notifications, announcement_notifications)
SELECT id, TRUE, TRUE, TRUE, TRUE, TRUE
FROM users
WHERE id NOT IN (SELECT user_id FROM user_settings);


SET FOREIGN_KEY_CHECKS = 1;

-- 显示创建结果
SELECT 'ExamSphere 数据库创建完成！（无外键约束版本）' AS message;
SELECT COUNT(*) AS table_count FROM information_schema.tables WHERE table_schema = 'examsphere';
SELECT table_name FROM information_schema.tables WHERE table_schema = 'examsphere' ORDER BY table_name;

