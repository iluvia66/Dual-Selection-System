from flask import Blueprint, render_template, redirect, url_for, request, flash

# 假设app.dao已经定义了相应的数据访问对象
from app.dao import advisor_dao
from app.dao import everyeardata_dao
from app.dao import menu_dao
from app.dao import menu_v_dao

# 定义蓝图
public = Blueprint('public', __name__)

@public.route('/base_advisor', methods=['GET','POST'])
def base_advisor():
    # 渲染 base_advisor.html 页面
    return render_template('base_advisor.html')