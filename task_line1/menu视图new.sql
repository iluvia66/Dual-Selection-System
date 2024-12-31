--����menu��
CREATE TABLE menu (
    mno INT,
    year INT,
    advisor_id VARCHAR(255),
    is_eligible BIT
);

GO
--д������
BULK INSERT menu
FROM 'C:\Users\86199\Desktop\�ɵ���\menu.csv'
WITH (
    FIELDTERMINATOR = ',',   -- �ֶηָ���Ϊ����
    ROWTERMINATOR = '\n',    -- �зָ���Ϊ���з�
    FIRSTROW = 2,            -- ����������
    CODEPAGE = '65001'       -- ʹ�� UTF-8 ����
);


GO
--�����̶����ݱ�
CREATE TABLE eveyeardata (
    year INT PRIMARY KEY,
	totalquota INT,
    exquota VARCHAR(255),
    placecode VARCHAR(50),
    place VARCHAR(255),
    location VARCHAR(255),
    phone VARCHAR(50),
    context VARCHAR(255)
);

GO

INSERT INTO eveyeardata (year, placecode, place, location, phone, context) 
VALUES (2022, '10022', '������ҵ��ѧ', '�����������廪��· 35 ��/100083', '010-62338214/62338380', '����ʦ/����ʦ');

GO

--������ͼ
CREATE VIEW menu_v AS
SELECT
    m.mno,
    m.year,
    ey.exquota,
    ey.totalquota,
    d.department_id,
    d.name AS department,
    fs.name AS firsubject,
    ss.name AS secsubject,
	fs.overview AS title,
    a.name AS advisor,
    ey.placecode,
    ey.place,
    ey.location,
    ey.phone,
    ey.context

FROM
    menu m
	LEFT JOIN eveyeardata ey ON m.year = ey.year
	LEFT JOIN advisor a ON m.advisor_id = a.advisor_id
	LEFT JOIN advisor_secsubject ass ON a.advisor_id=ass.advisor_id
	LEFT JOIN secsubject ss ON ass.secsubject_id=ss.secsubject_id
	LEFT JOIN firsubject fs ON ss.firsubject_id = fs.firsubject_id
    LEFT JOIN department d ON fs.department_id = d.department_id
    LEFT JOIN firsubject_test fst ON fs.firsubject_id = fst.firsubject_id
    LEFT JOIN firtest ft ON fst.firtest_id = ft.firtest_id;  