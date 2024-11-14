USE dual_selection_system;
GO

-- ���� Candidate ��
IF OBJECT_ID('Candidate', 'U') IS NULL
BEGIN
    CREATE TABLE Candidate (
        candidate_id INT PRIMARY KEY IDENTITY(1,1), -- ʹ�� IDENTITY ʵ���Զ�����
        name VARCHAR(255) NOT NULL,                 -- ����������������Ϊ��
        gender VARCHAR(10),                         -- �Ա�
        birthdate DATE,                             -- ��������
        id_number VARCHAR(20),                      -- ���֤����
        email VARCHAR(255),                         -- ��������
        phone VARCHAR(20),                          -- ��ϵ�绰
        nationality VARCHAR(50),                    -- ��Դ��
        exam_id VARCHAR(20),                        -- ׼��֤��
        degree VARCHAR(50),                         -- ����ѧ��
        undergrad_major VARCHAR(100),               -- ����רҵ
        undergrad_school VARCHAR(100),              -- ���Ʊ�ҵѧУ
        undergrad_type VARCHAR(50),                 -- ����ѧУ����
        applying_major VARCHAR(100)                 -- ����רҵ
    );
END;

-- ���� PreliminaryExam ������ subject_id ָ��һ��ѧ�Ʊ� (firsubject) �� firsubject_id
CREATE TABLE PreliminaryExam (
    firstest_id INT PRIMARY KEY,                -- ������Ψһ��ʶÿ�����Լ�¼
    candidate_id INT,                           -- �����ָ�������е� candidate_id
    subject_id INT,                             -- ָ��һ��ѧ�Ʊ� (firsubject) �е� firsubject_id
    exam_date DATE,                             -- ����ʱ��
    subject_score FLOAT,                        -- �����ڸó��Կ�Ŀ�ϵĳɼ�
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id),
    FOREIGN KEY (subject_id) REFERENCES firsubject(firsubject_id) -- �� subject_id ������ firsubject ��� firsubject_id
);

-- ���� RetakeExam ��
CREATE TABLE RetakeExam (
    sectest_id INT PRIMARY KEY,                    -- ������Ψһ��ʶÿ�����Լ�¼
    candidate_id INT,                              -- �����ָ�������е� candidate_id
    retake_subject VARCHAR(50),                    -- ����ѧ��רҵ
    exam_ticket_number VARCHAR(20),                -- ����׼��֤��
    name VARCHAR(50),                              -- ��������
    gender CHAR(1),                                -- �Ա�
    candidate_type VARCHAR(20),                    -- �������
    undergraduate_school VARCHAR(100),             -- ���Ʊ�ҵѧУ
    graduation_date DATE,                          -- ���Ʊ�ҵʱ��
    undergraduate_major VARCHAR(50),               -- ���Ʊ�ҵרҵ
    contact_phone VARCHAR(15),                     -- �����ֻ�����
    emergency_contact_phone VARCHAR(15),           -- ������ϵ���ֻ�����
    preferred_supervisor VARCHAR(100),             -- ������ʦ��������
    intended_research_direction VARCHAR(100),      -- �ⱨ�о�����
    accept_direction_adjustment BIT,               -- �Ƿ���ܷ������ (1��ʾ���ܣ�0��ʾ������)
    direction_adjustment_priority VARCHAR(100),    -- �������������˳��
    retake_date DATE,                              -- ����ʱ��
    retake_location VARCHAR(100),                  -- ���Եص�
    retake_evaluation TEXT,                        -- ����С��Կ������ۺ�����
    listening_speaking_score FLOAT,                -- ������������������
    professional_knowledge_score FLOAT,            -- רҵ֪ʶ���Գɼ�
    comprehensive_ability_score FLOAT,             -- �ۺ��������Գɼ�
    total_score FLOAT,                             -- �����ܳɼ�
    retake_team_leader_signature VARCHAR(50),      -- �����鳤ǩ��
    retake_team_member_signatures TEXT,            -- �������Աǩ��
    proposed_supervisor_signature VARCHAR(50),     -- ��¼ȡ��ʦǩ��
    FOREIGN KEY (candidate_id) REFERENCES Candidate(candidate_id)
);
