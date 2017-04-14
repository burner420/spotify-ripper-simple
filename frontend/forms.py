from __future__ import unicode_literals
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import BooleanField, StringField, TextAreaField, PasswordField, validators


class SetupForm(FlaskForm):
    app_key = FileField('App Key',[FileRequired()])
    username = StringField('Username', [validators.Required()])
    password = StringField('Password', [validators.Required()])

class SettingsForm(FlaskForm):
    format_string = StringField('File Format String', [validators.Required()])

class NewRipForm(FlaskForm):
    urls = TextAreaField('Username', [validators.Required()])
    name = StringField('Name', [validators.Required(), validators.length(max=40)])





