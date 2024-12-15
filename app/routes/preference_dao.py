#routes/preference_dao.py
from flask import Blueprint, render_template, request, make_response
from app.dao.preference_dao import get_temp_selection, perform_matching  # 导入 DAO 层的逻辑
import csv
from io import StringIO

# 定义蓝图
preference_dao_bp = Blueprint('admin_matching', __name__)  # 名称保持一致

# 查看匹配页面
@preference_dao_bp.route('/matching', methods=['GET'])
def view_matching():
    try:
        temp_data = get_temp_selection()
        return render_template('admin_matching.html', temp_data=temp_data, matched_data=None)
    except Exception as e:
        print(f"Error: {e}")
        return "Error loading matching page", 500

# 执行匹配
@preference_dao_bp.route('/matching/run', methods=['POST'])
def run_matching():
    try:
        # 调用匹配逻辑
        matched_data = perform_matching()
        # 重新获取临时表数据
        temp_data = get_temp_selection()
        return render_template('admin_matching.html', temp_data=temp_data, matched_data=matched_data)
    except Exception as e:
        print(f"Error: {e}")
        return "Error running matching", 500

# 导出匹配结果为 CSV 文件
@preference_dao_bp.route('/matching/export', methods=['GET'])
def export_matching():
    try:
        # 获取匹配数据
        matched_data = perform_matching()

        # 生成 CSV 数据
        output = StringIO()
        writer = csv.writer(output)
        # 写入表头
        writer.writerow(['Candidate ID', 'Candidate Name', 'Advisor ID', 'Advisor Name', 'Subject Direction', 'Department', 'Match Date'])
        # 写入数据
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
        
        # 创建 Flask 响应
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=matching_results.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response

    except Exception as e:
        print(f"Error exporting matching: {e}") 
        return "Error exporting matching", 500
