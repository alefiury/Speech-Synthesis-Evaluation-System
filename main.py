import os

from flask import request, g
from flask_babel import Babel
from flask_migrate import Migrate

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


@app.cli.command("init-db")
def init_db():
    """Create SQL tables if they do not exist."""
    # Import models so SQLAlchemy metadata is fully registered.
    from app import models  # noqa: F401
    db.create_all()
