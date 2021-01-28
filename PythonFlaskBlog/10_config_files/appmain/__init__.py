from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_mail import Mail

from appmain.config import Config

app = Flask(__name__)

cfg = Config()

app.config['SECRET_KEY'] = cfg.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + \
                                        cfg.DB_USERNAME + \
                                        ':' + \
                                        cfg.DB_PASSWORD + \
                                        '@localhost:3306/flaskdb'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = cfg.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = cfg.MAIL_PASSWORD

mail = Mail(app)

db = SQLAlchemy(app)

loginManager = LoginManager(app)
#loginManager.login_view = 'login'

bcrypt = Bcrypt(app)

from appmain.user.routes import user
from appmain.post.routes import post
from appmain.routes import main

db.create_all()

app.register_blueprint(user)
app.register_blueprint(post)
app.register_blueprint(main)
