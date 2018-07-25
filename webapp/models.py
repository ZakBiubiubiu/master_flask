from webapp.exts import bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from flask_mongoengine import MongoEngine
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app
from webapp.exts import cache

db = SQLAlchemy()
tags = db.Table('post_tags',
                db.Column('post_id',db.Integer,db.ForeignKey('post.id'),primary_key=True),
                db.Column('tag_id',db.Integer, db.ForeignKey('tag.id'), primary_key=True))

roles = db.Table(
    'role_users', db.Column('user_id',db.Integer,db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id',db.Integer, db.ForeignKey('role.id'), primary_key=True))


class User(db.Model):
    """docstring for User"""
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    posts = db.relationship('Post',back_populates='author',lazy='dynamic')
    roles = db.relationship('Role', secondary=roles, back_populates='users',lazy='dynamic')

    def __init__(self, username,**kwargs):
        self.username = username
        default = Role.query.filter_by(name='default').one()
        self.roles.append(default)

    def __repr__(self):
        return '<User %s>' % self.username

    # 设置密码
    # self为
    # password为RegisterForm传入的password.data。
    # 不需要返回值
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    # 密码验证
    # self.password 为 LoginForm传入的user.password
    # password 为 LoginForm 传入的 password.data
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        return True

    def is_anonymous(self):
        if isinstance(self,AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        #  return str(self.id)
        return self.id

    @staticmethod
    @cache.memoize(60)  # 设置过期时间
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


class Post(db.Model):
    """docstring for Post"""
    __tablename__='post'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    publish_date = db.Column(db.DATETIME)
    comments = db.relationship('Comment', back_populates='post',lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User',back_populates='posts')
    tags = db.relationship('Tag', secondary=tags, back_populates='posts',lazy='dynamic')

    def __init__(self, title, text, **kwargs):
        self.title = title
        self.text = text

    def __repr__(self):
        return '<Post %s>' % self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100))
    text = db.Column(db.Text)
    date = db.Column(db.DATETIME)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    def __init__(self,name=None,text=None,**kwargs):
        self.name=name
        self.text=text

    def __repr__(self):
        return '<Comment %s>' % self.name


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    posts = db.relationship('Post', secondary=tags, back_populates='tags',lazy='dynamic')

    def __init__(self, title,**kwargs):
        self.title=title

    def __repr__(self):
        return '<Tag %s>' % self.title


class Role(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(80),unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', secondary=roles, back_populates='roles', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %s>' % self.name


class Reminder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String())
    text = db.Column(db.Text())

    def __repr__(self):
        return '<Reminder %s>' % self.text[:20]




# mongo = MongoEngine()
# available_roles = ('admin','poster','default')
#
#
# class User(mongo.Document):
#     username = mongo.StringField(required=True)
#     password = mongo.StringField(required=True)
#     roles = mongo.ListField(mongo.StringField(choices=available_roles))
#
#     def __repr__(self):
#         return '<User %s>' % self.username
#
#     # 设置密码
#     # self为
#     # password为RegisterForm传入的password.data。
#     # 不需要返回值
#     def set_password(self, password):
#         self.password = bcrypt.generate_password_hash(password)
#
#     # 密码验证
#     # self.password 为 LoginForm传入的user.password
#     # password 为 LoginForm 传入的 password.data
#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password, password)
#
#     def is_authenticated(self):
#         if isinstance(self, AnonymousUserMixin):
#             return False
#         else:
#             return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         if isinstance(self, AnonymousUserMixin):
#             return True
#         else:
#             return False
#
#     def get_id(self):
#         return str(self.id)
#
#
# class Comment(mongo.EmbeddedDocument):
#     name = mongo.StringField(required=True)
#     text = mongo.StringField(required=True)
#     date = mongo.DateTimeField(default=datetime.datetime.now())
#
#     def __repr__(self):
#         return '<Comment %s>' % self.text[:15]
#
#
# class Post(mongo.Document):
#     title = mongo.StringField(required=True)
#     publish_date = mongo.DateTimeField(default=datetime.datetime.now())
#     user = mongo.ReferenceField(User)
#     comments = mongo.ListField(mongo.EmbeddedDocumentField(Comment))
#     tags = mongo.ListField(mongo.StringField())
#
#     meta = {'allow_inheritance': True}
#
#     def __repr__(self):
#         return '<Post {%s}' % self.title
#
#
# class BlogPost(Post):
#     text = mongo.StringField(required = True)
#
#     @property
#     def type(self):
#         return 'blog'
#
#
# class VideoPost(Post):
#     url = mongo.StringField(required=True)
#
#     @property
#     def type(self):
#         return 'video'
#
#
# class ImagePost(Post):
#     image_url = mongo.StringField(required=True)
#
#     @property
#     def type(self):
#         return 'image'
#
#
# class QuotePost(Post):
#     quote = mongo.StringField(required=True)
#     author = mongo.StringField(required=True)
#
#     @property
#     def type(self):
#         return 'quote'
#
