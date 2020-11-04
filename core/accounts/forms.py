from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from flask_login import current_user
from core.models import User


# Trying these forms with macros, just out of interest
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='Please enter email address'),
                                             Email(message='Please enter valid email address')],
                        render_kw={"placeholder": "Enter Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
    submit = SubmitField('Log-In')


class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(message='Please enter email address'),
                                             Email(message='Please enter valid email address')],
                        render_kw={"placeholder": "Enter Email"})
    username = StringField('User Name', validators=[DataRequired(message='Please enter Username'),
                                                    Length(min=3, message='Username is too short')],
                           render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, message='Password is too short'),
                                                     EqualTo('pass_confirm', message='Passwords must match')],
                             render_kw={"placeholder": "Must contain one digit"})
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()],
                                 render_kw={"placeholder": "Repeat Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')


class UpdateUserForm(FlaskForm):
    email = StringField('Update Email', validators=[DataRequired(), Email()])
    username = StringField('Update Username', validators=[DataRequired(), Length(min=3, message='Username is too short')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')


