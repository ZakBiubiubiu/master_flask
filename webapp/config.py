# coding=utf-8


class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    DIALECT = 'mysql'
    DRIVER = 'mysqlconnector'
    USERNAME = 'root'
    PASSWORD = 'password'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'master_db'
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '123QWE123QWEODFNGRJNFGER'
    EXPLAIN_TEMPLATE_LOADING = True

