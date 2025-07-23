from flask import render_template, request, redirect, url_for
from app import app

posts = []

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', posts=posts)

@app.route('/add_post', methods=['POST'])
def add_post():
    title = request.form['title']
    content = request.form['content']
    posts.append({'title': title, 'content': content})
    return redirect(url_for('index'))
