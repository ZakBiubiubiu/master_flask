from flask_script import Manager, Server
from webapp import create_app
import os
from webapp.models import User, Post, Tag, tags, Comment
from webapp.exts import db
from flask_migrate import Migrate, MigrateCommand

env = os.environ.get('WEBAPP-ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('server',Server())
manager.add_command('db',MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post,Comment=Comment,tags=tags, Tag=Tag)


if __name__ == '__main__':
    manager.run()
