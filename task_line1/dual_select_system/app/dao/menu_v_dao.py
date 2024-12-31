from app.utils.db_utils import DBConnection

def get_all_menu_v():
    """
    获取所有menu_v视图的内容

    该函数通过执行一个SQL查询操作，从数据库中获取所有menu_v视图的内容。

    返回值:
        list: 包含所有menu_v视图记录的列表，如果没有记录则返回空列表。
    """
    query = """
    SELECT * FROM menu_v
    """
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"获取所有menu_v视图内容失败: {e}")
        return []
    finally:
        connection.close()

def update_advisor(year):
    """
    更新导师的资格状态

    该函数首先将advisor表中所有is_eligible字段设置为否，然后根据menu表中与给定年份且is_eligible为真的行，
    更新advisor表中相应行的is_eligible字段。

    参数:
        year (int): 要更新的年份。

    返回值:
        None
    """
    # 首先将advisor表中所有is_eligible字段设置为否
    set_all_ineligible_query = """
    UPDATE advisor
    SET is_eligible = 0
    """
    
    # 然后根据menu表更新advisor表中相应行的is_eligible字段
    update_query = """
    UPDATE advisor
    SET is_eligible = 1
    WHERE advisor_id IN (
        SELECT advisor_id FROM menu
        WHERE year = ? AND is_eligible = 1
    )
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return

    try:
        with connection.cursor() as cursor:
            # 执行将所有is_eligible设置为否的查询
            cursor.execute(set_all_ineligible_query)
            # 执行更新特定advisor_id的is_eligible为真的查询
            cursor.execute(update_query, (year,))
            connection.commit()
    except Exception as e:
        print(f"更新导师资格状态失败: {e}")
        connection.rollback()
    finally:
        connection.close()
