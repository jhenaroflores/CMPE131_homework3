from flask import Flask
from flask_login import LoginManager
from .models import db, User

# creates flask app instance
myapp_obj = Flask(__name__)


myapp_obj.config['SECRET_KEY'] = 'your_secret_key_here' # secret key for securely  signing session
myapp_obj.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # sets up sqlite database
myapp_obj.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turns off mod tracking

db.init_app(myapp_obj)

login_manager = LoginManager()
login_manager.init_app(myapp_obj)
login_manager.login_view = 'login'  # Redirect here if @login_required fails

# tells flask-login how to load a user from the database by id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# imports routes
from app import routes
