from app.utils.db_utils import DBConnection

# 获取导师下所有候选人
def get_candidates_by_advisor(advisor_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT a.advisor_id, a.name AS advisor_name, c.candidate_id, c.name AS candidate_name, 
                   c.email AS candidate_email, c.phone AS candidate_phone, pm.preference_order, 
                   pm.status, pm.match_date
            FROM dbo.Preference_Match AS pm
            INNER JOIN dbo.Candidate AS c ON pm.candidate_id = c.candidate_id
            INNER JOIN dbo.advisor AS a ON pm.advisor_id = a.advisor_id
            WHERE a.advisor_id = ?
            ORDER BY pm.preference_order;
        """
        cursor.execute(query, (advisor_id,))
        candidates = cursor.fetchall()

        return [
            {
                'advisor_id': row[0],
                'advisor_name': row[1],
                'candidate_id': row[2],
                'candidate_name': row[3],
                'candidate_email': row[4],
                'candidate_phone': row[5],
                'preference_order': row[6],
                'status': row[7],
                'match_date': row[8]
            }
            for row in candidates
        ]

    except Exception as e:
        print(f"Error fetching candidates: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

# 获取导师的年度剩余配额
def check_advisor_quota(advisor_id):
    try:
        connection = DBConnection.get_connection()  # 获取数据库连接
        cursor = connection.cursor()  # 创建游标
        
        query = """
            SELECT annual_quota, assigned_quota
            FROM dbo.advisor
            WHERE advisor_id = ?
        """
        cursor.execute(query, (advisor_id,))
        result = cursor.fetchone()  # 获取查询结果
        
        if result:
            annual_quota, assigned_quota = result
            remaining_quota = (annual_quota or 0) - (assigned_quota or 0)
            return remaining_quota
        else:
            return 0
    
    except Exception as e:
        print(f"Error fetching remaining quota: {e}")
        return 0
    
    finally:
        cursor.close()
        connection.close()

# 插入临时选择记录
def insert_temp_selection(advisor_id, candidate_id, preference_order):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 先检查是否已存在相同的记录
        query = """
            SELECT * FROM temp_selection
            WHERE advisor_id = ? AND candidate_id = ?
        """
        cursor.execute(query, (advisor_id, candidate_id))  # 直接传递 candidate_id，无需强制转换
        result = cursor.fetchone()
        
        if result:
            # 如果已存在记录，更新记录
            update_query = """
                UPDATE temp_selection
                SET preference_order = ?
                WHERE advisor_id = ? AND candidate_id = ?
            """
            cursor.execute(update_query, (preference_order, advisor_id, candidate_id))
        else:
            # 否则插入新记录
            insert_query = """
                INSERT INTO temp_selection (advisor_id, candidate_id, preference_order)
                VALUES (?, ?, ?)
            """
            cursor.execute(insert_query, (advisor_id, candidate_id, preference_order))
        
        connection.commit()  # 提交事务
    except Exception as e:
        print(f"Error inserting/updating temp selection: {e}")
        connection.rollback()  # 回滚事务
    finally:
        cursor.close()  # 关闭游标
        connection.close()  # 关闭连接

# 获取导师临时选择的候选人
def get_temp_selections_by_advisor(advisor_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT selection_id, candidate_id, preference_order
            FROM temp_selection
            WHERE advisor_id = ? AND status = '待确认'
            ORDER BY preference_order;
        """
        cursor.execute(query, (advisor_id,))
        selections = cursor.fetchall()

        return [
            {
                'selection_id': row[0],
                'candidate_id': row[1],
                'preference_order': row[2]
            }
            for row in selections
        ]
    
    except Exception as e:
        print(f"Error fetching temp selections: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

# 删除临时选择记录
def delete_temp_selection(advisor_id, candidate_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        query = """
            DELETE FROM temp_selection
            WHERE advisor_id = ? AND candidate_id = ?
        """
        cursor.execute(query, (advisor_id, candidate_id))
        connection.commit()

    except Exception as e:
        print(f"Error deleting temp selection: {e}")
        connection.rollback()  # 出错时回滚
    finally:
        cursor.close()
        connection.close()

# 更新匹配状态为“已选择”
def update_match_status(advisor_id, candidate_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        query = """
            UPDATE dbo.Preference_Match
            SET status = '已选择', match_date = GETDATE()
            WHERE advisor_id = ? AND candidate_id = ?
        """
        cursor.execute(query, (advisor_id, candidate_id))
        connection.commit()

    except Exception as e:
        print(f"Error updating match status: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

# 更新导师的配额
def update_advisor_quota(advisor_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        query = """
            UPDATE dbo.advisor
            SET assigned_quota = assigned_quota + 1
            WHERE advisor_id = ?
        """
        cursor.execute(query, (advisor_id,))
        connection.commit()
        
        cursor.execute("SELECT assigned_quota FROM dbo.advisor WHERE advisor_id = ?", (advisor_id,))
        result = cursor.fetchone()
        print(f"Updated assigned_quota for advisor {advisor_id}: {result[0]}")  # 打印更新后的值
    
    except Exception as e:
        print(f"Error updating advisor quota: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


# 确认并提交选择
def confirm_and_submit_selection(advisor_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT candidate_id
            FROM temp_selection
            WHERE advisor_id = ? AND status = '待确认'
            ORDER BY preference_order
        """
        cursor.execute(query, (advisor_id,))
        selections = cursor.fetchall()

        for selection in selections:
            candidate_id = selection[0]
            # 更新匹配状态为“已选择”
            update_match_status(advisor_id, candidate_id)
            # 更新导师的配额
            update_advisor_quota(advisor_id)
            # 删除临时选择记录
            delete_temp_selection(advisor_id, candidate_id)

        connection.commit()
        print("Selection confirmed and submitted successfully.")
    
    except Exception as e:
        print(f"Error confirming and submitting selection: {e}")
        connection.rollback()  # 回滚事务
    finally:
        cursor.close()
        connection.close()
