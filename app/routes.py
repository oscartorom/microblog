from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from datetime import datetime

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)

## Flask allows for dynamic inputs: <>... this can be used later within the function
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

# Decorator executed before a function
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET','POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template('edit_profile.html', title='Edit Profile', form=form)