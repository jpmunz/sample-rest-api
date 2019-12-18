class Config(object):
    DEBUG = False
    ERROR_404_HELP = False
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/sample.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://:@localhost:6379/0"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
