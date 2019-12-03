from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app) # takes in app instance to know which variables to use
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
CORS(app)



from app import routes
