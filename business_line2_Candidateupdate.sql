USE dual_selection_system;  -- 切换到目标数据库
GO

ALTER TABLE Candidate
ADD Exam_type VARCHAR(20);  -- 添加 Exam_type 列，设置为 NVARCHAR 类型，最大长度为20字符，可根据需求调整
