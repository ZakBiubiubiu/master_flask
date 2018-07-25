from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, widgets
from wtforms.validators import DataRequired, Length, EqualTo, URL
from webapp.models import User


# 评论表单
class CommentForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(max=255)])
    text = TextAreaField('Comment', validators=[DataRequired()])


# 登陆表单
class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    # remember = BooleanField('记住密码')

    # 改写Flaskform的validate方法
    def validate(self):
        check_validate = super(LoginForm, self).validate()
        # 使用父级方法，再进行扩展

        if not check_validate:
            return False

        # 检查用户名是否存在
        user = User.query.filter_by(username=self.username.data).one()

        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        # 检查密码是否正确
        if not user.check_password(self.password.data):
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        return True


# 注册表单
# 检测用户名是否存在
class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired(),Length(max=255)])
    password = PasswordField('Password', [DataRequired(),Length(min=8)])
    confirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])

    # recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if not check_validate:
            return False

        # 检查用户名是否存在
        user = User.query.filter_by(username=self.username.data).first()

        if user:
            self.username.errors.append(
                'User with that name already exists'
            )
            return False

        return True


# 发表文章表单
class PostForm(FlaskForm):
    title = StringField('Title', [DataRequired(), Length(max=255)])
    text = TextAreaField('Blog Content', [DataRequired()])


class OpenIdForm(FlaskForm):
    openid = StringField('OpenID URL', [DataRequired(), URL()])


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()