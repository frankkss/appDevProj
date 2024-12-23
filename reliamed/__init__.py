from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_migrate import Migrate
import os

app = Flask(__name__)
# Use DATABASE_URL from environment variables if available, otherwise fallback to local sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://uaqs6a9msldu91:p7ed62fe468cd91eb4450559b4782c731ec92a71dff37b1c54f29fd1091ff934a@cfls9h51f4i86c.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d60vupoa4r6o39'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'connect_args': {'timeout': 20}}  # Add this line

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = "info"

migrate = Migrate(app, db)

from reliamed import routes