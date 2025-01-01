# app/dao/advisor_dao.py
from app.utils.db_utils import DBConnection

# 获取导师信息
def get_advisor_info(advisor_id):
    """
    获取导师信息和剩余名额（仅剩余名额大于 0 的导师）
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT advisor_id, name, department, annual_quota - assigned_quota AS remaining_quota
        FROM dbo.advisor
        WHERE advisor_id = ? AND annual_quota > assigned_quota
        """
        cursor.execute(query, (advisor_id,))
        advisor = cursor.fetchone()

        if advisor:
            return {
                "advisor_id": advisor[0],
                "advisor_name": advisor[1],
                "department": advisor[2],
                "remaining_quota": advisor[3]
            }
        return None

    except Exception as e:
        print(f"Error fetching advisor info: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

#自由匹配
# 查看符合条件的导师
def get_available_advisors(department):
    """
    获取符合条件的导师列表，并按优先级排序
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT advisor_id, name, annual_quota - assigned_quota AS remaining_quota
        FROM dbo.advisor
        WHERE department = ?
          AND annual_quota > assigned_quota
        ORDER BY assigned_quota ASC, remaining_quota DESC
        """
        cursor.execute(query, (department,))
        available_advisors = cursor.fetchall()

        return [{"advisor_id": row[0], "advisor_name": row[1], "remaining_quota": row[2]} for row in available_advisors]

    except Exception as e:
        print(f"Error fetching available advisors: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
