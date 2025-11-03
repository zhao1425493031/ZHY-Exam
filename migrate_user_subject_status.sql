-- 用户课程关联表状态字段迁移
-- 添加新的状态：pending（待承认）、approved（已承认）、rejected（拒绝）

ALTER TABLE `user_subjects` 
MODIFY COLUMN `status` ENUM('active', 'expired', 'cancelled', 'pending', 'approved', 'rejected') DEFAULT 'pending' 
COMMENT '订阅状态：active-正常，expired-已过期，cancelled-已取消，pending-待承认，approved-已承认，rejected-拒绝';

-- 将现有的active状态保持为active，其他状态保持不变

