# app/__init__.py
from flask import Flask
from .routes.task_line3 import task_line3  # 只保留 task_line3 的导入
from app.routes.preference_dao import preference_dao_bp  # 修改为新的蓝图路径

def create_app():
    app = Flask(__name__)
    
    # 注册蓝图
    app.register_blueprint(task_line3, url_prefix='/task_line3')  # 添加 url_prefix
    app.register_blueprint(preference_dao_bp, url_prefix='/admin')  # 注册管理员匹配功能的蓝图

    return app
