-- ������ʦ��
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

-- ����һ��ѧ�Ʊ�
CREATE TABLE firsubject (
    firsubject_id INT PRIMARY KEY,
    name VARCHAR(255),
    overview TEXT,
    level INT
);

-- ��������ѧ�Ʊ�
CREATE TABLE secsubject (
    secsubject_id INT PRIMARY KEY,
    name VARCHAR(255),
    firsubject_id INT,
    overview TEXT,
    level INT,
    FOREIGN KEY (firsubject_id) REFERENCES firsubject(firsubject_id)
);

-- ��������Ŀ¼��
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

-- ������ʦ�����ѧ�ƵĹ�����
CREATE TABLE advisor_secsubject (
    advisor_id VARCHAR(255),
    secsubject_id INT,
    PRIMARY KEY (advisor_id, secsubject_id),
    FOREIGN KEY (advisor_id) REFERENCES advisor(advisor_id),
    FOREIGN KEY (secsubject_id) REFERENCES secsubject(secsubject_id)
);

-- ����һ��ѧ���뿼�Կ�Ŀ�Ĺ�����
CREATE TABLE firsubject_test (
    firsno INT PRIMARY KEY,
    firsubject_id INT,
    firtest_id INT,
    FOREIGN KEY (firsubject_id) REFERENCES firsubject(firsubject_id)
    -- ע�⣺�˴��������һ�����Կ�Ŀ�����а��� firtest_id ��Ϊ������Ψһ��ʶ
);
