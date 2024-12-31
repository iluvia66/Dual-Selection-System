--����firsubject��
alter table firsubject nocheck constraint all;
alter table department nocheck constraint all;
alter table secsubject nocheck constraint all;
alter table firsubject_test nocheck constraint all;
GO
delete from firsubject;

GO
BULK INSERT firsubject
FROM 'C:\Users\86199\Desktop\�ɵ���\firsubject_new.csv'
WITH (
    FIELDTERMINATOR = ',',  -- �ֶ���ֹ��
    ROWTERMINATOR = '\n',   -- ����ֹ��
    FIRSTROW = 2            -- �����һ���Ǳ����У���ӵڶ��п�ʼ����
);

GO
alter table firsubject check constraint all;
alter table department check constraint all;
alter table secsubject check constraint all;
alter table firsubject_test check constraint all;

--����secsubject��
alter table firsubject nocheck constraint all;
alter table advisor_secsubject nocheck constraint all;
alter table secsubject nocheck constraint all;
GO
delete from secsubject;

GO
BULK INSERT secsubject
FROM 'C:\Users\86199\Desktop\�ɵ���\secsubject_new1.csv'
WITH (
    FIELDTERMINATOR = ',',  -- �ֶ���ֹ��
    ROWTERMINATOR = '\n',   -- ����ֹ��
    FIRSTROW = 2            -- �����һ���Ǳ����У���ӵڶ��п�ʼ����
);

GO
alter table firsubject check constraint all;
alter table advisor_secsubject check constraint all;
alter table secsubject check constraint all;


--����firsubject_test
alter table firsubject nocheck constraint all;
alter table firtest nocheck constraint all;
GO
delete from firsubject_test;

GO
BULK INSERT firsubject_test
FROM 'C:\Users\86199\Desktop\�ɵ���\firsubject_test_new.csv'
WITH (
    FIELDTERMINATOR = ',',  -- �ֶ���ֹ��
    ROWTERMINATOR = '\n',   -- ����ֹ��
    FIRSTROW = 2            -- �����һ���Ǳ����У���ӵڶ��п�ʼ����
);

GO
alter table firsubject check constraint all;
alter table firtest check constraint all;

--����advisor_secsubject
alter table secsubject nocheck constraint all;
alter table advisor nocheck constraint all;
GO
delete from advisor_secsubject;

GO
BULK INSERT advisor_secsubject
FROM 'C:\Users\86199\Desktop\�ɵ���\advisor_secsubject_new2.csv'
WITH (
    FIELDTERMINATOR = ',',  -- �ֶ���ֹ��
    ROWTERMINATOR = '\n',   -- ����ֹ��
    FIRSTROW = 2            -- �����һ���Ǳ����У���ӵڶ��п�ʼ����
);

GO
alter table secsubject check constraint all;
alter table advisor check constraint all;