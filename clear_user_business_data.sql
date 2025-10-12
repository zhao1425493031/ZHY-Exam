-- =============================================
-- 清空用户业务数据 DDL 脚本
-- 用途：清空用户的考试相关数据，保留系统基础数据
-- 注意：此脚本会删除所有用户的考试记录、错题记录等业务数据
-- 执行前请务必备份数据库！
-- =============================================

-- 设置安全模式
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_SAFE_UPDATES = 0;

-- =============================================
-- 1. 清空考试相关记录
-- =============================================

-- 清空考试记录表
TRUNCATE TABLE exam_records;
SELECT '已清空考试记录表 (exam_records)' AS status;

-- 清空错题记录表
TRUNCATE TABLE wrong_answers;
SELECT '已清空错题记录表 (wrong_answers)' AS status;

-- 清空考试监控记录表
TRUNCATE TABLE exam_monitoring;
SELECT '已清空考试监控记录表 (exam_monitoring)' AS status;

-- =============================================
-- 2. 清空用户学习相关数据
-- =============================================

-- 清空用户收藏表
TRUNCATE TABLE user_favorites;
SELECT '已清空用户收藏表 (user_favorites)' AS status;

-- 清空学习进度表
TRUNCATE TABLE user_learning_paths;
SELECT '已清空学习进度表 (user_learning_paths)' AS status;

-- 清空在线答疑表
TRUNCATE TABLE qa_sessions;
SELECT '已清空在线答疑表 (qa_sessions)' AS status;

-- =============================================
-- 3. 清空用户购买和支付记录
-- =============================================

-- 清空用户购买记录表
TRUNCATE TABLE user_purchases;
SELECT '已清空用户购买记录表 (user_purchases)' AS status;

-- 清空支付订单表
TRUNCATE TABLE payment_orders;
SELECT '已清空支付订单表 (payment_orders)' AS status;

-- 清空退款记录表
TRUNCATE TABLE refund_records;
SELECT '已清空退款记录表 (refund_records)' AS status;

-- 清空用户优惠券表
TRUNCATE TABLE user_coupons;
SELECT '已清空用户优惠券表 (user_coupons)' AS status;

-- =============================================
-- 4. 清空用户订阅数据
-- =============================================

-- 清空用户科目订阅表（如果存在）
-- 注意：根据您的数据库设计，这个表名可能需要调整
-- TRUNCATE TABLE user_subjects;
-- SELECT '已清空用户科目订阅表 (user_subjects)' AS status;

-- =============================================
-- 5. 清空用户消息和通知
-- =============================================

-- 清空消息通知表
TRUNCATE TABLE notifications;
SELECT '已清空消息通知表 (notifications)' AS status;

-- =============================================
-- 6. 清空系统日志（可选）
-- =============================================

-- 清空操作日志表
TRUNCATE TABLE operation_logs;
SELECT '已清空操作日志表 (operation_logs)' AS status;

-- 清空系统日志表
TRUNCATE TABLE system_logs;
SELECT '已清空系统日志表 (system_logs)' AS status;

-- =============================================
-- 7. 重置自增ID（可选）
-- =============================================

-- 重置考试记录表的自增ID
ALTER TABLE exam_records AUTO_INCREMENT = 1;
SELECT '已重置考试记录表自增ID' AS status;

-- 重置错题记录表的自增ID
ALTER TABLE wrong_answers AUTO_INCREMENT = 1;
SELECT '已重置错题记录表自增ID' AS status;

-- 重置考试监控表的自增ID
ALTER TABLE exam_monitoring AUTO_INCREMENT = 1;
SELECT '已重置考试监控表自增ID' AS status;

-- 重置用户收藏表的自增ID
ALTER TABLE user_favorites AUTO_INCREMENT = 1;
SELECT '已重置用户收藏表自增ID' AS status;

-- 重置学习进度表的自增ID
ALTER TABLE user_learning_paths AUTO_INCREMENT = 1;
SELECT '已重置学习进度表自增ID' AS status;

-- 重置在线答疑表的自增ID
ALTER TABLE qa_sessions AUTO_INCREMENT = 1;
SELECT '已重置在线答疑表自增ID' AS status;

-- 重置用户购买记录表的自增ID
ALTER TABLE user_purchases AUTO_INCREMENT = 1;
SELECT '已重置用户购买记录表自增ID' AS status;

-- 重置支付订单表的自增ID
ALTER TABLE payment_orders AUTO_INCREMENT = 1;
SELECT '已重置支付订单表自增ID' AS status;

-- 重置退款记录表的自增ID
ALTER TABLE refund_records AUTO_INCREMENT = 1;
SELECT '已重置退款记录表自增ID' AS status;

-- 重置用户优惠券表的自增ID
ALTER TABLE user_coupons AUTO_INCREMENT = 1;
SELECT '已重置用户优惠券表自增ID' AS status;

-- 重置消息通知表的自增ID
ALTER TABLE notifications AUTO_INCREMENT = 1;
SELECT '已重置消息通知表自增ID' AS status;

-- 重置操作日志表的自增ID
ALTER TABLE operation_logs AUTO_INCREMENT = 1;
SELECT '已重置操作日志表自增ID' AS status;

-- 重置系统日志表的自增ID
ALTER TABLE system_logs AUTO_INCREMENT = 1;
SELECT '已重置系统日志表自增ID' AS status;

-- =============================================
-- 8. 恢复安全设置
-- =============================================

SET FOREIGN_KEY_CHECKS = 1;
SET SQL_SAFE_UPDATES = 1;

-- =============================================
-- 9. 显示清理结果统计
-- =============================================

SELECT 
    '数据清理完成' AS status,
    NOW() AS cleanup_time,
    '以下表的数据已被清空：' AS description,
    'exam_records, wrong_answers, exam_monitoring,' AS tables_cleared,
    'user_favorites, user_learning_paths, qa_sessions,' AS more_tables,
    'user_purchases, payment_orders, refund_records,' AS payment_tables,
    'user_coupons, notifications, operation_logs, system_logs' AS log_tables;

-- =============================================
-- 注意事项：
-- 1. 此脚本会删除所有用户的考试相关数据
-- 2. 保留的数据：用户账户、科目、题目、考试模板、系统配置等
-- 3. 执行前请务必备份数据库
-- 4. 建议在测试环境中先验证脚本的正确性
-- 5. 生产环境执行前请谨慎确认
-- =============================================
