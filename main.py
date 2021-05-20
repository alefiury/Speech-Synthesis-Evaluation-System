import os
from flask_migrate import Migrate, upgrade
from app import create_app, db

from app.main import views

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)