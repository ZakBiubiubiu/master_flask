from flask import Blueprint, url_for, redirect, flash, render_template,session
from webapp.forms import LoginForm, RegisterForm, OpenIdForm
from webapp.models import User, db
from webapp.exts import oid
from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed, current_app

main_blueprint = Blueprint('main', __name__, template_folder='templates')


@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    openid_form = OpenIdForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user, remember=True)
        # login_user(user, remember=form.remember.data)
        # 记住用户
        # 将验证成功的用户对象放入session当中。
        identity_changed.send(current_app._get_current_object(),identity=Identity(user.id))

        flash('你已经穿好衣服可以见人了.', category='success')
        # flask.flash(message, category='message')
        # 可为信息设置类别，方便在取出时进行筛选等。
        return redirect(url_for('blog.home'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category='danger')

    return render_template('main/login.html', form=form, openid_form=openid_form)


@main_blueprint.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    #删除principal存在session中的数据
    for key in ('identity.name','identity.auth_type'):
        session.pop(key,None)
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    flash('你已经脱去马甲,请不要裸奔', category='success')
    return redirect(url_for('blog.home'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
@oid.loginhandler
def register():
    form = RegisterForm()
    openid_form = OpenIdForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )
    if form.validate_on_submit():
        new_user = User(form.username.data)  # 建立User实例
        new_user.set_password(form.password.data)  # 设置密码

        db.session.add(new_user)
        db.session.commit()

        flash(
            '你的马甲已经缝制成功，请登台。', category='success'
        )
        return redirect(url_for('.login'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category='danger')

    return render_template('main/register.html', form=form, openid_form=openid_form)
