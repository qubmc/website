from flask import Flask
from flask_user import SQLAlchemyAdapter, UserManager

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('app.config')

# Setup the database
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the mail server
from flask_mail import Mail
mail = Mail(app)

# Setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
#toolbar = DebugToolbarExtension(app)

# Setup the password crypting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import the views
from app import views

# Setup the user login process
from flask_login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'

db_adapter = SQLAlchemyAdapter(db, User)
user_manager = UserManager(db_adapter, app)


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()

from app import admin

