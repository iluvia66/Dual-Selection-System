# app/dao/advisor_dao.py
from app.utils.db_utils import DBConnection

def get_advisor_by_id(advisor_id):
    """
    根据导师ID获取导师信息

    该函数通过执行一个SQL查询，从数据库中获取指定ID的导师信息。

    参数:
        advisor_id (int): 导师的ID。

    返回值:
        dict: 包含导师信息的字典，如果没有找到则返回None。
    """
    query = """
    SELECT * FROM advisor
    WHERE advisor_id = ?
    """

    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (advisor_id,))
            result = cursor.fetchone()
            #print(result)
            return result if result else None
    except Exception as e:
        print(f"查询失败: {e}")
        return None
    finally:
        connection.close()

def get_all_advisors():
    """
    获取所有导师的信息

    该函数通过执行一个SQL查询，从数据库中获取所有导师的信息。

    返回值:
        list: 包含所有导师信息的列表，如果没有导师则返回空列表。
    """
    query = """
    SELECT * FROM advisor
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results if results else []
    except Exception as e:
        print(f"所有导师的信息查询失败: {e}")
        return []
    finally:
        connection.close()

def update_advisor(advisor_id, name, title, photo_URL, biography, email, phone, department, annual_quota, assigned_quota):
    """
    更新导师信息

    该函数通过执行一个SQL更新操作，更新指定导师的所有信息。

    参数:
        advisor_id (str): 导师的ID。
        name (str): 导师的名字。
        title (str): 导师的职称。
        photo_URL (str): 导师照片的URL。
        biography (str): 导师的传记。
        email (str): 导师的电子邮件。
        phone (str): 导师的电话号码。
        department (str): 导师所在的部门。
        annual_quota (int): 导师的年度配额。
        assigned_quota (int): 已分配的配额。

    返回值:
        bool: 更新操作是否成功。
    """
    query = """
    UPDATE advisor
    SET name = ?, title = ?, photo_URL = ?, biography = ?, email = ?, phone = ?, department = ?, annual_quota = ?, assigned_quota = ?
    WHERE advisor_id = ?
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (name, title, photo_URL, biography, email, phone, department, annual_quota, assigned_quota, advisor_id))
            connection.commit()
            return True
    except Exception as e:
        print(f"更新导师信息失败: {e}")
        return False
    finally:
        connection.close()

def update_advisor_title(advisor_id, new_title):
    """
    更新导师职称

    该函数通过执行一个SQL更新操作，更新指定导师的职称。

    参数:
        advisor_id (varchar): 导师的ID。
        new_title (str): 导师的新职称。

    返回值:
        bool: 更新操作是否成功。
    """
    query = """
    UPDATE advisor
    SET title = ?
    WHERE advisor_id = ?
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (new_title, advisor_id))
            connection.commit()
            #print("执行更新函数")
            return True
    except Exception as e:
        print(f"更新职称数据失败: {e}")
        return False
    finally:
        connection.close()

def update_annual_quota(advisor_id, new_annual_quota ,new_assigned_quota):
    """
    确认导师年度招生指标

    该函数通过执行一个SQL更新操作，更新指定导师的年度招生指标。

    参数:
        advisor_id (varchar): 导师的ID。
        new_annual_quota (int): 导师的新年度招生指标。

    返回值:
        bool: 更新操作是否成功。
    """
    query = """
    UPDATE advisor
    SET annual_quota = ?, assigned_quota = ?
    WHERE advisor_id = ?
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (new_annual_quota, new_assigned_quota ,advisor_id))
            connection.commit()
            return True
    except Exception as e:
        print(f"更新年度配额失败: {e}")
        return False
    finally:
        connection.close()

def get_assigned_quota(advisor_id):
    """
    获取导师剩余指标

    该函数通过执行一个SQL查询，从数据库中获取指定导师的已分配招生指标。

    参数:
        advisor_id (varchar): 导师的ID。

    返回值:
        int: 导师的已分配招生指标，如果没有找到则返回None。
    """
    query = """
    SELECT assigned_quota FROM advisor
    WHERE advisor_id = %s
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return None

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (advisor_id,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"查询已分配配额失败: {e}")
        return None
    finally:
        connection.close()
