USE dual_selection_system;
GO

-- 创建 Candidate 表
IF OBJECT_ID('Candidate', 'U') IS NULL
BEGIN
    CREATE TABLE Candidate (
        candidate_id INT PRIMARY KEY IDENTITY(1,1), -- 使用 IDENTITY 实现自动递增
        name VARCHAR(255) NOT NULL,                 -- 考生姓名，不允许为空
        gender VARCHAR(10),                         -- 性别
        birthdate DATE,                             -- 出生日期
        id_number VARCHAR(20),                      -- 身份证号码
        email VARCHAR(255),                         -- 考生邮箱
        phone VARCHAR(20),                          -- 联系电话
        nationality VARCHAR(50),                    -- 生源地
        exam_id VARCHAR(20),                        -- 准考证号
        degree VARCHAR(50),                         -- 本科学历
        undergrad_major VARCHAR(100),               -- 本科专业
        undergrad_school VARCHAR(100),              -- 本科毕业学校
        undergrad_type VARCHAR(50),                 -- 本科学校类型
        applying_major VARCHAR(100)                 -- 报考专业
    );
END;

-- 创建 PreliminaryExam 表，并将 subject_id 指向一级学科表 (firsubject) 的 firsubject_id
CREATE TABLE PreliminaryExam (
    firstest_id INT PRIMARY KEY,                -- 主键，唯一标识每条初试记录
    candidate_id INT,                           -- 外键，指向考生表中的 candidate_id
    subject_id INT,                             -- 指向一级学科表 (firsubject) 中的 firsubject_id
    exam_date DATE,                             -- 考试时间
    subject_score FLOAT,                        -- 考生在该初试科目上的成绩
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id),
    FOREIGN KEY (subject_id) REFERENCES firsubject(firsubject_id) -- 将 subject_id 关联到 firsubject 表的 firsubject_id
);

-- 创建 RetakeExam 表
CREATE TABLE RetakeExam (
    sectest_id INT PRIMARY KEY,                    -- 主键，唯一标识每条复试记录
    candidate_id INT,                              -- 外键，指向考生表中的 candidate_id
    retake_subject VARCHAR(50),                    -- 复试学科专业
    exam_ticket_number VARCHAR(20),                -- 考生准考证号
    name VARCHAR(50),                              -- 考生姓名
    gender CHAR(1),                                -- 性别
    candidate_type VARCHAR(20),                    -- 考生类别
    undergraduate_school VARCHAR(100),             -- 本科毕业学校
    graduation_date DATE,                          -- 本科毕业时间
    undergraduate_major VARCHAR(50),               -- 本科毕业专业
    contact_phone VARCHAR(15),                     -- 考生手机号码
    emergency_contact_phone VARCHAR(15),           -- 紧急联系人手机号码
    preferred_supervisor VARCHAR(100),             -- 报考导师优先意向
    intended_research_direction VARCHAR(100),      -- 拟报研究方向
    accept_direction_adjustment BIT,               -- 是否接受方向调整 (1表示接受，0表示不接受)
    direction_adjustment_priority VARCHAR(100),    -- 方向调整的优先顺序
    retake_date DATE,                              -- 复试时间
    retake_location VARCHAR(100),                  -- 复试地点
    retake_evaluation TEXT,                        -- 复试小组对考生的综合评价
    listening_speaking_score FLOAT,                -- 外语听力及口语评分
    professional_knowledge_score FLOAT,            -- 专业知识测试成绩
    comprehensive_ability_score FLOAT,             -- 综合素质面试成绩
    total_score FLOAT,                             -- 复试总成绩
    retake_team_leader_signature VARCHAR(50),      -- 复试组长签字
    retake_team_member_signatures TEXT,            -- 复试组成员签字
    proposed_supervisor_signature VARCHAR(50),     -- 拟录取导师签字
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id)
);
