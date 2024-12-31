from app.utils.db_utils import DBConnection

def get_all_everyeardata():
    """
    查找表中所有值

    该函数通过执行一个SQL查询操作，从数据库中检索所有年度数据记录。

    参数:
        无

    返回值:
        list: 如果查询成功，返回包含所有记录的列表；如果失败，返回空列表。
    """
    query = """
    SELECT * FROM eveyeardata
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return []

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
            return records
    except Exception as e:
        print(f"查询所有记录失败: {e}")
        return []
    finally:
        connection.close()

def update_everyeardata(year, placecode, place, location, phone, context, totalquota, exquota):
    """
    更改表中特定年份的记录

    该函数通过执行一个SQL更新操作，更改数据库中特定年份的记录。

    参数:
        year (int): 年份，用作索引。
        placecode (str): 地点代码。
        place (str): 地点。
        location (str): 位置。
        phone (str): 电话。
        context (str): 上下文或描述。
        totalquota (int): 总指标。
        exquota (str): 额外指标。

    返回值:
        bool: 更新操作成功返回True，失败返回False。
    """
    if year is None:
        print("Year value cannot be null.")
        return False

    query = """
    UPDATE eveyeardata
    SET placecode = ?, place = ?, location = ?, phone = ?, context = ?, totalquota = ?, exquota = ?
    WHERE year = ?
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (placecode, place, location, phone, context, totalquota, exquota, year))
            connection.commit()
            return True
    except Exception as e:
        print(f"更新记录失败: {e}")
        return False
    finally:
        connection.close()

def year_exists_everyeardata(year):
    """
    检查表中是否存在指定的年份

    该函数通过执行一个SQL查询操作，检查数据库中是否存在指定的年份。

    参数:
        year (int): 要检查的年份。

    返回值:
        bool: 如果年份存在返回True，否则返回False。
    """
    query = "IF EXISTS(SELECT 1 FROM eveyeardata WHERE year = ?) SELECT 1 ELSE SELECT 0"
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (year,))
            result = cursor.fetchone()
            return result[0]  # EXISTS函数返回的结果是布尔值，直接返回即可
    except Exception as e:
        print(f"检查年份是否存在时发生错误: {e}")
        return False
    finally:
        connection.close()


def insert_everyeardata(year, placecode, place, location, phone, context, totalquota, exquota):
    """
    按年份插入记录

    该函数通过执行一个SQL插入操作，向数据库中插入一条年度数据记录。

    参数:
        year (int): 年份。
        placecode (str): 地点代码。
        place (str): 地点。
        location (str): 位置。
        phone (str): 电话。
        context (str): 上下文或描述。
        totalquota (int): 总指标。
        exquota (int): 额外指标。

    返回值:
        bool: 插入操作成功返回True，失败返回False。
    """
    if year is None:
        print("Year value cannot be null.")
        return False

    query = """
    INSERT INTO eveyeardata (year, placecode, place, location, phone, context, totalquota, exquota)
    VALUES (?, ?, ?, ?, ?, ?, ? ,?)
    """
    
    connection = DBConnection.get_connection()
    
    if connection is None:
        print("无法获取数据库连接")
        return False

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (year, placecode, place, location, phone, context, totalquota, exquota))
            connection.commit()
            return True
    except Exception as e:
        print(f"添加记录失败: {e}")
        return False
    finally:
        connection.close()
