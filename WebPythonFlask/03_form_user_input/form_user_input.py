from flask import Flask, render_template, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '97f802e4498c0ce2b8db61eec69268be'

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

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Account created successfully.")
        return redirect(url_for('home'))
    else:
        return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@abc.com' and form.password.data == 'password':
            print('You have logged in!')
            return redirect(url_for('home'))
        else:
            print('Login unsuccessful. Please check username and passoword')
    else:
        return render_template('books.html', title = 'Login', form = form)

if __name__ == "__main__":
    app.run("127.0.0.1", 5000)
