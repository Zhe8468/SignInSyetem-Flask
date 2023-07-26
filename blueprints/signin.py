from flask import Blueprint,render_template,request,session,flash,redirect,url_for
from exts import login_required,db
from models import SignInModel, ContactModel, UserModel
import datetime
from .forms import ContactForm, SettingsForm
from werkzeug.security import generate_password_hash

bp = Blueprint("signin",__name__,url_prefix="/signin")


@bp.route("/tables",methods=["GET","POST"])
@login_required
def tables():
    user_id = session['user_id']
    today = datetime.date.today()
    today = str(today)
    # 如果是GET请求 返回模板
    if request.method == 'GET':
        # 根据查询签到记录
        tb_content = SignInModel.query.filter_by(user_id=user_id).all()
        return render_template("tables.html",tb_content=tb_content)
    else:
        # 根据用户id判断签到状态
        res = SignInModel.query.filter_by(create_time=today,user_id=user_id).first()
        if not res:
            flash("老师还没有开始上课！")
            return redirect(url_for("signin.tables"))
        if res.state=="未签到":
            res.state = "已签到"
            db.session.add(res)
            db.session.commit()
            flash("签到成功！")
            # 根据查询签到记录
            tb_content = SignInModel.query.filter_by(user_id=user_id).all()
            return render_template("tables.html",tb_content=tb_content)
        else:
            flash("您已经签到过了！请不要重复签到")
            return redirect(url_for("signin.tables"))


@bp.route("/contact",methods=["GET","POST"])
@login_required
def contact():
    if request.method == 'GET':
        return render_template("contact.html")
    else:
        today = datetime.date.today()
        today = str(today)
        user_id = session['user_id']
        # 先检验
        res = ContactModel.query.filter_by(user_id=user_id,create_time=today).all()
        if not res:
            # 获取留言内容
            message = request.form.get("content")
            # 检验
            form = ContactForm(request.form)
            if form.validate():
                contact_model = ContactModel(create_time=today,user_id=session['user_id'],content=message)
                db.session.add(contact_model)
                db.session.commit()
                flash("发送成功！")
                return redirect(url_for("signin.contact"))
            else:
                # 检验不通过 显示提示信息
                errors = form.errors['content'][0]
                flash(errors)
                return redirect(url_for("signin.contact"))
        else:
            flash("你今天已经留言过了，请不要重复留言")
            return redirect(url_for("signin.contact"))


@bp.route("/settings",methods=["GET",'POST'])
@login_required
def settings():
    if request.method == 'GET':
        res = UserModel.query.filter_by(id=session['user_id']).first()
        info ={
            "user_id": session['user_id'],
            "email": res.email,
            "join_time": res.join_time,
            "username": res.username
        }
        return render_template("settings.html",**info)
    else:
        form = SettingsForm(request.form)
        # 读取两个密码
        if form.validate():
            # 查询原始密码
            res = UserModel.query.filter_by(id=session['user_id']).first()
            # 修改
            new_password = generate_password_hash(form.password.data)
            res.password = new_password
            db.session.add(res)
            db.session.commit()
            # 提示
            flash("密码修改成功！请记住您的密码，不要过多修改 :)")
            return redirect(url_for("signin.settings"))
        else:
            errors = ""
            for i in form.errors.values():
                for j in i:
                    errors += j
                    errors += " "
                errors += '\n'
            errors += "请重新输入"
            flash(errors)
            return redirect(url_for("signin.settings"))


