from flask import Blueprint, render_template,request,redirect,url_for,jsonify,session,flash
from exts import mail,db
from flask_mail import Message
from models import EmailCpatchaModel,UserModel #在这里也能顺带被app.py识别到 因为app.py导入了这个文件
import string,random,datetime #用于生成验证码
from .forms import RegisterForm,LoginForm # 表单验证
from werkzeug.security import generate_password_hash,check_password_hash# md5加密

bp = Blueprint("users",__name__,url_prefix="/users")

@bp.route("/login",methods=['POST','GET'])
def login():
    # 如果是GET请求 直接返回页面
    if request.method == 'GET':
        return render_template("login.html")
    # 如果是POST请求 进行表单验证
    form = LoginForm(request.form)
    # 如果验证通过
    if form.validate():
        # 获取数据
        email = form.email.data
        password = form.password.data
        print(generate_password_hash(password))
        # 根据邮箱结果进行查询
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model and check_password_hash(user_model.password,password):
            # 保存登录状态
            session['user_id'] = user_model.id
            # 登录成功 跳转到后台
            return redirect(url_for("signin.tables"))
        else:
            flash("邮箱或密码错误！")
            return redirect(url_for("users.login"))
    else:
        flash("邮箱或密码格式错误！")
        # 登录失败 重新刷新
        return redirect(url_for("users.login"))




@bp.route("/register",methods=["GET","POST"])
def register():
    # 如果是GET请求，那么返回注册页面
    if request.method == "GET":
        return render_template("register.html")
    # 如果是POST请求，那么开始验证
    # 通过request获取前端传递的form当中的内容
    form = RegisterForm(request.form)
    # 如果验证通过
    if form.validate():
        # 获取数据
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # 对密码进行md5加密后再存储
        password = generate_password_hash(password)
        # 更新数据库 创建用户
        user_model = UserModel(email=email,username=username,password=password)
        db.session.add(user_model)
        db.session.commit()
        # 注册成功 重定向
        return redirect(url_for("users.login"))
    else:
        # 生成错误信息 用于flash展示
        errors = ""
        for i in form.errors.values():
            for j in i:
                errors += j
                errors += " "
            errors += '\n'
        errors += "请重新输入"
        flash(errors)
        # 验证失败 重新跳转
        return redirect(url_for("users.register"))



@bp.route("/captcha",methods=['POST'])
def get_captcha():
    # 使用POST请求获取邮箱
    email = request.form.get("email")
    # 如果没有传递邮箱 那么不往下继续
    if not email:
        # 400 客户端错误！
        return jsonify({"code":400})
    # 验证码字符集
    letters = string.ascii_letters+string.digits
    # 生成验证码
    captcha = "".join(random.sample(letters,6))
    # 初始化邮件对象
    message = Message(
        subject="学生之家社团签到系统账号注册",
        recipients=[email],
        body="【学生之家社团签到系统】同学你好！您的注册验证码是{}，请不要告诉他人！".format(captcha)
    )
    # 发送邮件对象
    mail.send(message)
    # 查询是否存在该邮箱对应的验证码
    captcha_model = EmailCpatchaModel.query.filter_by(email=email).first()
    if captcha_model:
        # 更新验证码
        captcha_model.captcha = captcha
        # 更新时间
        captcha_model.create_time = datetime.datetime.now()
        # 更新数据库
        db.session.commit()
    else:
        # 如果没有，则创建数据
        captcha_model = EmailCpatchaModel(email=email,captcha=captcha)
        db.session.add(captcha_model)
        db.session.commit()
    print("captcha: {}".format(captcha))
    return jsonify({"code":200})

@bp.route("/logout")
def logout():
    # 清除session中的所有数据
    session.clear()
    # 重定向
    return redirect(url_for("users.login"))