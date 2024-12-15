from app.utils.db_utils import DBConnection
from datetime import datetime

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

# 执行匹配逻辑
def perform_matching():
    try:
        connection = DBConnection.get_connection()
        cursor = connection.cursor()
        matched_data = []

        # 查询临时表数据，按照 candidate_id 和 preference_order 排序
        query = """
            SELECT ts.candidate_id, ts.advisor_id, ts.preference_order, c.name AS candidate_name, 
                   a.name AS advisor_name, r.subject_name, a.department
            FROM dbo.temp_selection ts
            INNER JOIN dbo.Candidate c ON ts.candidate_id = c.candidate_id
            INNER JOIN dbo.advisor a ON ts.advisor_id = a.advisor_id
            LEFT JOIN dbo.Retest_Info r ON ts.candidate_id = r.candidate_id
            ORDER BY a.advisor_id, a.department, ts.preference_order ASC
        """
        cursor.execute(query)
        temp_records = cursor.fetchall()

        processed_candidates = set()

        for candidate_id, advisor_id, preference_order, candidate_name, advisor_name, subject_name, department in temp_records:
            if candidate_id not in processed_candidates:
                # 更新到 Preference_Match 表
                update_query = """
                    UPDATE dbo.Preference_Match
                    SET status = '已匹配', match_date = ?
                    WHERE candidate_id = ? AND advisor_id = ?
                """
                match_date = datetime.now()
                cursor.execute(update_query, (match_date, candidate_id, advisor_id))

                # 保存匹配结果
                matched_data.append({
                    'candidate_id': candidate_id,
                    'advisor_id': advisor_id,
                    'candidate_name': candidate_name,
                    'advisor_name': advisor_name,
                    'subject_name': subject_name or "未指定",
                    'department': department,
                    'match_date': match_date
                })

                processed_candidates.add(candidate_id)

        # 删除未匹配的记录
        delete_query = """
            DELETE FROM dbo.temp_selection
            WHERE candidate_id NOT IN ({})
        """.format(", ".join(map(str, processed_candidates)))
        cursor.execute(delete_query)

        connection.commit()
        return matched_data
    except Exception as e:
        print(f"Error performing matching: {e}")
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


