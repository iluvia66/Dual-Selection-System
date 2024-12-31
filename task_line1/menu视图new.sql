--创建menu表
CREATE TABLE menu (
    mno INT,
    year INT,
    advisor_id VARCHAR(255),
    is_eligible BIT
);

GO
--写入数据
BULK INSERT menu
FROM 'C:\Users\86199\Desktop\可导入\menu.csv'
WITH (
    FIELDTERMINATOR = ',',   -- 字段分隔符为逗号
    ROWTERMINATOR = '\n',    -- 行分隔符为换行符
    FIRSTROW = 2,            -- 跳过标题行
    CODEPAGE = '65001'       -- 使用 UTF-8 编码
);


GO
--创建固定数据表
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
VALUES (2022, '10022', '北京林业大学', '北京海淀区清华东路 35 号/100083', '010-62338214/62338380', '周老师/李老师');

GO

--创建视图
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