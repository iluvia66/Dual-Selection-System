from app.utils.db_utils import db_session

class PreferenceDAO:
    @staticmethod
    def get_students_by_advisor(advisor_id):
        query = """
            SELECT *
            FROM View_Advisor_Student_Preferences
            WHERE advisor_id = :advisor_id
        """
        result = db_session.execute(query, {'advisor_id': advisor_id})
        return result.fetchall()
