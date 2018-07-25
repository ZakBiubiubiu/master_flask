# coding=utf-8

from flask import Flask, render_template, redirect, url_for, Blueprint, abort, request
from sqlalchemy import func
from webapp.models import *
from webapp.forms import *
from os import path
import datetime
from webapp.exts import admin_permission
from flask_principal import Permission, UserNeed
from flask_login import login_required, current_user, fresh_login_required
from webapp.exts import cache
import locale


blog_blueprint = Blueprint('blog', __name__, template_folder='templates')


@cache.cached(timeout=7200, key_prefix='sidebar_data')
def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label('total')).join(
        tags).group_by(Tag).order_by(db.text('total DESC')).limit(5).all()

    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
@cache.cached(timeout=60)  # timeouts设置缓存失效时间
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template('blog/home.html', posts=posts, recent=recent, top_tags=top_tags)


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))  # frozenset:不可变集合
    # lang = locale.getlocale()
    # print(lang)
    return (path + args).encode('utf-8')


@blog_blueprint.route('/post/<int:post_id>', methods=('GET', 'POST'))
@cache.cached(timeout=600, key_prefix=make_cache_key)
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.text.data
        new_comment.post_id = post_id
        new_comment.date = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('.post', post_id=post_id),)

    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('blog/post.html',post=post,tags=tags,comments=comments,recent=recent,top_tags=top_tags,form=form)


@blog_blueprint.route('/tag/<string:tag_name>')
@blog_blueprint.route('/tag/<string:tag_name>/<int:page>')
def tag(tag_name,page=1):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).paginate(page,10)
    recent, top_tags = sidebar_data()

    return render_template('blog/tag.html',tag=tag,posts=posts,recent=recent,top_tags=top_tags,tag_name=tag_name)


@blog_blueprint.route('/user/<string:username>')
@blog_blueprint.route('/user/<string:username>/<int:page>')
def user(username,page=1):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).paginate(page,10)
    recent, top_tags = sidebar_data()

    return render_template('blog/user.html', user=user,posts=posts,recent=recent,top_tags=top_tags,username=username)


# 新建post视图函数
@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        print('验证陈工')
        newpost = Post(form.title.data, form.text.data)
        newpost.author = User.query.filter_by(username=current_user.username).one()
        newpost.publish_date = datetime.datetime.now()
        db.session.add(newpost)
        db.session.commit()

        return redirect(url_for('blog.post', post_id=newpost.id))
    print('验证失败')
    print(current_user.username)
    return render_template('blog/new.html', form=form)


# 编辑视图函数
@blog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@fresh_login_required
def edit_post(id):

    post = Post.query.get_or_404(id)
    permission = Permission(UserNeed(post.author.id))
    # 设置访问本视图的权限

    if permission.can() or admin_permission.can():
        # 判断Identity是否有要求的permission
        form = PostForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()

            db.session.add(post)
            db.session.commit()

            return redirect(url_for('blog.post', post_id=post.id))

        form.text.data = post.text

        return render_template('blog/edit.html', form=form, post=post)

    abort(403)
