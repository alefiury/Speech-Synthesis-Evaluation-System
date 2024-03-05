import os

from flask import request, g
from flask_babel import Babel
from flask_migrate import Migrate, upgrade

from app.main import views
from app import create_app, db


def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES']) or app.config['LANGUAGES'][0]
    return g.lang_code


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
babel = Babel(app)
babel.init_app(app, locale_selector=get_locale)

# Migrate database
migrate = Migrate(app, db)