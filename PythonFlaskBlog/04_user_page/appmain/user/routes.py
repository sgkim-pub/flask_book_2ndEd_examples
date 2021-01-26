from flask import render_template, url_for, redirect, request, Blueprint
from appmain.user.forms import RegistrationForm
from appmain.user.models import Userdata
from appmain import app, db, bcrypt
from flask_login import current_user

from appmain.user.forms import LoginForm
from flask_login import login_user, logout_user

import os
import secrets
from PIL import Image
from appmain.user.forms import UpdateAccountForm
from flask_login import login_required

from appmain.user.forms import DeleteAccountForm

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

def savePicture(form_picture):
        random_hex = secrets.token_hex(8)       #       8 bytes
        _, f_ext = os.path.splitext(form_picture.filename)      #       throw away filename = _
        pictureFn = random_hex + f_ext
        picturePath = os.path.join(app.root_path, 'static/profile_pics', pictureFn)

        pictureDir = os.path.join(app.root_path, 'static/profile_pics')
        os.makedirs(pictureDir, exist_ok = True)

        outputSize = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(outputSize)
        i.save(picturePath)

        return pictureFn

@user.route("/account", methods=['GET', 'POST'])
@login_required
def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                if form.picture.data:
                        pictureFile = savePicture(form.picture.data)
                        current_user.picture = pictureFile
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()
                print('An account has been updated!', current_user.username)
                return redirect(url_for('user.account'))
        elif request.method == 'GET':
                form.username.data = current_user.username
                form.email.data = current_user.email
                form.prevUsername.data = current_user.username
                form.prevEmail.data = current_user.email
        picture = url_for('static', filename='profile_pics/' + current_user.picture)
        return render_template("account.html", title='Account', image_file=picture, form=form)

@user.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('main.home'))

@user.route("/deleteAccount", methods=['GET', 'POST'])
@login_required
def deleteAccount():
        if current_user.is_authenticated:
                form = DeleteAccountForm()
                if form.validate_on_submit():
                        user = Userdata.query.filter_by(id=current_user.id).first()
                        if bcrypt.check_password_hash(user.password, form.password.data):
                                print('This account is deleted: ', user.username)
                                # db.session.delete(user)
                                # db.session.commit()
                                return redirect(url_for('user.logout'))
                        else:
                                return redirect(url_for('main.home'))
                elif request.method == 'POST':
                        user = {'username': current_user.username, 'useremail': current_user.email}
                else:
                        return redirect(url_for('main.home'))
                return render_template("deleteAccount.html", title='Delete account', user=user, form=form)
        else:
                return redirect(url_for('main.home'))