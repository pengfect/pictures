from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment


app = Flask(__name__)
app.config.from_pyfile('./app.conf')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
Bootstrap(app)
moment = Moment(app)
from pictures import views
