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

-- 创建一级学科表
CREATE TABLE firsubject (
    firsubject_id INT PRIMARY KEY,
    name VARCHAR(255),
    overview TEXT,
    level INT
);

-- 创建二级学科表
CREATE TABLE secsubject (
    secsubject_id INT PRIMARY KEY,
    name VARCHAR(255),
    firsubject_id INT,
    overview TEXT,
    level INT,
    FOREIGN KEY (firsubject_id) REFERENCES firsubject(firsubject_id)
);

-- 创建招生目录表
CREATE TABLE menu (
    mno INT PRIMARY KEY,
    year INT,
    advisor_id VARCHAR(255),
    exquota INT,
    totalquota INT,
    placecode INT,
    place VARCHAR(255),
    location VARCHAR(255),
    phone VARCHAR(255),
    context VARCHAR(255),
    FOREIGN KEY (advisor_id) REFERENCES advisor(advisor_id)
);

-- 创建导师与二级学科的关联表
CREATE TABLE advisor_secsubject (
    advisor_id VARCHAR(255),
    secsubject_id INT,
    PRIMARY KEY (advisor_id, secsubject_id),
    FOREIGN KEY (advisor_id) REFERENCES advisor(advisor_id),
    FOREIGN KEY (secsubject_id) REFERENCES secsubject(secsubject_id)
);

-- 创建一级学科与考试科目的关联表
CREATE TABLE firsubject_test (
    firsno INT PRIMARY KEY,
    firsubject_id INT,
    firtest_id INT,
    FOREIGN KEY (firsubject_id) REFERENCES firsubject(firsubject_id)
    -- 注意：此处假设存在一个考试科目表，其中包含 firtest_id 作为主键或唯一标识
);
