from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from webapp import create_app
import os
from webapp.models import User, Post, Tag, tags, Comment, db, roles, Role
from flask_migrate import Migrate, MigrateCommand
import datetime
import random

# bash命令-设置环境变量：export WEBAPP_ENV='dev'
# bash命令-查看环境变量：echo $WEBAPP_ENV
# bash命令-抛弃环境变量：unset $WEBAPP_ENV
env = os.environ.get('WEBAPP-ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('server',Server())
manager.add_command('db',MigrateCommand)


# 创建一个python CLI, return：默认导入的模块 return type:dict
@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment, tags=tags, Tag=Tag,
                roles=roles, Role=Role)


@manager.command
def setup_db():
    db.create_all()

    # 创建管理员角色
    admin_role = Role('admin')
    admin_role.description = 'admin'
    db.session.add(admin_role)
    # 创建默认角色
    default_role = Role('default')
    default_role.description = 'default'
    db.session.add(default_role)

    # 创建管理员用户信息
    admin = User('admin')
    admin.set_password('password')
    admin.roles.append(admin_role)
    admin.roles.append(default_role)
    db.session.add(admin)

    tag_one = Tag('Python')
    tag_two = Tag('Flask')
    tag_three = Tag('SQLAlchemy')
    tag_four = Tag('Jinja')
    tag_list = [tag_one, tag_two, tag_three, tag_four]

    s = 'Body text'

    for i in range(100):
        new_post = Post('Post %s' %i, s)
        new_post.user = admin
        new_post.publish_date = datetime.datetime.now()
        new_post.tags = random.sample(tag_list, random.randint(1,3))

        db.session.add(new_post)

    db.session.commit()


manager.add_command('show-urls',ShowUrls())
# 列出所有路由和URL
manager.add_command('clean', Clean())
# 清除.pyc .pyo文件

if __name__ == '__main__':
    manager.run()
