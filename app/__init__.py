from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)

bootstrap = Bootstrap(app)

CORS(app)

app.config.from_object(Config)

# set up db variables
db = SQLAlchemy(app) # takes in app instance to know which variables to use
migrate = Migrate(app, db)

# app variable for handling login functionality
login = LoginManager(app)

# when a page requires someone to b eloged in, specify the routhe they should be sent to when accessing that page anonymously
login.login_view = 'login'

from app import routes
