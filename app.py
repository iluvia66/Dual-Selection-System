from flask import Flask, render_template, request, redirect, url_for, flash
from dao.user_dao import get_user_by_id
from routes.applicant_routes import applicant_bp
from routes.exam_view_routes import exam_view_bp
from routes.sift_routes import sift_bp
from routes.sift_update_routes import sift_update_bp
from routes.candidate_delete_routes import candidate_delete_bp
from routes.retest_info_routes import retest_info_bp
from routes.sift_trigger_routes import sift_trigger_bp
from routes.student_input_routes import student_input_bp
from services.user_service import authenticate_user, authenticate_advisor, register_user
from routes.login_routes import login_bp
from routes.register_routes import register_bp
from services.user_service import authenticate_user, authenticate_advisor, register_user

# 创建 Flask 应用实例
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置会话密钥

# 首页路由
@app.route('/index', methods=['GET'])
def index():
    """
    渲染研究生管理页面
    """
    return render_template('index.html')

# 登录页面路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('userid')  # 获取表单中的 userid
        password = request.form.get('password')  # 获取表单中的 password
        role = request.form.get('role')  # 获取用户角色
        advisor_id = request.form.get('advisor_id')  # 导师 ID，仅在角色为导师时需要

        # 验证用户
        user = authenticate_user(userid, password)

        if user:
            # 根据角色跳转到对应的页面
            if role == '学科管理员':
                return redirect(url_for('admin_page'))  # 跳转到学科管理员页面
            elif role == '导师':
                # 验证导师 ID
                if not advisor_id or not authenticate_advisor(advisor_id):
                    flash("导师 ID 无效或未提供")
                    return redirect(url_for('login'))
                return redirect(url_for('advisor_page', advisor_id=advisor_id))
            elif role == '学生用户':
                return redirect(url_for('candidate_page', userid=userid))  # 跳转到学生页面
            else:
                flash("未知角色，无法登录！")
                return redirect(url_for('login'))
        else:
            flash("用户 ID 或密码错误！")  # 登录失败提示
    return render_template('login.html')

# 注册页面路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        role = request.form['role']
        if register_user(userid, password, role):  # 注册用户
            flash('注册成功，请登录！')
            return redirect(url_for('login'))
        flash('用户 ID 已存在！')  # 注册失败提示
    return render_template('register.html')

# 学科管理员页面路由
@app.route('/admin_page', methods=['GET'])
def admin_page():
    """
    渲染学科管理员页面（admin_base.html）
    """
    return render_template('admin_base.html')

# 导师页面路由
@app.route('/advisor_page/<advisor_id>', methods=['GET'])
def advisor_page(advisor_id):
    """
    渲染导师页面（advisorbase.html）
    """
    return render_template('advisorbase.html', advisor_id=advisor_id)

# 学生用户页面路由
@app.route('/candidate_page', methods=['GET'])
def candidate_page():
    """
    渲染学生用户页面
    """
    userid = request.args.get('userid', None)
    if not userid:
        print("未提供用户 ID，重定向回登录页面")
        flash("无效用户，请重新登录")
        return redirect(url_for('login'))
    return render_template('candidatebase.html', userid=userid)

# 注册蓝图
app.register_blueprint(applicant_bp, url_prefix='/api')
app.register_blueprint(candidate_delete_bp, url_prefix='/')
app.register_blueprint(exam_view_bp, url_prefix='/api')
app.register_blueprint(sift_bp, url_prefix='/api')
app.register_blueprint(sift_update_bp, url_prefix='/api')
app.register_blueprint(retest_info_bp, url_prefix='/api')
app.register_blueprint(sift_trigger_bp)
app.register_blueprint(student_input_bp)
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(register_bp, url_prefix='/auth')

# 启动应用
if __name__ == '__main__':
    app.run(debug=True)
