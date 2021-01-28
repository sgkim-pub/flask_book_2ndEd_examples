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

from appmain.user.forms import resetPWEmailForm, resetPWForm
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from appmain import mail

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

def sendPWResetEmail(userdata):
        userID = userdata.id
        userEmail = userdata.email

        secretKey = app.config['SECRET_KEY']
        ####    발급한 주소(에 포함된 token)는 30분(1,800초) 동안 유효하다.
        s = Serializer(secretKey, 1800)
        token = s.dumps(userID).decode('utf-8')

        msg = Message(subject = 'Page for password reset', sender = 'noreply@abc.com', recipients = [userEmail])
        pwResetPage = url_for('user.resetPassword', token = token, _external = True)
        msg.body = f'Your password reset page: {pwResetPage}'

        mail.send(msg)

        return 0

@user.route("/checkEmail", methods=['GET', 'POST'])
def checkEmail():
        form = resetPWEmailForm()
        if form.validate_on_submit():
                emailAddr = form.email.data
                userdata = Userdata.query.filter_by(email = emailAddr).first()
                if userdata:
                        sendPWResetEmail(userdata)
                        return redirect(url_for('main.home'))
                else:
                        print('No such user in DB.')
                        return redirect(url_for('user.checkEmail'))
        else:
                return render_template("pw_reset_email.html", title = 'Email for password reset', form = form)

@user.route("/resetPassword", methods=['GET', 'POST'])
def resetPassword():
        token = request.args.get('token', '', type = str)
        form = resetPWForm()
        if form.validate_on_submit():
                s = Serializer(app.config['SECRET_KEY'])
                userID = s.loads(token)
                hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = Userdata.query.filter_by(id = userID).first()
                user.password = hashedPassword
                db.session.commit()
                print('A password has been updated: ', user.username)
                return redirect(url_for('main.home'))
        else:
                return render_template("pw_reset.html", title = 'reset password', form = form)
