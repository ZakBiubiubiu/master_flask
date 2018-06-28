# coding=utf-8

from flask import Flask,  redirect,url_for
from webapp.controllers.blog import blog_blueprint
from webapp.config import DevConfig
from webapp.exts import db, bcrypt


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(blog_blueprint, url_prefix='/blog')


    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))

    return app

# if __name__ == '__main__':
#     app.run()