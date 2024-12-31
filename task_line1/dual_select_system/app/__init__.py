#app/__init__.py
from flask import Flask
from .routes.task_line1 import task_line1
from .routes.task_line3 import task_line3  # 导入task_line3蓝图

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # 替换为一个复杂的、唯一的字符串
    app.register_blueprint(task_line3, url_prefix='/task_line3')  # 注册蓝图并指定URL前缀
    app.register_blueprint(task_line1, url_prefix='/task_line1')
    return app
