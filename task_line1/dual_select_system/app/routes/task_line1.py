# task_line1.py

from flask import Blueprint, render_template, redirect, url_for, request, session, flash

# 假设app.dao已经定义了相应的数据访问对象
from app.dao import advisor_dao
from app.dao import everyeardata_dao
from app.dao import menu_dao
from app.dao import menu_v_dao

import sys
from pathlib import Path
# 获取当前文件的路径
current_file_path = Path(__file__).resolve()
# 获取项目的根路径
project_root = current_file_path.parent.parent.parent
# 将项目的根路径添加到 sys.path
sys.path.append(str(project_root))

# 定义蓝图
task_line1 = Blueprint('task_line1', __name__)

#更新所有导师信息
@task_line1.route('/advisor/update', methods=['GET','POST'])
def update_advisor():
    advisor_id = request.form.get('advisor_id')
    name = request.form.get('name')
    title = request.form.get('title')
    photo_URL = request.form.get('photo_URL')
    biography = request.form.get('biography')
    email = request.form.get('email')
    phone = request.form.get('phone')
    department = request.form.get('department')
    annual_quota = request.form.get('annual_quota')
    assigned_quota = request.form.get('assigned_quota')
    
    if advisor_id and name and title and email and phone and department and annual_quota and assigned_quota:
        success = advisor_dao.update_advisor(advisor_id=advisor_id, name=name, title=title, photo_URL=photo_URL, biography=biography, email=email, phone=phone, department=department, annual_quota=annual_quota, assigned_quota=assigned_quota)
        if success:
            flash("Advisor information updated successfully!", "success")
        else:
            flash("Failed to update advisor information.", "error")
    else:
        flash("Invalid input.", "error")
    advisors = advisor_dao.get_all_advisors()
    return render_template('advisor.html', advisors=advisors)

#更新指定导师信息
@task_line1.route('/advisor/update_one', methods=['GET','POST'])
def update_one_advisor():
    advisor_id = request.form.get('advisor_id')
    name = request.form.get('name')
    title = request.form.get('title')
    photo_URL = request.form.get('photo_URL')
    biography = request.form.get('biography')
    email = request.form.get('email')
    phone = request.form.get('phone')
    department = request.form.get('department')
    annual_quota = request.form.get('annual_quota')
    assigned_quota = request.form.get('assigned_quota')
    
    if advisor_id and name and title and email and phone and department and annual_quota and assigned_quota:
        success = advisor_dao.update_advisor(
            advisor_id=advisor_id, 
            name=name, 
            title=title, 
            photo_URL=photo_URL, 
            biography=biography, 
            email=email, 
            phone=phone, 
            department=department, 
            annual_quota=annual_quota, 
            assigned_quota=assigned_quota
        )
        if success:
            flash("Advisor information updated successfully!", "success")
        else:
            flash("Failed to update advisor information.", "error")
    else:
        flash("Invalid input.", "error")
    advisor_id="L001"
    # 只获取指定advisor_id的导师信息
    advisor = advisor_dao.get_advisor_by_id(advisor_id)
    
    return render_template('aovisor_update.html', advisor=advisor)

#更新导师职称
@task_line1.route('/advisor/update_title', methods=['GET', 'POST'])
def update_advisor_title_route():
    if request.method == 'POST':
        advisor_id = request.form.get('advisor_id')
        #name = request.form.get('name')
        new_title = request.form.get('new_title')
        print(advisor_id)
        if advisor_id and new_title:
            #print("if执行")
            success = advisor_dao.update_advisor_title(advisor_id=advisor_id, new_title=new_title)
            if success:
                flash("Title updated successfully!", "success")
            else:
                flash("Failed to update title.", "error")
        else:
            flash("Invalid input.", "error")
    
    advisors = advisor_dao.get_all_advisors()
    return render_template('advisor_title.html', advisors=advisors)

#更新导师招生人数
@task_line1.route('/advisor/update_quota', methods=['GET', 'POST'])
def update_advisor_quota_route():
    if request.method == 'POST':
        advisor_id = request.form.get('advisor_id')
        annual_quota = request.form.get('annual_quota', type=int)
        assigned_quota = request.form.get('assigned_quota', type=int)

        if not assigned_quota:
            assigned_quota = annual_quota  # 如果未指定 assigned_quota，则默认与 annual_quota 相等

        if advisor_id and annual_quota is not None:
            # 更新记录
            success = advisor_dao.update_annual_quota(advisor_id=advisor_id, new_annual_quota=annual_quota, new_assigned_quota=assigned_quota)
            if success:
                flash("Quota updated successfully!", "success")
            else:
                flash("Failed to update quota.", "error")
        else:
            flash("Advisor ID and Annual Quota are required.", "error")

    advisors = advisor_dao.get_all_advisors()  # 假设这个函数返回所有顾问的记录
    return render_template('advisor_quota.html', advisors=advisors)

#everyeardata更新每年的记录
@task_line1.route('/everyeardata/update', methods=['GET', 'POST'])
def update_everyeardata_route():
    if request.method == 'POST':
        year = request.form.get('year')
        # 假设其他字段也通过表单提交
        placecode = request.form.get('placecode')
        place = request.form.get('place')
        location = request.form.get('location')
        phone = request.form.get('phone')
        context = request.form.get('context')
        totalquota = request.form.get('totalquota')
        exquota = request.form.get('exquota')

        if year:
            # 更新记录
            success = everyeardata_dao.update_everyeardata(year=year, placecode=placecode, place=place, location=location, phone=phone, context=context, totalquota=totalquota, exquota=exquota)
            if success:
                flash("Record updated successfully!", "success")
            else:
                flash("Failed to update record.", "error")
        else:
            flash("Year is required.", "error")
    
    records = everyeardata_dao.get_all_everyeardata()  # 假设这个函数返回所有记录
    return render_template('everyeardata.html', records=records)

