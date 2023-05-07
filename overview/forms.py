from flask_wtf import FlaskForm
from wtforms import (
    StringField, IntegerField, PasswordField,
    BooleanField, SubmitField, DateField, TextAreaField)
from wtforms.validators import (
    DataRequired, ValidationError, Email, EqualTo, Length, NumberRange)
from .models import User
from wtforms.widgets.core import Markup
from wtforms.widgets.core import html_params

class ProjectForm(FlaskForm):
    number = StringField(
        'Number', validators=[DataRequired(), Length(min=1, max=139)])
    name = StringField(
        'Name', validators=[DataRequired(), Length(min=1, max=139)])
    value = IntegerField('Value', validators=[
        DataRequired(), 
        NumberRange(min=1, max=1000000, message='Value must be greater than or equal to 1')])
    timestamp = DateField('Date Recieved', format='%d/%m/%y')
    client = StringField(
        'Client', validators=[DataRequired(), Length(min=1, max=139)])
    submit = SubmitField('Create Project')


class TaskForm(FlaskForm):
    title = StringField(
        'Task', validators=[DataRequired(), Length(min=1, max=139)])
    genre = StringField(
        'Genre', validators=[DataRequired(), Length(min=1, max=49)])
    submit = SubmitField('Add Task')


class InlineButtonWidget(object):
    """
    Render a basic ``<button>`` field.
    """
    input_type = 'submit'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('value', field.label.text)
        return Markup(
            '<button %s><i class="material-icons">done</i></button>' % 
            self.html_params(name=field.name, **kwargs))


class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.  This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()


class TaskCompleteForm(FlaskForm):
    duration = IntegerField(
        'Task Time',
        validators=[DataRequired(), NumberRange(min=1, max=10000)])
    submit = InlineSubmitField('complete')