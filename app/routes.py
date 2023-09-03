from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Oscar'}    
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
    
    return render_template('index.html', title='home', user=user, posts=posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign in', form=form)