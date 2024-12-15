#routes/task_line3.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.dao import candidate_dao  # 导入DAO层

task_line3 = Blueprint('task_line3', __name__)

# 查看导师的候选人
@task_line3.route('/advisor/<advisor_id>/candidates', methods=['GET'])
def get_candidates(advisor_id):
    try:
        response = candidate_dao.get_candidates_by_advisor(advisor_id)

        # 如果返回错误信息
        if isinstance(response, tuple):
            error_message, status_code = response
            return render_template('error_page.html', error_message=error_message), status_code

        advisor_info = response["advisor_info"]
        candidates = response["candidates"]

        return render_template('advisor_candidates.html', advisor_info=advisor_info, candidates=candidates)
    except Exception as e:
        print(f"Error: {e}")
        return "Error fetching candidates", 500

# 保存或移除选择的学生
@task_line3.route('/advisor/<advisor_id>/candidates/<candidate_id>/toggle', methods=['POST'])
def toggle_selection(advisor_id, candidate_id):
    try:
        action = request.form.get("action")
        preference_order = int(request.form.get("preference_order", 0))

        if action == "select":
            candidate_dao.save_selection(advisor_id, candidate_id, preference_order)
        elif action == "remove":
            candidate_dao.remove_selection(advisor_id, candidate_id)

        return redirect(url_for('task_line3.get_candidates', advisor_id=advisor_id))
    except Exception as e:
        print(f"Error: {e}")
        return "Error toggling selection", 500
