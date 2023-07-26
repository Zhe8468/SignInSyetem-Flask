from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from exts import db
from models import UserModel,SignInModel,ContactModel,CourseModel
import datetime

bp = Blueprint("admin",__name__,url_prefix="/admin")
is_admin_login = False # 标记管理员是否登录

@bp.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template("admin_login.html")
    else:
        account = request.form.get("account")
        password = request.form.get("password")
        if account == "xueshengzhijia" and password=="xszjhtgl2022":
            global is_admin_login
            is_admin_login = True
            flash("登录成功！")
            return redirect(url_for("admin.students"))
        else:
            flash("账号或密码错误")
            return redirect(url_for("admin.login"))

@bp.route("/students",methods=["GET","POST"])
def students():
    if is_admin_login:
        stus = UserModel.query.all()
        return render_template("admin_students.html",stus=stus)
    else:
        return redirect(url_for("admin.login"))


@bp.route("/signins",methods=["GET","POST"])
def signins():
    if is_admin_login:
        signins = SignInModel.query.order_by(SignInModel.create_time.desc()).all()
        return render_template("admin_signins.html",signins=signins)
    else:
        return redirect(url_for("admin.login"))

@bp.route("/contact_board",methods=["GET","POST"])
def contact_board():
    if is_admin_login:
        contacts = ContactModel.query.order_by(ContactModel.create_time.desc()).all()
        return render_template("admin_contact_board.html",contacts=contacts)
    else:
        return redirect(url_for("admin.login"))
@bp.route("/class_begin",methods=["POST"])
def class_begin():
    if is_admin_login:
        today = datetime.date.today()
        today = str(today)
        # 看一下今天是否已经上课了
        course = CourseModel.query.filter_by(create_time=today).all()
        if not course:
            # 添加课程记录
            course = CourseModel(create_time=today,course_name=request.form['course_name'])
            db.session.add(course)
            db.session.commit()
            # 初始化所有学生的签到状态
            stus = UserModel.query.all()
            for stu in stus:
                signin_model = SignInModel(create_time=today,course_name=request.form['course_name'],user_id=stu.id,state="未签到")
                db.session.add(signin_model)
                db.session.commit()
            # 成功！
            flash("初始化成功！您可以开始上课！")
            return redirect(url_for("admin.signins"))
        else:
            flash("今天已经上课过了！不要重复上课")
            return redirect(url_for("admin.signins"))
    else:
        return redirect(url_for("admin.login"))

@bp.route("/logout")
def logout():
    global is_admin_login
    is_admin_login = False
    # 重定向
    return redirect(url_for("admin.login"))
