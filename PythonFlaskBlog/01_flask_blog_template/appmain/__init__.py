from flask import Flask

#### 플라스크 윕 서버를 생성한다.
app = Flask(__name__)

app.config['SECRET_KEY'] = '97f802e4498c0ce2b8db61eec69268be'

from appmain.routes import main

app.register_blueprint(main)
