from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Use DATABASE_URL from environment variables if available, otherwise fallback to local sqlite
database_url = os.getenv('DATABASE_URL', 'sqlite:///reliamed.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SECRET_KEY'] = 'ef3cc4b50e1ffa8bbffa39dd'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from reliamed import routes