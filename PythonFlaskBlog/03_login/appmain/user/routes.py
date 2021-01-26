from flask import render_template, url_for, redirect, request, Blueprint
from appmain.user.forms import RegistrationForm
from appmain.user.models import Userdata
from appmain import app, db, bcrypt
from flask_login import current_user

from appmain.user.forms import LoginForm
from flask_login import login_user, logout_user

user = Blueprint('user', __name__)

@user.route("/register", methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('main.home'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = Userdata(username=form.username.data, email=form.email.data, password=hashedPassword)
                db.session.add(user)
                db.session.commit()
                # print(form.username.data, form.email.data, hashedPassword)
                print('An account has been created as %s' % form.username.data)
                return redirect(url_for('main.home'))
        return render_template("register.html", title='Register', form=form)

@user.route("/login", methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('main.home'))
        form = LoginForm()
        if form.validate_on_submit():
                user = Userdata.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user)
                        return redirect(url_for('main.home'))
                else:
                        print('Login Unsuccessful. Please check username or password')
        return render_template("login.html", title='Login', form=form)

@user.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('main.home'))
