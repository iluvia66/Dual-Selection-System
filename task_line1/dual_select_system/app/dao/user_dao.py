from app.utils.db_utils import DBConnection

def get_user_by_id(userid):
    """
    根据用户ID查询用户信息
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        query = "SELECT UserID, Password, UserRole FROM [User] WHERE UserID = ?"
        cursor.execute(query, (userid,))
        row = cursor.fetchone()
        connection.close()
        if row:
            return {"userid": row[0], "password": row[1], "role": row[2]}
        return None
    except Exception as e:
        print(f"Error querying user by ID: {e}")
        return None


def insert_user(userid, password, role):
    """
    插入新用户
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO [User] (UserID, Password, UserRole) VALUES (?, ?, ?)"
        cursor.execute(query, (userid, password, role))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error inserting user: {e}")
        return False