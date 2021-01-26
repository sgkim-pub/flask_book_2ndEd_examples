from flask import Flask, render_template, redirect, url_for, Blueprint

posts = [
    {
        'author': 'Elsa',
        'title': 'Blog posting 1',
        'content': 'The first posting',
        'datePosted': 'September 6, 2020'
    },
    {
        'author': 'Anna',
        'title': 'Blog posting 2',
        'content': 'The second posting',
        'datePosted': 'September 7, 2020'
    }
]

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template("home.html", posts = posts)

@main.route("/about")
def about():
    return render_template("about.html", title = 'About')
