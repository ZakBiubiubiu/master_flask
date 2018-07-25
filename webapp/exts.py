from flask_bcrypt import Bcrypt
from flask_openid import OpenID
from flask import redirect, flash, url_for, session, render_template, Blueprint, Markup
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_restful import Api
from flask_celery import Celery
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache
from flask_assets import Environment, Bundle
from flask_admin import Admin
from flask_mail import Mail
from flask_youku import YouKu
from flask import request
from gzip import GzipFile
from io import BytesIO

bcrypt = Bcrypt()
oid = OpenID()
login_manager = LoginManager() # 初始化
principals = Principal()
rest_api = Api()
celery = Celery()  # 对flask-celery-helper进行实例化
debug_toolbar = DebugToolbarExtension()
cache = Cache()
admin = Admin()
mail = Mail()

# login_manger配置修改
login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = '请穿上马甲再上场'
login_manager.login_message_category = 'Info'

# principal配置,定义三种角色
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))


@login_manager.user_loader
def load_user(user_id):
    from webapp.models import User
    # return User.query.get(int(user_id))
    return User.query.get(user_id)


@oid.after_login
def create_or_login(resp):
    from webapp.models import User, db
    # 在函数内导入，避免循环导入，因为models.py也导入了bcrypt对象
    username = resp.fullname or resp.nickname or resp.email
    if not username:
        flash('Invalid Login. Please try again.', 'danger')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('blog.home'))


assets_env = Environment()

main_css = Bundle(
    'css/bootstrap.css',
    filters='cssmin',
    output='css/common.css'
)

main_js = Bundle(
    'js/jquery.js',
    'js/bootstrap.js',
    filters='jsmin',
    output='js/common.js'
)

youku = YouKu()


class Gzip(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.after_request(self.after_request)

    def after_request(self, response):
        encoding = request.headers.get('Accept-Encoding', '')

        if 'gzip' not in encoding or not response.status_code in (200, 201):
            return response

        response.direct_passthrough = False

        contents = BytesIO()

        with GzipFile( mode='wb', compresslevel=5, fileobj=contents) as gzip_file:
            gzip_file.write(response.get_data())

        response.set_data(bytes(contents.getvalue()))

        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = response.content_length

        return response

flask_gzip = Gzip()
