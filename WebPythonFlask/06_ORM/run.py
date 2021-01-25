from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskweb:your_password@localhost:3306/flaskdb'

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)

db.create_all()

member1 = Member(username = 'elsa', email = 'elsa@abc.com', password = 'aB3xTup8')
member2 = Member(username = 'anna', email = 'anna@abc.com', password = '9srQcm52')

db.session.add(member1)
db.session.add(member2)
db.session.commit()
