import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY =                    os.environ.get('SECRET_KEY') or 'matkhau'
    SQLALCHEMY_COMMIT_ON_TEARDOWN=  True
    FLASK_MAIL_SUBJECT_PREFIX    =  "[Flasky]"
    FLASK_ADMIN                  =  os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG   =True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT   = 465
    MAIL_USE_TLS= False
    MAIL_USE_SSL= True
    MAIL_USERNAME= os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI=os.environ.get('DEV_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')

class TestConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir,'data-test.sqlite')

config = {
        'dev': DevConfig,
        'test': TestConfig,
        'production': ProductionConfig,
        'default': DevConfig
        }
    
    
