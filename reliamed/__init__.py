from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_migrate import Migrate
import os

app = Flask(__name__)

# Use DATABASE_URL from environment variables if available, otherwise fallback to local sqlite
database_url = os.getenv('DATABASE_URL', 'sqlite:///reliamed.db')

# Fix for Render PostgreSQL URL (postgres:// -> postgresql://)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Only add timeout for SQLite
if database_url.startswith('sqlite'):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'timeout': 20}}

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = "info"

migrate = Migrate(app, db)

from reliamed import routes