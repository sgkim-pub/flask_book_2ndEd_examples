from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '97f802e4498c0ce2b8db61eec69268be'

from appmain.user.routes import user
from appmain.routes import main

app.register_blueprint(user)
app.register_blueprint(main)
