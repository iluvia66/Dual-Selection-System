-- 创建导师表
CREATE TABLE advisor (
    advisor_id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255),
    title VARCHAR(255),
    photo_URL VARCHAR(MAX),
    biography TEXT,
    email VARCHAR(255),
    phone VARCHAR(255),
    department VARCHAR(255),
    annual_quota INT,
    assigned_quota INT,
    is_eligible BIT
);



-- 创建志愿匹配表
IF OBJECT_ID('Preference_Match', 'U') IS NULL
BEGIN
    CREATE TABLE Preference_Match (
        match_id INT PRIMARY KEY IDENTITY(1,1),      -- 使用 IDENTITY 实现自动递增
        candidate_id INT NOT NULL,                   -- 外键，指向 Candidate 表中的 candidate_id
        advisor_id VARCHAR(255) NOT NULL,            -- 外键，指向 advisor 表中的 advisor_id
        preference_order INT NOT NULL,               -- 志愿顺序（1 表示第一志愿，2 表示第二志愿，3 表示第三志愿）
        status VARCHAR(20) DEFAULT '待确认',           -- 志愿状态，默认为“待确认”
        match_type VARCHAR(20) DEFAULT '志愿匹配',    -- 匹配类型，默认为“志愿匹配”
        match_date DATETIME,                         -- 匹配确认的日期

        -- 外键约束
        CONSTRAINT fk_candidate FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id),
        CONSTRAINT fk_advisor FOREIGN KEY (advisor_id) REFERENCES advisor(advisor_id)
    );
END;


-- 创建导师二级学科关系表
CREATE TABLE advisor_secsubject (
    advisor_secsubject_id INT PRIMARY KEY IDENTITY(1,1),  -- 主键，自增的表ID
    advisor_id VARCHAR(255),                               -- 外键，导师ID
    secsubject_id VARCHAR(255),                                     -- 外键，二级学科ID
    FOREIGN KEY (advisor_id) REFERENCES advisor(advisor_id), -- 关联导师表
    FOREIGN KEY (secsubject_id) REFERENCES secsubject(secsubject_id) -- 关联二级学科表
);