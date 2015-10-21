from flask.ext.wtf import Form
from flask import render_template, flash, redirect
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired




class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class Scanner(Form):
    seed_url = StringField('seed_url', validators=[DataRequired()])

