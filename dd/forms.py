from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dd.models import User, Sources, Events, Properties, sources_events
from werkzeug.datastructures import MultiDict
from dd import db


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken, please choose a different one')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError(
                'That email is taken, please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# for EventForm had to use coerce int to get form.source.data back as integer - shorturl.at/betF5 + https://wtforms.readthedocs.io/en/stable/fields.html


class EventForm(FlaskForm):
    title = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    source = SelectMultipleField('Source', choices=[], coerce=int)
    property = SelectMultipleField('Property', choices=[], coerce=int)
    submit = SubmitField('Submit')


class SourceForm(FlaskForm):
    title = StringField('Source Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    type = StringField('Source Type', validators=[DataRequired()])
    #event = QuerySelectMultipleField(query_factory=available_events)
    event = SelectMultipleField('Event', choices=[], coerce=int)
    submit = SubmitField('Submit')


class PropertyForm(FlaskForm):
    title = StringField('Property Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    type = StringField('Property Type',  validators=[DataRequired()])
    known_values = StringField('Known Values')
    min = StringField('Minimum Value')
    max = StringField('Maximum Value')
    event = SelectMultipleField('Event', choices=[], coerce=int)
    submit = SubmitField('Submit')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken, please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    'That email is taken, please choose a different one')
