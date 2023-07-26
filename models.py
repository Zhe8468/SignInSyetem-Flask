from exts import db
import datetime

class EmailCpatchaModel(db.Model):
    '''
    邮箱验证码ORM
    '''
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    captcha = db.Column(db.String(10),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.datetime.now)

class UserModel(db.Model):
    '''
    用户ORM
    '''
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(300),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.datetime.now)

class SignInModel(db.Model):
    '''
    用户签到ORM
    '''
    __tablename__ = "signin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.String(100),nullable=False)
    course_name = db.Column(db.String(200),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("UserModel",backref="signins")
    state = db.Column(db.String(50), nullable=False)

class CourseModel(db.Model):
    '''
    课程ORM
    '''
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.String(100),nullable=False)
    course_name = db.Column(db.String(200), nullable=False)

class ContactModel(db.Model):
    '''
    用户留言ORM
    '''
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("UserModel",backref="contacts")
    content = db.Column(db.Text, nullable=False)


