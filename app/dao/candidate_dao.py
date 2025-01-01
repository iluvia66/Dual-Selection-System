#DAO/candidate_dao.py
from app.utils.db_utils import DBConnection

# 获取导师下所有候选人并按照志愿顺序排序，同时检查临时表中是否已选择该学生
def get_candidates_by_advisor(advisor_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 获取导师的招生资格和配额
        advisor_query = """
            SELECT is_eligible, annual_quota FROM dbo.advisor WHERE advisor_id = ?
        """
        cursor.execute(advisor_query, (advisor_id,))
        advisor_data = cursor.fetchone()

        if advisor_data is None:
            return "导师不存在", 404

        is_eligible, annual_quota = advisor_data

        # 如果导师没有招生资格
        if is_eligible != 1:
            return "该导师无招生权限", 403

        # 获取导师已选择的学生数量
        temp_query = """
            SELECT COUNT(*) FROM dbo.temp_selection WHERE advisor_id = ?
        """
        cursor.execute(temp_query, (advisor_id,))
        selected_count = cursor.fetchone()[0]

        # 获取导师下所有候选人的基本信息
        query = """
            SELECT a.advisor_id, a.name AS advisor_name, c.candidate_id, c.name AS candidate_name, 
                   c.email AS candidate_email, c.phone AS candidate_phone, pm.preference_order, 
                   pm.status, pm.match_date
            FROM dbo.Preference_Match AS pm
            INNER JOIN dbo.Candidate AS c ON pm.candidate_id = c.candidate_id
            INNER JOIN dbo.advisor AS a ON pm.advisor_id = a.advisor_id
            WHERE a.advisor_id = ?
            ORDER BY pm.preference_order;  -- 按照志愿顺序排序
        """
        cursor.execute(query, (advisor_id,))
        candidates = cursor.fetchall()

        # 查询临时表中是否有该导师的选择记录
        temp_query = """
            SELECT candidate_id FROM dbo.temp_selection WHERE advisor_id = ?
        """
        cursor.execute(temp_query, (advisor_id,))
        selected_candidates = {row[0] for row in cursor.fetchall()}  # 临时表中已选择的学生ID集合

        # 打印查询到的候选人数据
        print(f"Fetched candidates for advisor_id {advisor_id}:")
        for candidate in candidates:
            print(candidate)

        # 处理候选人数据，添加 selected 字段
        return {
            "advisor_info": {"is_eligible": is_eligible, "annual_quota": annual_quota, "selected_count": selected_count},
            "candidates": [
                {
                    'advisor_id': row[0],
                    'advisor_name': row[1],
                    'candidate_id': row[2],
                    'candidate_name': row[3],
                    'candidate_email': row[4],
                    'candidate_phone': row[5],
                    'preference_order': row[6],
                    'status': row[7],
                    'match_date': row[8],
                    'selected': row[2] in selected_candidates  # 检查是否已选
                }
                for row in candidates
            ]
        }
    except Exception as e:
        print(f"Error fetching candidates: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

# 保存选择的学生到临时表
def save_selection(advisor_id, candidate_id, preference_order):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 插入选择记录到临时表
        query = """
            INSERT INTO dbo.temp_selection (selection_id, advisor_id, candidate_id, preference_order, status, created_at)
            VALUES (NEWID(), ?, ?, ?, '待确认', GETDATE())
        """
        cursor.execute(query, (advisor_id, candidate_id, preference_order))
        connection.commit()

    except Exception as e:
        print(f"Error saving selection: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

# 移除选择的学生
def remove_selection(advisor_id, candidate_id):
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 从临时表移除选择记录
        query = """
            DELETE FROM dbo.temp_selection 
            WHERE advisor_id = ? AND candidate_id = ?
        """
        cursor.execute(query, (advisor_id, candidate_id))
        connection.commit()

    except Exception as e:
        print(f"Error removing selection: {e}")
        raise
    finally:
        cursor.close()
        connection.close()




#自由选择阶段代码
#获取未匹配的学生
def get_unmatched_students_by_advisor(advisor_id):
    """
    根据导师 ID 获取该导师可匹配的学生列表：
    学生的学院（department）与导师一致，且未被匹配。
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 获取导师的学院
        advisor_query = "SELECT department FROM dbo.advisor WHERE advisor_id = ?"
        cursor.execute(advisor_query, (advisor_id,))
        advisor_department = cursor.fetchone()[0]

        if not advisor_department:
            raise ValueError("导师的学院信息缺失")

        # 获取未匹配的学生，并按学院筛选
        query = """
        SELECT DISTINCT c.candidate_id, c.name
        FROM dbo.Candidate c
        WHERE c.department = ?  -- 学生学院必须与导师学院一致
          AND c.candidate_id NOT IN (
              SELECT DISTINCT candidate_id
              FROM dbo.Preference_Match
              WHERE status = '已匹配'
          );
        """
        cursor.execute(query, (advisor_department,))
        unmatched_students = cursor.fetchall()

        return [{"candidate_id": row[0], "candidate_name": row[1]} for row in unmatched_students]

    except Exception as e:
        print(f"Error fetching unmatched students by advisor: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


#导师获取匹配成功的学生信息
def get_matches_by_advisor(advisor_id):
    """
    获取该导师的匹配成功的学生记录
    """
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()

        # 查询匹配成功的记录
        query = """
        SELECT 
            pm.candidate_id, 
            c.name AS candidate_name, 
            c.email, 
            c.phone, 
            c.nationality, 
            c.exam_id, 
            c.degree, 
            c.applying_major, 
            pm.match_date 
        FROM 
            Preference_Match pm
        INNER JOIN 
            Candidate c 
        ON 
            pm.candidate_id = c.candidate_id
        WHERE 
            pm.advisor_id = ? 
            AND pm.status = '已匹配'
        ORDER BY pm.match_date DESC
        """
        cursor.execute(query, (advisor_id,))
        results = cursor.fetchall()

        # 转换结果为字典列表
        matches = [
            {
                'candidate_id': row[0],
                'candidate_name': row[1],
                'email': row[2],
                'phone': row[3],
                'nationality': row[4],
                'exam_id': row[5],
                'degree': row[6],
                'applying_major': row[7],
                'match_date': row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] else None
            }
            for row in results
        ]

        return matches

    except Exception as e:
        print(f"Error fetching matches for advisor {advisor_id}: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
