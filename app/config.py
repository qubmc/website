import logging
import os

# DEBUG can only be set to True in a
# development environment for security reasons
DEBUG = True

# Secret key for generating tokens
SECRET_KEY = 'keep the bad guys out'

# Flask-Admin credentials
ADMIN_CREDENTIALS = ('admin', 'pa$$word')

# Database choice
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
CSRF_ENABLED = True

# Flask-Mail settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'webmaster.qubmc@gmail.com'
MAIL_PASSWORD = 'keepoutthebadguys'
MAIL_DEFAULT_SENDER = '"Webmaster @ QUBMC" <noreply@qubmc.co.uk>'
ADMINS = ['webmaster.qubmc@gmail.com']

# Flask-User settings
USER_APP_NAME = 'QUBMC'  # Used by email templates

# Number of times a password is hashed
BCRYPT_LOG_ROUNDS = 12

# Image Uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/img/uploads')
MAX_CONTENT_PATH = (16 * 1024 * 1024)
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

LOG_LEVEL = logging.DEBUG
LOG_FILENAME = 'activity.log'