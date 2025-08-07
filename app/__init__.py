import sys
print("Starting app initialization...", file=sys.stderr)
from flask import Flask, request, session
print("Flask imported", file=sys.stderr)
from config import Config
print("Config imported", file=sys.stderr)
from flask_sqlalchemy import SQLAlchemy
print("SQLAlchemy imported", file=sys.stderr)
from flask_migrate import Migrate
print("Migrate imported", file=sys.stderr)
from flask_login import LoginManager
print("LoginManager imported", file=sys.stderr)
from flask_babel import Babel, lazy_gettext as _l
print("Babel imported", file=sys.stderr)

def get_locale():
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

print("Creating Flask app...", file=sys.stderr)
app = Flask(__name__, template_folder='../templates', static_folder='../static')
print("Flask app created", file=sys.stderr)
app.config.from_object(Config)
print("Config loaded", file=sys.stderr)
db = SQLAlchemy(app)
print("SQLAlchemy initialized", file=sys.stderr)
migrate = Migrate(app, db)
print("Migrate initialized", file=sys.stderr)
login = LoginManager(app)
print("LoginManager initialized", file=sys.stderr)
babel = Babel(app, locale_selector=get_locale)
print("Babel initialized", file=sys.stderr)

print("Importing routes and models...", file=sys.stderr)
from app import routes, models
print("Routes and models imported", file=sys.stderr)
print("App initialization complete.", file=sys.stderr)
