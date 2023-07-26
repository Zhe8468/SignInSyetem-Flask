import wtforms
from wtforms.validators import length,email,EqualTo,InputRequired
from models import EmailCpatchaModel,UserModel


class LoginForm(wtforms.Form):
    '''
    登录表单验证
    '''
    email = wtforms.StringField(validators=[email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[length(min=6,message="密码必须大于6个字符")])

class RegisterForm(wtforms.Form):
    '''
    注册表单验证
    '''
    username = wtforms.StringField(validators=[length(min=3,max=20,message="用户名必须大于3个字符")])
    email = wtforms.StringField(validators=[email(message="邮箱格式不正确！")])
    captcha = wtforms.StringField(validators=[length(min=6,max=6,message="验证码为6个字符")])
    password = wtforms.StringField(validators=[length(min=6,message="密码必须大于6个字符")])
    confirm_password = wtforms.StringField(validators=[EqualTo("password","两次输入的密码不一致")])


    # 重写判断函数 要验证哪个字段 就用哪个字段命名
    # 格式为：validate_字段名
    def validate_captcha(self, field):
        '''
        验证码正确性判断
        '''
        # 获取用户输入的验证码
        captcha = field.data
        # 获取邮箱
        email = self.email.data
        # 根据邮箱查询数据库当中生成的验证码
        captcha_model = EmailCpatchaModel.query.filter_by(email=email).first()
        # 转换为小写再判断
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():
            raise wtforms.ValidationError("邮箱验证码错误！")

    def validate_email(self,field):
        '''
        邮箱是否注册过判断
        '''
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise wtforms.ValidationError("邮箱已经存在！")

class ContactForm(wtforms.Form):
    '''
    留言验证
    '''
    content = wtforms.StringField(validators=[InputRequired(message="你没有输入内容")])


class SettingsForm(wtforms.Form):
    '''
    个人设置表单验证
    '''
    password = wtforms.StringField(validators=[length(min=6, message="密码必须大于6个字符")])
    confirm_password = wtforms.StringField(validators=[EqualTo("password", "两次输入的密码不一致")])

