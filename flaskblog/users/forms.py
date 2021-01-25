from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 30)])
    email = StringField('Email', validators = [DataRequired(), email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username taken')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email taken')


class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min = 2, max = 30)])
    email = StringField('Email', validators = [DataRequired(), email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Username taken')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email taken')
    
class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), email()])
    submit = SubmitField('Request Password Reset')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user is None:
                raise ValidationError('No account with that email.  Please register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')