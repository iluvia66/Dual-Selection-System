from dbutils.pooled_db import PooledDB
import pyodbc
import logging

class DBConnection:
    # 配置并创建连接池
    pool = PooledDB(
        creator=pyodbc.connect,  # 使用 pyodbc.connect 作为 creator
        maxconnections=10,
        mincached=2,
        maxcached=5,
        blocking=True,
        driver='{ODBC Driver 17 for SQL Server}',  # 确保使用正确的驱动
        server='XU',  # 数据库服务器地址
        database='dual_selection_system',  # 数据库名称
        uid='sa',  # 用户名
        pwd='111111'  # 密码
    )

    @classmethod
    def get_connection(cls):
        """从连接池中获取一个数据库连接"""
        try:
            connection = cls.pool.connection()
            return connection
        except pyodbc.Error as e:
            logging.error(f"连接失败: {e}")
            raise e  # 抛出异常，便于上层调用捕获

# 测试连接
if __name__ == "__main__":
    try:
        connection = DBConnection.get_connection()
        print("成功连接到 SQL Server!")
        connection.close()  # 关闭连接，返回到连接池
    except pyodbc.Error as e:
        print("连接失败:", e)
