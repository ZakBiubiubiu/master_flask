# coding=utf-8
import datetime
from celery.schedules import crontab
import tempfile


class Config(object):
    SECRET_KEY = '123QWE123QWEODFNGRJNFGER'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_RECORD_QUERIES = True  # debug_toolbar支持SQLAlchemy查询记录
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@127.0.0.1:3306/master_db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///master_db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    EXPLAIN_TEMPLATE_LOADING = True
    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_RESULT_BACKEND = 'rpc://'

    CACHE_TYPE = 'simple'
    # CACHE_TYPE = 'redis'  # 要安装redis
    # CACHE_REDIS_HOST = 'localhost'
    # CACHE_REDIS_PORT = '6379'
    # CACHE_REDIS_PASSWORD = 'password'
    # CACHE_REDIS_DB = '0'
    # DEBUG_TB_PROFILER_ENABLED = True

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = 'username'
    MAIL_PASSWORD = 'password'

    ASSETS_DEBUG = True

    CELERYBEAT_SCHEDULE = {
        'log-every-30-seconds':{
            'task': 'webapp.tasks.log',
            'schedule': datetime.timedelta(seconds=5),
            'args': ('Message',)
        }
    }
    CELERYBEAT_SCHEDULE = {
        'weekly-digest': {
            'task': 'webapp.tasks.digest',
            'schedule': crontab(day_of_week=6, hour='10')
        }
    }


    MONGODB_SETTING = {
        'db': 'local',
        'host': 'localhost',
        'port': 27017
    }


class TestConfig(Config):
    db_file = tempfile.NamedTemporaryFile()

    DEBUG = True
    DEBUG_TB_ENABLED = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_file.name + '.db'

    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False

    CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    CELERY_RESULT_BACKEND = 'rpc://'

    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USERNAME = '404846497@qq.com'
    MAIL_PASSWORD = 'ade17605085910'

