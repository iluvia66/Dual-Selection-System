#routes/task_line3.py
from flask import Blueprint, render_template, request, redirect, url_for
from app.dao import candidate_dao  # 导入DAO层
from app.dao import advisor_dao
from app.dao import preference_dao
from app.dao.preference_dao import save_free_matching_selection, save_free_matching_skip
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

        return render_template('advisor_candidates.html', advisor_base="advisor_base.html",advisor_info=advisor_info, candidates=candidates,advisor_id=advisor_id ) # 传递 advisor_id)
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



#自由匹配阶段代码
# 自由匹配阶段查看学生
# 自由匹配页面返回链接修正
@task_line3.route('/free_matching/<advisor_id>', methods=['GET'])
def free_matching(advisor_id):
    """
    自由匹配导师界面：检查轮次状态并显示当前轮次内容
    """
    try:
        # 获取当前轮次状态
        current_round = preference_dao.get_current_round_status()
        if not current_round:
            return render_template(
                'error_page.html',
                error_message="当前没有待操作的轮次，请等待管理员完成操作。"
            ), 403

        # 获取当前轮次的临时记录
        selected_records = preference_dao.get_free_matching_temp(current_round["current_round"])

        # 检查是否当前导师已经提交了选择或跳过
        has_selected = any(record["advisor_id"] == advisor_id for record in selected_records)
        if has_selected:
            return render_template(
                'buffer_page.html',
                message="本轮选择已完成，请等待管理员完成匹配操作。"
            )

        # 获取导师信息
        advisor_info = advisor_dao.get_advisor_info(advisor_id)
        if not advisor_info:
            return render_template(
                'error_page.html',
                error_message="导师信息未找到或导师无剩余名额"
            ), 404

        # 获取符合条件的学生列表
        candidates = candidate_dao.get_unmatched_students_by_advisor(advisor_id)
        print(f"Candidates: {candidates}")  # 调试日志
        # 渲染自由匹配页面
        return render_template(
            'free_matching.html',
            advisor_info=advisor_info,
            candidates=candidates,
            round_number=current_round["current_round"],
            advisor_id=advisor_id  # 传递 advisor_id
        )
    except Exception as e:
        print(f"Error in free matching: {e}")
        return "Error loading free matching page", 500





# 自由匹配选择学生
@task_line3.route('/free_matching/<advisor_id>/select/<candidate_id>', methods=['POST'])
def free_matching_select(advisor_id, candidate_id):
    """
    导师选择学生或跳过操作
    """
    try:
        action = request.form.get("action")  # 获取操作类型
        round_number = int(request.form.get("round_number", 1))  # 当前轮次

        # 检查当前导师是否已选择
        selected_records = preference_dao.get_free_matching_temp(round_number)
        has_selected = any(record["advisor_id"] == advisor_id for record in selected_records)
        if has_selected:
            return render_template(
                'buffer_page.html',
                message="您已完成本轮选择，请等待管理员完成匹配操作。"
            )

        # 保存选择记录或跳过记录
        if action == "select":
            save_free_matching_selection(advisor_id, candidate_id, round_number)
        elif action == "skip":
            save_free_matching_skip(advisor_id, round_number)

        # 跳转到缓冲页面
        return render_template(
            'buffer_page.html',
            message="您已完成本轮选择，请等待管理员完成匹配操作。"
        )
    except Exception as e:
        print(f"Error in free matching selection: {e}")
        return "Error handling free matching selection", 500



#导师查看匹配结果代码
@task_line3.route('/advisor/<advisor_id>/matches', methods=['GET'])
def view_matches(advisor_id):
    """
    查看该导师的匹配结果
    """
    try:
        # 获取该导师的匹配记录
        matches = candidate_dao.get_matches_by_advisor(advisor_id)

        # 渲染模板，传递匹配结果
        return render_template('advisor_matches.html', advisor_id=advisor_id, matches=matches)
    except Exception as e:
        print(f"Error fetching matches for advisor {advisor_id}: {e}")
        return "Error fetching matches", 500
