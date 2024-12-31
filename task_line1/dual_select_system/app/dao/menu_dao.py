from app.utils.db_utils import DBConnection

def get_all_menus():
    """
    获取所有menu表的内容

    该函数通过执行一个SQL查询操作，从数据库中获取所有menu表的内容。

    返回值:
        list: 包含所有menu表记录的列表，如果没有记录则返回空列表。
    """
    query = """
    SELECT * FROM menu
    """
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            #print(results)
            return results
    except Exception as e:
        print(f"获取所有menu表内容失败: {e}")
        return []
    finally:
        connection.close()

def update_is_eligible(advisor_id, is_eligible):
    """
    更新生源资格

    该函数通过执行一个SQL更新操作，更新数据库中导师的招生资格。

    参数:
        advisor_id (int): 导师ID。
        is_eligible (int): 是否有招生资格。

    返回值:
        bool: 更新操作成功返回True，失败返回False。
    """
    query = """
    UPDATE menu
    SET is_eligible = ?
    WHERE advisor_id = ?
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    is_eligible_bool = bool(is_eligible)

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (is_eligible_bool, advisor_id))
            connection.commit()
            return True
    except Exception as e:
        print(f"更新is_eligible字段失败: {e}")
        return False
    finally:
        connection.close()

def insert_new_menu(year, advisor_id, is_eligible):
    """
    为menu表插入一条新纪录

    该函数通过执行一个SQL插入操作，向数据库中插入一条新纪录。
    新纪录的mno值为当前记录条数加一。

    参数:
        year (int): 年份。
        advisor_id (str): 导师ID。
        is_eligible (bool): 是否有招生资格。

    返回值:
        bool: 插入操作成功返回True，失败返回False。
    """
    query_get_max_mno = """
    SELECT MAX(mno) FROM menu
    """
    query_insert = """
    INSERT INTO menu (mno, year, advisor_id, is_eligible)
    VALUES (?, ?, ?, ?)
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query_get_max_mno)
            max_mno = cursor.fetchone()[0]
            new_mno = 1 if max_mno is None else max_mno + 1
            cursor.execute(query_insert, (new_mno, year, advisor_id, is_eligible))
            connection.commit()
            return True
    except Exception as e:
        print(f"插入新menu记录失败: {e}")
        return False
    finally:
        connection.close()

def update_menu_record(mno, year, advisor_id, is_eligible):
    """
    修改menu表中的一条记录内容

    该函数通过执行一个SQL更新操作，更新数据库中指定mno值的记录内容。
    mno值不能被修改。

    参数:
        mno (int): 编号。
        year (int): 年份。
        advisor_id (str): 导师ID。
        is_eligible (bool): 是否有招生资格。

    返回值:
        bool: 更新操作成功返回True，失败返回False。
    """
    query = """
    UPDATE menu
    SET year = ?, advisor_id = ?, is_eligible = ?
    WHERE mno = ?
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (year, advisor_id, is_eligible, mno))
            connection.commit()
            return True
    except Exception as e:
        print(f"更新menu记录失败: {e}")
        return False
    finally:
        connection.close()

def delete_menu_record(mno):
    """
    删除一条menu记录

    该函数通过执行一个SQL删除操作，从数据库中删除指定mno值的记录。
    删除后，所有大于该mno值的记录的mno值减一。

    参数:
        mno (int): 编号。

    返回值:
        bool: 删除操作成功返回True，失败返回False。
    """
    query_delete = """
    DELETE FROM menu WHERE mno = ?
    """
    query_update = """
    UPDATE menu SET mno = mno - 1 WHERE mno > ?
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query_delete, (mno,))
            cursor.execute(query_update, (mno,))
            connection.commit()
            return True
    except Exception as e:
        print(f"删除menu记录失败: {e}")
        return False
    finally:
        connection.close()
