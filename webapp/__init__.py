# coding=utf-8

from flask import Flask,  redirect,url_for
from webapp.controllers.blog import blog_blueprint
from webapp.controllers.main import main_blueprint
from webapp.controllers.admin import ModelView, CustomView, PostView, CustomModelView, CustomFileAdmin
from webapp.config import DevConfig
from webapp.exts import bcrypt, oid, login_manager, principals, rest_api, celery, debug_toolbar, cache, assets_env, main_css, main_js,admin, mail, youku, flask_gzip
from webapp.models import db, Reminder, User, Role, Post, Comment, Tag
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user
from webapp.controllers.rest.post import PostApi
from webapp.controllers.rest.auth import AuthApi
from webapp.controllers.rest.comment import CommentApi
from sqlalchemy import event
from .tasks import on_reminder_save
import os.path as op


# app工厂形式: 将app的实例化放置于函数中，并进行了配置文件的设置，db和bcrypt与aoo的绑定，蓝图的注册。
def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    # db从app的config中获取URI
    event.listen(Reminder, 'after_insert', on_reminder_save)
    # SQLAlchemy在Reminder上注册回调函数，当after_insert发生后，执行on_reminder_save
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    celery.init_app(app)
    debug_toolbar.init_app(app)
    cache.init_app(app)
    admin.init_app(app)

    assets_env.init_app(app)
    assets_env.register('main_js', main_js)
    assets_env.register('main_css', main_css)

    rest_api.add_resource(PostApi, '/api/post', '/api/post/<int:post_id>', endpoint='post')
    rest_api.add_resource(AuthApi, '/api/auth', endpoint='auth')
    rest_api.add_resource(CommentApi, '/api/comment', '/api/post/<int:post_id>/comment', endpoint='comment')
    # add_resource(self, resource, *urls, **kwargs),api管理的是resource，将resource和url绑定
    # 绑定app后添加出错？
    rest_api.init_app(app)
    mail.init_app(app)
    youku.init_app(app)
    # flask_gzip.init_app(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # 设置identity的user对象？
        identity.user = current_user  # 注释掉好像也没影响

        # 将user的权限加入当前的Identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
            # 基于id的权限
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))
                # 基于角色的权限

    app.register_blueprint(blog_blueprint, url_prefix='/blog')
    app.register_blueprint(main_blueprint)

    admin.add_view(CustomView(name='Custom'))
    models = [User, Role, Comment, Tag, Reminder]

    for model in models:
        admin.add_view(CustomModelView(model, db.session, category='models'))  # 同一个category的视图会放在同一个下拉菜单

    admin.add_view(PostView(Post, db.session, name='PostManager'))
    admin.add_view(CustomFileAdmin(op.join(op.dirname(__file__), 'static'), '/static/', name='Static Files'))
    # @app.route('/')
    # def index():
    #     return redirect(url_for('blog.home'))

    return app
