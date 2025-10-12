-- =============================================
-- 快速清空用户业务数据脚本
-- 用途：快速清理用户的考试相关数据
-- 注意：此脚本会立即删除数据，请谨慎使用！
-- =============================================

-- 快速清理所有用户业务数据
SET FOREIGN_KEY_CHECKS = 0;

-- 核心业务数据清理
DELETE FROM exam_records;
DELETE FROM wrong_answers;
DELETE FROM exam_monitoring;
DELETE FROM user_favorites;
DELETE FROM user_learning_paths;
DELETE FROM qa_sessions;
DELETE FROM user_purchases;
DELETE FROM payment_orders;
DELETE FROM refund_records;
DELETE FROM user_coupons;
DELETE FROM notifications;
DELETE FROM operation_logs;
DELETE FROM system_logs;

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

SET FOREIGN_KEY_CHECKS = 1;

-- 显示清理结果
SELECT 
    '用户业务数据清理完成' AS status,
    NOW() AS cleanup_time,
    '已清理的表：exam_records, wrong_answers, exam_monitoring, user_favorites, user_learning_paths, qa_sessions, user_purchases, payment_orders, refund_records, user_coupons, notifications, operation_logs, system_logs' AS cleared_tables;
