from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.dao import candidate_dao

# 定义蓝图
task_line3 = Blueprint('task_line3', __name__)

# 获取导师候选人列表的视图
@task_line3.route('/advisor/<advisor_id>/candidates', methods=['GET'])
def get_candidates(advisor_id):
    try:
        # 获取导师的候选人、临时选择和剩余配额
        candidates = candidate_dao.get_candidates_by_advisor(advisor_id)
        temp_selections = candidate_dao.get_temp_selections_by_advisor(advisor_id)
        
        # 获取导师的剩余配额，假设check_advisor_quota返回的是剩余配额
        remaining_quota = candidate_dao.check_advisor_quota(advisor_id)

        # 如果没有配额或配额有问题，可以显示提示信息
        if remaining_quota is None:
            flash("Error: Could not fetch remaining quota for the advisor.", "error")
            remaining_quota = 0

        return render_template(
            'advisor_candidates.html', 
            candidates=candidates, 
            temp_selections=temp_selections, 
            remaining_quota=remaining_quota, 
            advisor_id=advisor_id
        )
    except Exception as e:
        flash(f"Error fetching candidates: {e}", "error")
        return redirect(url_for('task_line3.get_candidates', advisor_id=advisor_id))

# 导师选择候选人的视图
@task_line3.route('/advisor/<advisor_id>/candidates/<candidate_id>/select', methods=['POST'])
def select_candidate(advisor_id, candidate_id):
    try:
        # 不强制转换 candidate_id 为 int，直接使用原始值
        # 但是我们确保 candidate_id 应该是一个有效的整数
        candidate_id = int(candidate_id)  # candidate_id 应该是 int 类型的，已经是 int 类型就无需再次转换

        # 获取剩余配额
        remaining_quota = candidate_dao.check_advisor_quota(advisor_id)

        if remaining_quota <= 0:
            return {"error": "No remaining quota for this advisor"}, 400

        # 获取候选人的优先级
        preference_order = request.form.get('preference_order')

        # 插入临时选择记录
        candidate_dao.insert_temp_selection(advisor_id, candidate_id, preference_order)

        # 更新剩余配额
        remaining_quota -= 1

        # 获取该候选人的详细信息
        # 假设 candidates 是一个列表，查询该候选人的信息
        candidates = candidate_dao.get_candidates_by_advisor(advisor_id)  # 获取候选人列表
        candidate = next((candidate for candidate in candidates if candidate['candidate_id'] == candidate_id), None)

        if candidate is None:
            return {"error": "Candidate not found"}, 404

        return {
            "candidate_name": candidate['candidate_name'],
            "preference_order": preference_order,
            "remaining_quota": remaining_quota
        }

    except Exception as e:
        return {"error": str(e)}, 500


# 确认并提交导师的选择
@task_line3.route('/advisor/<advisor_id>/confirm_selection', methods=['POST'])
def confirm_selection(advisor_id):
    try:
        # 提交并确认选择
        candidate_dao.confirm_and_submit_selection(advisor_id)
        flash("Selection confirmed and submitted successfully", "success")
        return redirect(url_for('task_line3.get_candidates', advisor_id=advisor_id))
    except Exception as e:
        flash(f"Error confirming selection: {e}", "error")
        return redirect(url_for('task_line3.get_candidates', advisor_id=advisor_id))
