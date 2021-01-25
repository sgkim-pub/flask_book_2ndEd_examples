from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskweb:your_password@localhost:3306/flaskdb'

db = SQLAlchemy(app)

class Bookinfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookTitle = db.Column(db.String(30), unique=True, nullable=False)
    isbn = db.Column(db.String(60), unique=True, nullable=False)
    pages = db.Column(db.Integer, unique=False, nullable=False)

db.create_all()

if not db.session.query(Bookinfo).all():
    books = []

    books.append(Bookinfo(bookTitle = '논어', isbn = '9788952204639', pages = 374))
    books.append(Bookinfo(bookTitle = '맹자-상', isbn = '9788982641237', pages = 432))
    books.append(Bookinfo(bookTitle = '맹자-하', isbn = '9788982641244', pages = 464))
    books.append(Bookinfo(bookTitle = '대학', isbn = '9788982644054', pages = 416))

    for book in books:
        db.session.add(book)

    db.session.commit()
else:
    pass

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/books")
def showBooks():
    bookList = db.session.query(Bookinfo).all()
    return render_template("books.html", books = bookList)

if __name__ == '__main__':
    app.run("127.0.0.1", 5000)
