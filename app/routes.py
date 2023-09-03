from flask import render_template
from app import app

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

