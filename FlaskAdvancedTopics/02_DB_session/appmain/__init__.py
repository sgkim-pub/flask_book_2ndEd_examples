from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

app.config['SECRET_KEY'] = 'af082ad67d6e61bf2baedc2d32af1309'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskweb:your_password@localhost:3306/flaskdb'

db = SQLAlchemy(app)

from appmain.DBSession.routes import sess

app.register_blueprint(sess)

from appmain.DBSession.utils import SQLAlchemySessionInterface

app.session_interface = SQLAlchemySessionInterface()
