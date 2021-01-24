from flask import Blueprint, redirect, render_template, url_for
from appmain.user.forms import RegistrationForm, LoginForm

user = Blueprint('user', __name__)

@user.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print("Account created successfully.")
        return redirect(url_for('main.home'))
    else:
        return render_template('register.html', title = 'Register', form = form)

@user.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@abc.com' and form.password.data == 'password':
            print('You have been logged in!')
            return redirect(url_for('main.home'))
        else:
            print('Login unsuccessful. Please check username and passoword')
            return render_template('books.html', title='Login', form=form)
    else:
        return render_template('books.html', title = 'Login', form = form)
