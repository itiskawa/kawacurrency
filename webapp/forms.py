from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from webapp.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('There already exists an account with this e-mail address')


class LoginForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=2, max=20)])
    
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])

    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('There already exists an account with this e-mail address')


class TransactionForm(FlaskForm):
    username = StringField('Receiver', 
                validators=[DataRequired(), Length(min=2, max=20)])
    
    amount = FloatField('How much do you want to send?', 
                        validators=[DataRequired()])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists')
            
    submit = SubmitField('Update')