#everyeardata插入新纪录
@task_line1.route('/everyeardata/insert', methods=['GET','POST'])
def insert_everyeardata_route():
    year = request.form.get('year')
    if not year:
        flash("Year is required.", "error")
        return redirect(url_for('task_line1.update_everyeardata_route'))

    if everyeardata_dao.year_exists_everyeardata(year):  # 假设这个函数检查记录是否存在
        flash('Year already exists!', 'error')
        return redirect(url_for('task_line1.update_everyeardata_route'))

    # 插入新记录
    success = everyeardata_dao.insert_everyeardata(year=year, placecode=request.form.get('placecode'), place=request.form.get('place'), location=request.form.get('location'), phone=request.form.get('phone'), context=request.form.get('context'), totalquota=request.form.get('totalquota'), exquota=request.form.get('exquota'))
    if success:
        flash("New record inserted successfully!", "success")
    else:
        flash("Failed to insert new record.", "error")

    return redirect(url_for('task_line1.update_everyeardata_route'))

# 获取所有菜单项并显示在页面上
@task_line1.route('/menus')
def show_menus():
    menus = menu_dao.get_all_menus()
    return render_template('menu.html', menus=menus)

# 添加新菜单项
@task_line1.route('/menus/add', methods=['GET','POST'])
def insert_menu():
    year = request.form['year']
    advisor_id = request.form['advisor_id']
    is_eligible = request.form.get('is_eligible', 'off') == 'on'
    
    if menu_dao.insert_new_menu(year, advisor_id, is_eligible):
        flash('New menu added successfully!', 'success')
    else:
        flash('Failed to add new menu.', 'error')
    
    return redirect(url_for('.show_menus'))

# 更新现有菜单项
@task_line1.route('/menus/update', methods=['GET','POST'])
def update_menu():
    #print("路由被触发")
    if request.method == 'POST':
        mno = request.form['mno']
        year = request.form['year']
        advisor_id = request.form['advisor_id']
        is_eligible = request.form.get('is_eligible', 'off') == 'on'
        print(mno,year,advisor_id,is_eligible)
        if menu_dao.update_menu_record(mno, year, advisor_id, is_eligible):
            flash('Menu updated successfully!', 'success')
        else:
            flash('Failed to update menu.', 'error')
    
    return redirect(url_for('.show_menus'))

# 删除菜单项
@task_line1.route('/menus/delete/<int:mno>', methods=['GET','POST'])
def delete_menu(mno):
    if menu_dao.delete_menu_record(mno):
        flash('Menu deleted successfully!', 'success')
    else:
        flash('Failed to delete menu.', 'error')
    
    return redirect(url_for('.show_menus'))

#获取所有视图
@task_line1.route('/menu_v', methods=['GET', 'POST'])
def get_menu_v():
    '''
    if request.method == 'POST':
        year = request.form.get('year')
        if year:
            # 调用 menu_v_dao 中的 update_advisor 函数
            menu_v_dao.update_advisor(year)
            flash('Advisor updated successfully for year: {}'.format(year), 'success')
        else:
            flash('Year is required.', 'error')
        # 刷新页面
        return redirect(url_for('task_line1./advisor/update_quota'))
    '''
    # 获取视图数据
    view_data = menu_v_dao.get_all_menu_v()
    return render_template('menu_v.html', view_data=view_data)

#更新每年资格
@task_line1.route('/submit_year', methods=['POST'])
def update_year_is_eligible_route():
    if request.method == 'POST':
        year = request.form.get('year')
        if year:
            # 调用 menu_v_dao 中的 update_advisor 函数
            menu_v_dao.update_advisor(year)
            flash('Advisor updated successfully for year: {}'.format(year), 'success')
        else:
            flash('Year is required.', 'error')
        # 刷新页面
        return redirect(url_for('task_line1.update_advisor_quota_route'))

#注册
from app.services.user_service import register_user
@task_line1.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        role = request.form['role']  # 获取用户选择的角色
        if register_user(userid, password, role):
            flash('注册成功，请登录！')
            return redirect(url_for('task_line1.login'))
        flash('用户ID已存在！')
    return render_template('register.html')

#登录
from app.services.user_service import authenticate_user
@task_line1.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')  # 获取表单中的 userid
        password = request.form.get('password')  # 获取表单中的 password

        # 调用 authenticate_user 验证用户
        user = authenticate_user(userid, password)
        if user:
            role = user['role']
            if role == '学生用户':
                print(f"学生用户登录成功，用户ID: {userid}")
                return redirect(url_for('task_line1.candidate_base', userid=userid))
            elif role == '学科管理员':
                return redirect(url_for('task_line1.admin_base'))
            elif role == '导师':
                return redirect(url_for('task_line1.advisor_base'))
            else:
                flash('未知角色，无法登录！')
                return redirect(url_for('task_line1.login'))
        else:
            flash('用户ID或密码错误！')  # 登录失败提示
    return render_template('login.html')