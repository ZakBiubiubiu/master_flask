from webapp.exts import db, bcrypt

tags = db.Table('post_tags',
                db.Column('post_id',db.Integer,db.ForeignKey('post.id'),primary_key=True),
                db.Column('tag_id',db.Integer, db.ForeignKey('tag.id'), primary_key=True))


class User(db.Model):
    """docstring for User"""
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    posts = db.relationship('Post',back_populates='author',lazy='dynamic')

    def __init__(self, username,**kwargs):
        self.username = username

    def __repr__(self):
        return '<User %s>' % self.username


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

    def __init__(self,title,text,**kwargs):
        self.title=title
        self.text=text

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
