import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sjdhfks_sdewkln'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}