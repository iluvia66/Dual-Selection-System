#dao/ preference_dao.py

from app.utils.db_utils import DBConnection
from datetime import datetime
import random
# 获取临时表数据
def get_temp_selection():
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
            SELECT candidate_id, advisor_id, preference_order, status, created_at 
            FROM dbo.temp_selection
            ORDER BY preference_order ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Fetched temp_selection records:", results)  # 添加调试日志

        return [
            {
                'candidate_id': row[0],
                'advisor_id': row[1],
                'preference_order': row[2],
                'status': row[3],
                'created_at': row[4]
            }
            for row in results
        ]
    except Exception as e:
        print(f"Error fetching temp selection: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


def update_advisor_assign_quota():
    """
    更新导师表中的 assign_quota 字段，基于 Preference_Match 表中已匹配的学生数量。
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # SQL 查询：统计每个导师已匹配的学生数量，并更新到 advisor 表的 assign_quota 字段
        update_query = """
        UPDATE dbo.advisor
        SET assigned_quota = ISNULL((
            SELECT COUNT(*)
            FROM dbo.Preference_Match pm
            WHERE pm.advisor_id = advisor.advisor_id AND pm.status = '已匹配'
        ), 0);
        """
        cursor.execute(update_query)
        connection.commit()
        print("导师表 assign_quota 已成功更新。")

    except Exception as e:
        print(f"Error updating assigned_quota:  {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def perform_matching():
    """
    执行匹配逻辑：
    1. 从临时表 `temp_selection` 获取匹配信息。
    2. 更新 `Preference_Match` 表中学生与导师的状态为 '已匹配'，并记录匹配日期。
    3. 只处理每个学生的第一个志愿（优先级最高）。
    4. 清理 `temp_selection` 表中未被处理的记录。
    5. 返回匹配结果的数据。

    返回:
        matched_data (list): 包含已匹配结果的列表。
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        matched_data = []  # 存储匹配结果

        # 1. 查询临时表数据，按照导师 ID、部门和志愿顺序排序
        query = """
            SELECT ts.candidate_id, ts.advisor_id, ts.preference_order, 
                   c.name AS candidate_name, a.name AS advisor_name, 
                   r.subject_name, a.department
            FROM dbo.temp_selection ts
            INNER JOIN dbo.Candidate c ON ts.candidate_id = c.candidate_id
            INNER JOIN dbo.advisor a ON ts.advisor_id = a.advisor_id
            LEFT JOIN dbo.Retest_Info r ON ts.candidate_id = r.candidate_id
            ORDER BY a.advisor_id, a.department, ts.preference_order ASC
        """
        cursor.execute(query)
        temp_records = cursor.fetchall()  # 获取所有临时表数据

        processed_candidates = set()  # 存储已经匹配的学生 ID

        # 2. 遍历临时表数据，执行匹配逻辑
        for candidate_id, advisor_id, preference_order, candidate_name, advisor_name, subject_name, department in temp_records:
            if candidate_id not in processed_candidates:
                # 更新 Preference_Match 表中的匹配状态和匹配日期
                update_query = """
                    UPDATE dbo.Preference_Match
                    SET status = '已匹配', match_date = ?
                    WHERE candidate_id = ? AND advisor_id = ? AND preference_order = ?
                """
                match_date = datetime.now()
                cursor.execute(update_query, (match_date, candidate_id, advisor_id, preference_order))

                # 保存匹配成功的数据
                matched_data.append({
                    'candidate_id': candidate_id,
                    'advisor_id': advisor_id,
                    'candidate_name': candidate_name,
                    'advisor_name': advisor_name,
                    'subject_name': subject_name or "未指定",
                    'department': department,
                    'match_date': match_date.strftime("%Y-%m-%d %H:%M:%S")
                })

                # 标记该学生已处理
                processed_candidates.add(candidate_id)

        # 3. 清理临时表中未被匹配的记录
        if processed_candidates:
        # 使用参数化查询删除未匹配的记录
            placeholders = ','.join(['?'] * len(processed_candidates))
            delete_query = f"""
                DELETE FROM dbo.temp_selection
                WHERE candidate_id NOT IN ({placeholders})
            """
            print(f"Executing DELETE query: {delete_query}")
            cursor.execute(delete_query, tuple(processed_candidates))
        else:
            # 先检查是否还有待确认的记录
            check_query = "SELECT COUNT(*) FROM dbo.temp_selection"
            cursor.execute(check_query)
            remaining_count = cursor.fetchone()[0]

            if remaining_count > 0:
                print("No new matches. Skipping table cleanup to preserve existing data.")
            else:
                # 如果临时表中本来没有数据，则安全清空
                print("No processed candidates found. Clearing the entire temp_selection table.")
                cursor.execute("DELETE FROM dbo.temp_selection")

        # 提交事务
        connection.commit()
        print("临时表 temp_selection 已清理或保留。")


        # 4. 返回匹配结果
        #return matched_data

        #更新导师的 assign_quota
        update_advisor_assign_quota()

        return matched_data
   
    except Exception as e:
        print(f"Error performing matching: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


#自由匹配阶段

# 自由匹配 - 导师选择学生
def save_free_matching_selection(advisor_id, candidate_id, round_number):
    """
    保存导师选择的学生到 free_matching_temp 表
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO free_matching_temp (advisor_id, candidate_id, round_number, status, created_at)
        VALUES (?, ?, ?, '待确认', GETDATE())
        """
        cursor.execute(query, (advisor_id, candidate_id, round_number))
        connection.commit()
        print(f"导师 {advisor_id} 选择了学生 {candidate_id}，第 {round_number} 轮匹配")
    except Exception as e:
        print(f"Error saving free matching selection: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


# 自由匹配 - 导师跳过
def save_free_matching_skip(advisor_id, round_number):
    """
    保存导师跳过的记录到 free_matching_temp 表
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO free_matching_temp (advisor_id, candidate_id, round_number, status, created_at)
        VALUES (?, NULL, ?, '跳过', GETDATE())
        """
        cursor.execute(query, (advisor_id, round_number))
        connection.commit()
        print(f"导师 {advisor_id} 在第 {round_number} 轮跳过选择")
    except Exception as e:
        print(f"Error saving free matching skip: {e}")
        raise
    finally:
        cursor.close()
        connection.close()



# 自由匹配 - 确认选择
#新增获取当前轮次数据的函数：
def get_free_matching_temp(round_number):
    """
    获取当前轮次的自由匹配临时表数据
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT fm.advisor_id, fm.candidate_id, a.name AS advisor_name, 
               c.name AS candidate_name, fm.round_number, fm.status
        FROM free_matching_temp fm
        LEFT JOIN advisor a ON fm.advisor_id = a.advisor_id
        LEFT JOIN Candidate c ON fm.candidate_id = c.candidate_id
        WHERE fm.round_number = ?
        """
        cursor.execute(query, (round_number,))
        results = cursor.fetchall()

        return [
            {
                "advisor_id": row[0],
                "candidate_id": row[1],
                "advisor_name": row[2],
                "candidate_name": row[3],
                "round_number": row[4],
                "status": row[5]
            }
            for row in results
        ]
    except Exception as e:
        print(f"Error fetching free matching temp data: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


#获取当前轮次和状态
def get_current_round_status():
    """
    获取当前处于 'pending' 状态的轮次信息
    返回:
        dict: 包含当前轮次和状态信息的字典，例如 {"current_round": 1, "status": "pending"}
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT current_round, status
        FROM round_control
        WHERE status = 'pending'
        ORDER BY current_round ASC
        """
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return {"current_round": result[0], "status": result[1]}
        return None
    except Exception as e:
        print(f"Error fetching current round status: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

#更新轮次状态
def update_round_status(round_number, new_status):
    """
    更新指定轮次的状态
    参数:
        round_number (int): 要更新的轮次号
        new_status (str): 新状态，例如 'completed'
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE round_control
        SET status = ?
        WHERE current_round = ?
        """
        cursor.execute(query, (new_status, round_number))
        connection.commit()
        print(f"轮次 {round_number} 状态更新为 {new_status}")
    except Exception as e:
        print(f"Error updating round status: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def execute_batch_free_matching(current_round):
    """
    按优先级匹配自由匹配阶段的学生。
    优先级：未选择过学生的导师 > 剩余名额多的导师。
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 获取自由匹配记录，按优先级排序
        query = """
        SELECT fm.advisor_id, fm.candidate_id, a.name AS advisor_name, c.name AS candidate_name,
               a.annual_quota - a.assigned_quota AS remaining_quota
        FROM free_matching_temp fm
        LEFT JOIN advisor a ON fm.advisor_id = a.advisor_id
        LEFT JOIN Candidate c ON fm.candidate_id = c.candidate_id
        WHERE fm.round_number = ?
        ORDER BY
            CASE WHEN fm.candidate_id IS NULL THEN 1 ELSE 0 END ASC,
            remaining_quota DESC;
        """
        cursor.execute(query, (current_round,))
        free_matching_records = cursor.fetchall()

        # 处理匹配逻辑
        matched_data = []
        for record in free_matching_records:
            advisor_id, candidate_id, advisor_name, candidate_name, remaining_quota = record

            # 如果 candidate_id 为 NULL 或导师名额已满，跳过
            if candidate_id is None:
                print(f"导师 {advisor_id} 跳过了选择，跳过此记录")
                continue
            if remaining_quota <= 0:
                print(f"导师 {advisor_id} 的名额已满，跳过此记录")
                continue

            # 检查学生是否已经被匹配
            check_student_query = """
            SELECT COUNT(*) FROM Preference_Match
            WHERE candidate_id = ? AND status = '已匹配'
            """
            cursor.execute(check_student_query, (candidate_id,))
            already_matched = cursor.fetchone()[0]

            if already_matched > 0:
                print(f"学生 {candidate_id} 已被匹配到其他导师，跳过")
                continue

            # 检查是否已存在匹配记录
            check_query = """
            SELECT COUNT(*) FROM Preference_Match
            WHERE candidate_id = ? AND advisor_id = ?
            """
            cursor.execute(check_query, (candidate_id, advisor_id))
            exists = cursor.fetchone()[0]

            if exists > 0:
                # 如果记录已存在，执行更新
                update_query = """
                UPDATE Preference_Match
                SET preference_order = 4, status = '已匹配', match_type = '自由匹配', match_date = GETDATE()
                WHERE candidate_id = ? AND advisor_id = ?
                """
                cursor.execute(update_query, (candidate_id, advisor_id))
                print(f"更新匹配记录: 学生 {candidate_id}, 导师 {advisor_id}")
            else:
                # 如果记录不存在，执行插入
                insert_query = """
                INSERT INTO Preference_Match (match_id, candidate_id, advisor_id, preference_order, status, match_type, match_date)
                VALUES (NEWID(), ?, ?, 4, '已匹配', '自由匹配', GETDATE());
                """
                cursor.execute(insert_query, (candidate_id, advisor_id))
                print(f"插入新匹配记录: 学生 {candidate_id}, 导师 {advisor_id}")

            # 更新导师表的 assigned_quota
            update_quota_query = """
            UPDATE advisor
            SET assigned_quota = assigned_quota + 1
            WHERE advisor_id = ?;
            """
            cursor.execute(update_quota_query, (advisor_id,))

            # 保存匹配结果
            matched_data.append({
                "advisor_id": advisor_id,
                "candidate_id": candidate_id,
                "advisor_name": advisor_name,
                "candidate_name": candidate_name
            })

        # 清理自由匹配临时表
        delete_query = """
        DELETE FROM free_matching_temp WHERE round_number = ?;
        """
        cursor.execute(delete_query, (current_round,))

        connection.commit()
        return matched_data

    except Exception as e:
        connection.rollback()
        print(f"Error in execute_batch_free_matching: {e}")
        raise
    finally:
        cursor.close()
        connection.close()



def set_next_round_pending(next_round):
    """
    设置下一轮的状态为 'pending'
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        UPDATE round_control
        SET status = 'pending'
        WHERE current_round = ?
        """
        cursor.execute(query, (next_round,))
        connection.commit()
        print(f"轮次 {next_round} 状态已设置为 pending")
    except Exception as e:
        print(f"Error setting next round pending: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

#检查 free_matching_temp 表中是否有 candidate_id 为 NULL 的记录
def debug_free_matching_temp(current_round):
    """
    调试：打印当前轮次的自由匹配临时表数据
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT advisor_id, candidate_id, round_number, status
        FROM free_matching_temp
        WHERE round_number = ?
        """
        cursor.execute(query, (current_round,))
        results = cursor.fetchall()

        print("当前轮次的自由匹配临时表数据:")
        for row in results:
            print(f"导师ID: {row[0]}, 学生ID: {row[1]}, 轮次: {row[2]}, 状态: {row[3]}")

    except Exception as e:
        print(f"Error debugging free_matching_temp: {e}")
    finally:
        cursor.close()
        connection.close()

# 查看所有匹配结果
def get_all_matches():
    """
    获取所有已匹配成功的记录
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT pm.match_id, c.name AS candidate_name, a.name AS advisor_name,
               pm.match_type, pm.match_date
        FROM Preference_Match pm
        INNER JOIN Candidate c ON pm.candidate_id = c.candidate_id
        INNER JOIN advisor a ON pm.advisor_id = a.advisor_id
        WHERE pm.status = '已匹配'
        ORDER BY pm.match_date ASC
        """
        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {
                "match_id": row[0],
                "candidate_name": row[1],
                "advisor_name": row[2],
                "match_type": row[3],
                "match_date": row[4]
            }
            for row in results
        ]
    except Exception as e:
        print(f"Error fetching matched results: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


def get_unmatched_students():
    """
    获取未匹配成功的学生，包括学生的学院信息
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT c.candidate_id, c.name, c.email, c.phone, c.applying_major, c.department
        FROM Candidate c
        WHERE c.candidate_id NOT IN (
            SELECT DISTINCT candidate_id
            FROM Preference_Match
            WHERE status = '已匹配'
        )
        """
        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {
                "candidate_id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "applying_major": row[4],
                "department": row[5]  # 学院信息
            }
            for row in results
        ]
    except Exception as e:
        print(f"Error fetching unmatched students: {e}")
        raise
    finally:
        cursor.close()
        connection.close()






#手动匹配函数
def get_available_advisors():
    """
    获取剩余名额大于 0 的导师列表，包括导师的学院信息
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        query = """
        SELECT advisor_id, name, department, annual_quota - assigned_quota AS remaining_quota
        FROM advisor
        WHERE annual_quota > assigned_quota
        """
        cursor.execute(query)
        results = cursor.fetchall()

        return [
            {
                "advisor_id": row[0],
                "name": row[1],
                "department": row[2],  # 学院信息
                "remaining_quota": row[3]
            }
            for row in results
        ]
    except Exception as e:
        print(f"Error fetching available advisors: {e}")
        raise
    finally:
        cursor.close()
        connection.close()


def manual_match_candidate_to_advisor(candidate_id, advisor_id):
    """
    手动匹配学生到导师：检查是否已有记录，存在则更新状态，不存在则插入新记录。
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 查询是否存在记录
        check_query = """
        SELECT status 
        FROM Preference_Match 
        WHERE candidate_id = ? AND advisor_id = ?
        """
        cursor.execute(check_query, (candidate_id, advisor_id))
        existing_record = cursor.fetchone()

        if existing_record:
            # 如果记录存在但未匹配成功，更新状态
            if existing_record[0] != '已匹配':
                update_query = """
                UPDATE Preference_Match
                SET status = '已匹配', match_type = '手动匹配', match_date = GETDATE()
                WHERE candidate_id = ? AND advisor_id = ?
                """
                cursor.execute(update_query, (candidate_id, advisor_id))
                print(f"匹配记录已更新: 学生 {candidate_id} -> 导师 {advisor_id}")
            else:
                # 如果已匹配，抛出错误提示
                raise ValueError(f"匹配记录已存在: 学生 {candidate_id} -> 导师 {advisor_id}")
        else:
            # 如果记录不存在，插入新匹配记录
            match_id = f"P{random.randint(1000, 9999)}"
            insert_query = """
            INSERT INTO Preference_Match (match_id, candidate_id, advisor_id, preference_order, status, match_type, match_date)
            VALUES (?, ?, ?, 5, '已匹配', '手动匹配', GETDATE())
            """
            cursor.execute(insert_query, (match_id, candidate_id, advisor_id))
            print(f"手动匹配成功: 学生 {candidate_id} -> 导师 {advisor_id}，匹配 ID: {match_id}")

        # 更新导师名额
        update_quota_query = """
        UPDATE advisor
        SET assigned_quota = assigned_quota + 1
        WHERE advisor_id = ?
        """
        cursor.execute(update_quota_query, (advisor_id,))

        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error in manual matching: {e}")
        raise
    finally:
        cursor.close()
        connection.close()
