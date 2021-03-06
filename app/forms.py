from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User
from wtforms import TextAreaField

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditprofileForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    about_me = TextAreaField('About me', validators = [Length(min = 0, max = 140)])
    # about_me = TextAreaField('About me', validators = [DataRequired()])
    # about_me = StringField('About me')
    submit = SubmitField('Submit')

class AddpostForm(FlaskForm):
    # username = StringField('Username', validators = [DataRequired()])
    username = StringField('Username')
    body = TextAreaField('New Post', validators = [DataRequired()])
    submit = SubmitField('Submit')
