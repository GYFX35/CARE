from flask import render_template, request, redirect, url_for, flash, g
from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm, SearchForm
from app.models import User, Post, Comment, Category, Tag, Vote
from flask_login import current_user, login_user, logout_user, login_required

@app.before_request
def before_request():
    g.search_form = SearchForm()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if not Category.query.first():
        db.session.add(Category(name='Health'))
        db.session.add(Category(name='Education'))
        db.session.add(Category(name='Technology'))
        db.session.commit()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, category=form.category.data)
        tags = form.tags.data.split(',')
        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
            post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    posts = Post.query.all()
    return render_template('index.html', title='Home', form=form, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.all()
    return render_template('user.html', user=user, posts=posts)

@app.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('post', id=post.id))
    comments = post.comments.all()
    return render_template('post.html', post=post, form=form, comments=comments)

@app.route('/category/<int:id>')
def category(id):
    category = Category.query.get_or_404(id)
    posts = category.posts
    return render_template('category.html', category=category, posts=posts)

@app.route('/tag/<int:id>')
def tag(id):
    tag = Tag.query.get_or_404(id)
    posts = tag.posts
    return render_template('tag.html', tag=tag, posts=posts)

@app.route('/upvote/<int:post_id>')
@login_required
def upvote(post_id):
    post = Post.query.get_or_404(post_id)
    vote = Vote.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if vote:
        flash('You have already voted on this post.')
        return redirect(url_for('index'))
    post.votes += 1
    vote = Vote(user_id=current_user.id, post_id=post.id)
    db.session.add(vote)
    db.session.commit()
    flash('You have successfully upvoted this post.')
    return redirect(url_for('index'))

@app.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('index'))
    posts, total = Post.search(g.search_form.q.data, 1, 10)
    return render_template('search.html', title='Search', posts=posts)

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
