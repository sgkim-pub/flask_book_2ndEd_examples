from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Elsa',
        'title': 'Blog posting 1',
        'content': 'The first posting',
        'datePosted': 'August 16, 2020'
    },
    {
        'author': 'Anna',
        'title': 'Blog posting 2',
        'content': 'The second posting',
        'datePosted': 'August 17, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = 'About')

if __name__ == "__main__":
    app.run("127.0.0.1", 5000)