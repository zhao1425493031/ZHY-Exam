-- 添加合格分数字段到考试表
ALTER TABLE exams 
ADD COLUMN passing_score INT COMMENT '合格分数' AFTER total_points;

-- 更新现有数据：如果有settings里的passing_score，迁移到新字段
UPDATE exams 
SET passing_score = JSON_UNQUOTE(JSON_EXTRACT(settings, '$.passing_score'))
WHERE JSON_EXTRACT(settings, '$.passing_score') IS NOT NULL;

-- 更新NULL值为默认60%
UPDATE exams 
SET passing_score = FLOOR(total_points * 0.6)
WHERE passing_score IS NULL;

