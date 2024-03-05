import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  FLASK_ADMIN = os.environ.get("FLASKADMIN")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SSL_REDIRECT = False

  AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
  AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
  AWS_REGION_NAME = os.environ.get("AWS_REGION_NAME")
  S3_BUCKET = os.environ.get("S3_BUCKET")
  S3_BUCKET_SOUND_TEST = os.environ.get("S3_BUCKET_SOUND_TEST")
  S3_KEY_SOUND_TEST = os.environ.get("S3_KEY_SOUND_TEST")
  MAX_SAMPLES = os.environ.get("MAX_SAMPLES")


  FIREBASE_CONFIG = {
    "apiKey": os.environ.get("FIREBASE_API_KEY"),
    "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.environ.get("FIREBASE_DATABASE_URL"),
    "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET")
  }

  LANGUAGES = ["pt", "en", "es"]

  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    if os.environ.get('DEV_DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL').replace('://', 'ql://', 1)
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('://', 'ql://', 1)
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'default': DevelopmentConfig
}