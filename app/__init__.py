from flask import Flask
from .routes.task_line3 import task_line3  # 导入任务线 3 蓝图
from .routes.preference_dao import preference_dao_bp  # 导入管理员匹配功能蓝图

def create_app():
    """
    创建并初始化 Flask 应用
    """
    app = Flask(__name__)
    
    # 注册蓝图
    app.register_blueprint(task_line3, url_prefix='/task_line3')  # 任务线 3 的功能，如自由匹配等
    app.register_blueprint(preference_dao_bp, url_prefix='/admin')  # 管理员相关功能，如志愿匹配
    #app.register_blueprint(preference_dao_bp, url_prefix='/admin_matching')
    # 可以加入更多初始化配置，例如数据库、日志等
    return app
