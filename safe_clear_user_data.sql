-- =============================================
-- 安全清空用户业务数据脚本（带备份和验证）
-- 用途：安全地清空用户考试相关数据
-- 作者：ExamSphere 系统
-- 日期：2025-10-12
-- =============================================

-- =============================================
-- 第一步：创建备份表（可选）
-- =============================================

-- 如果需要备份数据，请取消以下注释并执行
/*
-- 备份考试记录
CREATE TABLE exam_records_backup AS SELECT * FROM exam_records;
SELECT '已创建考试记录备份表' AS backup_status;

-- 备份错题记录
CREATE TABLE wrong_answers_backup AS SELECT * FROM wrong_answers;
SELECT '已创建错题记录备份表' AS backup_status;

-- 备份用户购买记录
CREATE TABLE user_purchases_backup AS SELECT * FROM user_purchases;
SELECT '已创建用户购买记录备份表' AS backup_status;
*/

-- =============================================
-- 第二步：显示清理前的数据统计
-- =============================================

SELECT '清理前数据统计：' AS status;

SELECT 
    'exam_records' AS table_name,
    COUNT(*) AS record_count,
    '考试记录' AS description
FROM exam_records
UNION ALL
SELECT 
    'wrong_answers' AS table_name,
    COUNT(*) AS record_count,
    '错题记录' AS description
FROM wrong_answers
UNION ALL
SELECT 
    'exam_monitoring' AS table_name,
    COUNT(*) AS record_count,
    '考试监控记录' AS description
FROM exam_monitoring
UNION ALL
SELECT 
    'user_favorites' AS table_name,
    COUNT(*) AS record_count,
    '用户收藏' AS description
FROM user_favorites
UNION ALL
SELECT 
    'user_purchases' AS table_name,
    COUNT(*) AS record_count,
    '用户购买记录' AS description
FROM user_purchases
UNION ALL
SELECT 
    'notifications' AS table_name,
    COUNT(*) AS record_count,
    '消息通知' AS description
FROM notifications;

-- =============================================
-- 第三步：确认清理操作
-- =============================================

-- 请手动确认是否继续执行清理操作
-- 如果需要继续，请取消以下注释

/*
-- =============================================
-- 第四步：执行清理操作
-- =============================================

-- 设置安全模式
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_SAFE_UPDATES = 0;

-- 开始事务
START TRANSACTION;

-- 清空用户业务数据
TRUNCATE TABLE exam_records;
TRUNCATE TABLE wrong_answers;
TRUNCATE TABLE exam_monitoring;
TRUNCATE TABLE user_favorites;
TRUNCATE TABLE user_learning_paths;
TRUNCATE TABLE qa_sessions;
TRUNCATE TABLE user_purchases;
TRUNCATE TABLE payment_orders;
TRUNCATE TABLE refund_records;
TRUNCATE TABLE user_coupons;
TRUNCATE TABLE notifications;
TRUNCATE TABLE operation_logs;
TRUNCATE TABLE system_logs;

-- 重置自增ID
ALTER TABLE exam_records AUTO_INCREMENT = 1;
ALTER TABLE wrong_answers AUTO_INCREMENT = 1;
ALTER TABLE exam_monitoring AUTO_INCREMENT = 1;
ALTER TABLE user_favorites AUTO_INCREMENT = 1;
ALTER TABLE user_learning_paths AUTO_INCREMENT = 1;
ALTER TABLE qa_sessions AUTO_INCREMENT = 1;
ALTER TABLE user_purchases AUTO_INCREMENT = 1;
ALTER TABLE payment_orders AUTO_INCREMENT = 1;
ALTER TABLE refund_records AUTO_INCREMENT = 1;
ALTER TABLE user_coupons AUTO_INCREMENT = 1;
ALTER TABLE notifications AUTO_INCREMENT = 1;
ALTER TABLE operation_logs AUTO_INCREMENT = 1;
ALTER TABLE system_logs AUTO_INCREMENT = 1;

-- 恢复安全设置
SET FOREIGN_KEY_CHECKS = 1;
SET SQL_SAFE_UPDATES = 1;

-- 提交事务
COMMIT;

SELECT '数据清理完成！' AS status;
*/

-- =============================================
-- 第五步：清理后验证（需要在执行清理后运行）
-- =============================================

/*
SELECT '清理后数据统计：' AS status;

SELECT 
    'exam_records' AS table_name,
    COUNT(*) AS record_count,
    '考试记录' AS description
FROM exam_records
UNION ALL
SELECT 
    'wrong_answers' AS table_name,
    COUNT(*) AS record_count,
    '错题记录' AS description
FROM wrong_answers
UNION ALL
SELECT 
    'exam_monitoring' AS table_name,
    COUNT(*) AS record_count,
    '考试监控记录' AS description
FROM exam_monitoring
UNION ALL
SELECT 
    'user_favorites' AS table_name,
    COUNT(*) AS record_count,
    '用户收藏' AS description
FROM user_favorites
UNION ALL
SELECT 
    'user_purchases' AS table_name,
    COUNT(*) AS record_count,
    '用户购买记录' AS description
FROM user_purchases
UNION ALL
SELECT 
    'notifications' AS table_name,
    COUNT(*) AS record_count,
    '消息通知' AS description
FROM notifications;
*/

-- =============================================
-- 使用说明：
-- 1. 首先运行此脚本查看清理前的数据统计
-- 2. 如果需要备份，取消备份部分的注释并执行
-- 3. 确认无误后，取消第四步的注释并执行清理操作
-- 4. 最后运行第五步验证清理结果
-- =============================================
