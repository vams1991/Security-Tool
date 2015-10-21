from flask import render_template, flash, redirect,jsonify
from app import app
from .forms import LoginForm,Scanner
from XSSModule import XSS_Module
from urlparse import urlparse
from sql import SQL_Module
from crawler import main


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'hacker'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    form = Scanner()
    if form.validate_on_submit():
        flash('Scanning URL="%s"' %
              (form.seed_url.data))
        o = urlparse(form.seed_url.data)
        if o.scheme=='http' or o.scheme=='https':
          flash('Valid URL !')
          obj=main(form.seed_url.data)
          #XSS_Module(form.seed_url.data,obj)
          SQL_Module(form.seed_url.data,obj)
        else :
          flash('Invalid URL!');  
    return render_template('scanner.html',
                           title='Scanner',
                           form=form)


