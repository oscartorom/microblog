from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Sydney!"
        },
        {
            "author": {"username": "Susan"},
            "body": "I hate movies"
        }
    ]
    
    return render_template('index.html', title='home', posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    # If user is authenticated, go to main page
    if current_user.is_authenticated:
        return redirect(url_for('index'))        
    
    # Load the form to login
    form = LoginForm()
    ### When they submit the form...
    if form.validate_on_submit():
        # Get the user, and validate it exists and the password is right. If it fails, redirect to login again
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # Login the user with flask-login. Then mark the next page so we can redirect. If there is no next page, then go to index
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    # This happens when no login/form has been submited. Default, just loads the form
    return render_template('login.html', title='Sign in', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))