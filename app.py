from flask import Flask,session,g
from exts import db,mail
from blueprints import users_bp,signin_bp,admin_bp
from flask_migrate import Migrate
from models import UserModel
from flask_wtf import CSRFProtect

app = Flask(__name__)
# 配置绑定
app.config.from_pyfile("config.py")
# 数据库绑定
db.init_app(app)
# 邮箱绑定
mail.init_app(app)
# 数据库迁移对象
migrate = Migrate(app,db)
# 蓝图注册
app.register_blueprint(users_bp)
app.register_blueprint(signin_bp)
app.register_blueprint(admin_bp)
# CSRF攻击保护
csrf = CSRFProtect(app)
# 上下文管理器
@app.before_request
def before_request():
    # 获取session中的id
    user_id = session.get("user_id")
    # 存在id 说明用户已经登录
    if user_id:
        # 防止get报错
        try:
            user_model = UserModel.query.get(user_id)
            # 给全局变量绑定用户ORM模型 在任何地方都可以方便操作
            g.user = user_model
        except:
            g.user = None

# 请求路径
# before_request ---> 视图函数 ----> 返回模板  ----> context_processor
@app.context_processor
def context_processor():
    # 如果用户已经登录
    if hasattr(g,"user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80)



