from flask import Blueprint, redirect, render_template, request, make_response, url_for
from app.dao import preference_dao
from app.dao.preference_dao import execute_batch_free_matching, get_current_round_status, get_temp_selection, perform_matching, set_next_round_pending, update_round_status  # 导入 DAO 层逻辑
import csv
from io import StringIO

# 定义蓝图
preference_dao_bp = Blueprint('admin_matching', __name__)  # 蓝图名称

# 志愿匹配页面
@preference_dao_bp.route('/matching', methods=['GET'])
def view_matching():
    """
    管理员查看志愿匹配临时表
    """
    try:
        temp_data = get_temp_selection()
        return render_template('admin_matching.html', temp_data=temp_data, matched_data=None)
    except Exception as e:
        print(f"Error: {e}")
        return "Error loading matching page", 500

# 执行志愿匹配
@preference_dao_bp.route('/matching/run', methods=['POST'])
def run_matching():
    """
    管理员执行志愿匹配
    """
    try:
        matched_data = perform_matching()
        temp_data = get_temp_selection()
        return render_template('admin_matching.html', temp_data=temp_data, matched_data=matched_data)
    except Exception as e:
        print(f"Error: {e}")
        return "Error running matching", 500

# 导出志愿匹配结果为 CSV
@preference_dao_bp.route('/matching/export', methods=['GET'])
def export_matching():
    """
    导出志愿匹配结果为 CSV 文件
    """
    try:
        matched_data = perform_matching()

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Candidate ID', 'Candidate Name', 'Advisor ID', 'Advisor Name', 'Subject Direction', 'Department', 'Match Date'])
        for match in matched_data:
            writer.writerow([
                match['candidate_id'], 
                match['candidate_name'], 
                match['advisor_id'], 
                match['advisor_name'], 
                match['subject_name'], 
                match['department'], 
                match['match_date']
            ])

        output.seek(0)
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=matching_results.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response
    except Exception as e:
        print(f"Error exporting matching: {e}")
        return "Error exporting matching", 500

# 自由匹配查看页面
@preference_dao_bp.route('/free_matching', methods=['GET'])
def free_matching_admin_view():
    """
    管理员查看自由匹配临时数据
    """
    try:
        # 获取当前轮次
        round_number = request.args.get("round_number", 1, type=int)
        temp_data = preference_dao.get_free_matching_temp(round_number)

        # 渲染模板
        return render_template(
            'admin_free_matching.html',
            round_number=round_number,
            temp_data=temp_data
        )
    except Exception as e:
        print(f"Error loading admin free matching page: {e}")
        return "Error loading admin free matching page", 500


# 执行自由匹配
@preference_dao_bp.route('/free_matching/run', methods=['POST'])
def run_free_matching():
    """
    管理员执行自由匹配逻辑并更新轮次状态
    """
    try:
        # 获取当前轮次
        current_round = get_current_round_status()
        if not current_round:
            return {"status": "error", "message": "当前没有待操作的轮次"}, 400

        # 执行自由匹配逻辑
        matched_data = execute_batch_free_matching(current_round["current_round"])

        # 更新当前轮次为 completed
        update_round_status(current_round["current_round"], "completed")

        # 设置下一轮为 pending
        set_next_round_pending(current_round["current_round"] + 1)
        # 检查是否已是最后一轮
        if current_round["current_round"] >= 3:
            # 跳转到匹配结果页面
            return redirect(url_for('admin_matching.view_all_matches'))

        # 跳转到下一轮的自由匹配管理页面
        next_round = current_round["current_round"] + 1
        return redirect(url_for('admin_matching.free_matching_admin_view', round_number=next_round))
    except Exception as e:
        print(f"Error in batch matching: {e}")
        return {"status": "error", "message": str(e)}, 500


@preference_dao_bp.route('/matching/results', methods=['GET'])
def view_all_matches():
    """
    管理员查看所有匹配结果和未匹配的学生
    """
    try:
        # 获取已匹配的结果
        matches = preference_dao.get_all_matches()

        # 获取未匹配的学生
        unmatched_students = preference_dao.get_unmatched_students()

        # 渲染模板
        return render_template(
            'all_matches.html',
            matches=matches,
            unmatched_students=unmatched_students
        )
    except Exception as e:
        print(f"Error loading all matches: {e}")
        return "Error loading all matches", 500



#手动匹配阶段代码
@preference_dao_bp.route('/manual_matching', methods=['GET'])
def manual_matching():
    """
    管理员手动匹配页面
    """
    try:
        # 获取未匹配学生和导师信息
        unmatched_students = preference_dao.get_unmatched_students()
        available_advisors = preference_dao.get_available_advisors()

        # 获取最新的匹配记录
        matched_data = preference_dao.get_all_matches()

        # 渲染手动匹配页面
        return render_template(
            'manual_matching.html',
            unmatched_students=unmatched_students,
            available_advisors=available_advisors,
            matched_data=matched_data  # 添加已匹配记录到页面
        )
    except Exception as e:
        print(f"Error loading manual matching page: {e}")
        return "Error loading manual matching page", 500



@preference_dao_bp.route('/manual_matching/submit', methods=['POST'])
def manual_matching_submit():
    """
    处理管理员手动匹配提交
    """
    try:
        # 获取表单数据
        candidate_id = request.form.get("candidate_id")
        advisor_id = request.form.get("advisor_id")

        if not candidate_id or not advisor_id:
            return {"status": "error", "message": "学生或导师不能为空"}, 400

        try:
            # 调用手动匹配 DAO 方法
            preference_dao.manual_match_candidate_to_advisor(candidate_id, advisor_id)

            # 匹配成功后重定向到避免重复提交
            return redirect(url_for('admin_matching.manual_matching'))
        except ValueError as e:
            # 捕获错误信息返回页面
            unmatched_students = preference_dao.get_unmatched_students()
            available_advisors = preference_dao.get_available_advisors()
            matched_data = preference_dao.get_all_matches()

            return render_template(
                'manual_matching.html',
                unmatched_students=unmatched_students,
                available_advisors=available_advisors,
                matched_data=matched_data,
                error_message=str(e)
            )
    except Exception as e:
        print(f"Error in manual matching: {e}")
        return {"status": "error", "message": str(e)}, 500


@preference_dao_bp.route('/settings', methods=['GET'])
def settings():
    """
    管理员系统设置页面
    """
    return render_template('settings.html')
