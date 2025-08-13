from flask import request
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Category

from wtforms import DateTimeField, SelectMultipleField

class WHOIndicatorForm(FlaskForm):
    indicators = SelectMultipleField(_l('Indicators'), coerce=str, validators=[DataRequired()])
    submit = SubmitField(_l('Get Data'))

class ResourceForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    url = StringField(_l('URL'), validators=[DataRequired()])
    resource_type = StringField(_l('Resource Type'), validators=[DataRequired()])
    submit = SubmitField(_l('Add Resource'))

class QASessionForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    description = StringField(_l('Description'), validators=[DataRequired()])
    start_time = DateTimeField(_l('Start Time'), format='%Y-%m-%d %H:%M:%S')
    end_time = DateTimeField(_l('End Time'), format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField(_l('Schedule'))

class MessageForm(FlaskForm):
    message = StringField(_l('Message'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class CommentForm(FlaskForm):
    body = StringField(_l('Comment'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

from wtforms_sqlalchemy.fields import QuerySelectField

def category_query():
    return Category.query

class PostForm(FlaskForm):
    title = StringField(_l('Title'), validators=[DataRequired()])
    content = StringField(_l('Content'), validators=[DataRequired()])
    category = QuerySelectField(query_factory=category_query, allow_blank=True, get_label='name')
    tags = StringField(_l('Tags (comma separated)'))
    submit = SubmitField(_l('Submit'))

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegistrationForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
