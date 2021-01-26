from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from appmain.user.models import Userdata

from wtforms import HiddenField

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    picture = FileField('Profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Userdata.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different username.')

    def validate_email(self, email):
        email = Userdata.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already taken. Please choose a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    prevUsername = HiddenField('Previous username')
    email = StringField('Email', validators=[DataRequired(), Email()])
    prevEmail = HiddenField('Previous email')
    picture = FileField('Profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = Userdata.query.filter_by(username=username.data).first()

        if self.prevUsername.data == username.data:
            pass
        else:
            if user:
                raise ValidationError('That username is already taken. Please choose a different username.')
            else:
                pass

    def validate_email(self, email):
        user = Userdata.query.filter_by(email=email.data).first()

        if self.prevEmail.data == email.data:
            pass
        else:
            if user:
                raise ValidationError('That email is already taken. Please choose a different email address.')
            else:
                pass

class DeleteAccountForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')