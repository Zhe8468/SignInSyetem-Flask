'''
改文件用来防止循环导入
以及添加一些项目的通用装饰器
'''

from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import g,redirect,url_for
from functools import wraps

db = SQLAlchemy()
mail = Mail()

# 访问权限限制的装饰器 可以判断用户是否登录
def login_required(func):
    # 这个装饰器要写 不然会导致url_for("signin.tables")变成"signin.wrapper"
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g,'user'):
            return func(*args, **kwargs)
        else:
            # 没有登录 返回登录界面
            return redirect(url_for("users.login"))
    return wrapper
