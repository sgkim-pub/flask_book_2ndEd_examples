from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'af082ad67d6e61bf2baedc2d32af1309'

from appmain.cookie.routes import cookie

app.register_blueprint(cookie)

from appmain.session.routes import sess

app.register_blueprint(sess)