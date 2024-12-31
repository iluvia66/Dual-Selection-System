--导入firsubject表
alter table firsubject nocheck constraint all;
alter table department nocheck constraint all;
alter table secsubject nocheck constraint all;
alter table firsubject_test nocheck constraint all;
GO
delete from firsubject;

GO
BULK INSERT firsubject
FROM 'C:\Users\86199\Desktop\可导入\firsubject_new.csv'
WITH (
    FIELDTERMINATOR = ',',  -- 字段终止符
    ROWTERMINATOR = '\n',   -- 行终止符
    FIRSTROW = 2            -- 如果第一行是标题行，则从第二行开始导入
);

GO
alter table firsubject check constraint all;
alter table department check constraint all;
alter table secsubject check constraint all;
alter table firsubject_test check constraint all;

--导入secsubject表
alter table firsubject nocheck constraint all;
alter table advisor_secsubject nocheck constraint all;
alter table secsubject nocheck constraint all;
GO
delete from secsubject;

GO
BULK INSERT secsubject
FROM 'C:\Users\86199\Desktop\可导入\secsubject_new1.csv'
WITH (
    FIELDTERMINATOR = ',',  -- 字段终止符
    ROWTERMINATOR = '\n',   -- 行终止符
    FIRSTROW = 2            -- 如果第一行是标题行，则从第二行开始导入
);

GO
alter table firsubject check constraint all;
alter table advisor_secsubject check constraint all;
alter table secsubject check constraint all;


--导入firsubject_test
alter table firsubject nocheck constraint all;
alter table firtest nocheck constraint all;
GO
delete from firsubject_test;

GO
BULK INSERT firsubject_test
FROM 'C:\Users\86199\Desktop\可导入\firsubject_test_new.csv'
WITH (
    FIELDTERMINATOR = ',',  -- 字段终止符
    ROWTERMINATOR = '\n',   -- 行终止符
    FIRSTROW = 2            -- 如果第一行是标题行，则从第二行开始导入
);

GO
alter table firsubject check constraint all;
alter table firtest check constraint all;

--导入advisor_secsubject
alter table secsubject nocheck constraint all;
alter table advisor nocheck constraint all;
GO
delete from advisor_secsubject;

GO
BULK INSERT advisor_secsubject
FROM 'C:\Users\86199\Desktop\可导入\advisor_secsubject_new2.csv'
WITH (
    FIELDTERMINATOR = ',',  -- 字段终止符
    ROWTERMINATOR = '\n',   -- 行终止符
    FIRSTROW = 2            -- 如果第一行是标题行，则从第二行开始导入
);

GO
alter table secsubject check constraint all;
alter table advisor check constraint all;