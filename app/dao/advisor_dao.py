# app/dao/advisor_dao.py
from app.utils.db_utils import DBConnection

def get_students_by_advisor_id(advisor_id):
    """
    根据导师ID获取学生信息

    该函数通过执行一个SQL查询，从数据库中获取指定导师的学生信息。

    参数:
        advisor_id (int): 导师的ID。

    返回值:
        list: 包含学生信息的列表，每个学生信息是一个字典。
    """
    # SQL查询语句，用于从View_Advisor_Student_Preferences视图中获取指定导师的学生信息
    query = """
    SELECT * FROM View_Advisor_Student_Preferences
    WHERE advisor_id =?
    """
    
    # 获取数据库连接
    connection = DBConnection.get_connection()
    
    # 创建游标对象
    cursor = connection.cursor()
    
    # 执行SQL查询，获取学生信息
    cursor.execute(query, (advisor_id,))
    
    # 获取查询结果
    students = cursor.fetchall()
    
    # 关闭游标
    cursor.close()
    
    # 关闭数据库连接
    connection.close()
    
    # 返回学生信息
    return students
