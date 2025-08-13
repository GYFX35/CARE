from flask import render_template, request, redirect, url_for, flash, g, jsonify
from sqlalchemy import func
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, PostForm, CommentForm, SearchForm, MessageForm, QASessionForm, ResourceForm, WHOIndicatorForm
from app.models import User, Post, Comment, Category, Tag, Vote, Message, QASession, Resource
from flask_login import current_user, login_user, logout_user, login_required
from openai import OpenAI

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
        post.author.add_notification('unread_comment_count', post.comments.count())
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

@app.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])

@app.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash('Your message has been sent.')
        return redirect(url_for('user', username=recipient))
    return render_template('send_message.html', title='Send Message',
                           form=form, recipient=recipient)

@app.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).all()
    return render_template('messages.html', messages=messages)

@app.route('/schedule_qa', methods=['GET', 'POST'])
@login_required
def schedule_qa():
    if not current_user.is_expert:
        flash('Only experts can schedule Q&A sessions.')
        return redirect(url_for('index'))
    form = QASessionForm()
    if form.validate_on_submit():
        session = QASession(expert_id=current_user.id, title=form.title.data,
                              description=form.description.data,
                              start_time=form.start_time.data,
                              end_time=form.end_time.data)
        db.session.add(session)
        db.session.commit()
        flash('Your Q&A session has been scheduled.')
        return redirect(url_for('index'))
    return render_template('schedule_qa.html', title='Schedule Q&A', form=form)

@app.route('/qa_sessions')
def qa_sessions():
    sessions = QASession.query.order_by(QASession.start_time.asc()).all()
    return render_template('qa_sessions.html', title='Q&A Sessions', sessions=sessions)

@app.route('/qa_session/<int:id>')
def qa_session(id):
    session = QASession.query.get_or_404(id)
    return render_template('qa_session.html', title=session.title, session=session)

@app.route('/resources')
def resources():
    resources = Resource.query.all()
    return render_template('resources.html', title='Resources', resources=resources)

@app.route('/add_resource', methods=['GET', 'POST'])
@login_required
def add_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        resource = Resource(title=form.title.data,
                              description=form.description.data,
                              url=form.url.data,
                              resource_type=form.resource_type.data)
        db.session.add(resource)
        db.session.commit()
        flash('The resource has been added.')
        return redirect(url_for('resources'))
    return render_template('add_resource.html', title='Add Resource', form=form)

@app.route('/data/posts_per_category')
def data_posts_per_category():
    data = db.session.query(Category.name, func.count(Post.id)).join(Post).group_by(Category.name).all()
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return jsonify({'labels': labels, 'values': values})

import requests

@app.route('/unesco_data')
def unesco_data():
    indicators = {
        'LR.AG15T99': 'Literacy rate, adult total (% of people ages 15 and above)',
        'EA.PRIMARY.AG25T99.CUM': 'Educational attainment, at least completed primary, population 25+, total (%) (cumulative)',
        'SE.PRM.ENRR': 'School enrollment, primary, both sexes (gross %)',
        'SE.SEC.ENRR': 'School enrollment, secondary, both sexes (gross %)'
    }
    data = {}
    for code, name in indicators.items():
        url = f"http://data.uis.unesco.org/api/v1/data/indicator/{code}?format=json"
        response = requests.get(url)
        data[name] = response.json()['dataSets'][0]['series']
    return render_template('unesco_data.html', title='UNESCO Data', data=data)

from flask import session

def get_who_indicators():
    if 'who_indicators' not in session:
        try:
            url = "https://ghoapi.azureedge.net/api/Indicator"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            session['who_indicators'] = response.json()['value']
        except requests.exceptions.RequestException as e:
            flash(f"Error fetching WHO indicators: {e}")
            return []
    return session['who_indicators']

@app.route('/who_indicators', methods=['GET', 'POST'])
def who_indicators():
    form = WHOIndicatorForm()
    indicators = get_who_indicators()
    if not indicators:
        return render_template('who_indicators.html', title='WHO Indicators', form=form, error="Could not fetch indicators.")

    form.indicators.choices = [(indicator['IndicatorCode'], indicator['IndicatorName']) for indicator in indicators]

    if form.validate_on_submit():
        return redirect(url_for('who_data', indicators=','.join(form.indicators.data)))

    return render_template('who_indicators.html', title='WHO Indicators', form=form)

@app.route('/who_data')
def who_data():
    indicators_str = request.args.get('indicators')
    if not indicators_str:
        flash('Please select at least one indicator.')
        return redirect(url_for('who_indicators'))

    indicators = indicators_str.split(',')
    data = {}
    indicator_names = {ind['IndicatorCode']: ind['IndicatorName'] for ind in get_who_indicators()}

    for indicator in indicators:
        try:
            url = f"https://ghoapi.azureedge.net/api/{indicator}"
            response = requests.get(url)
            response.raise_for_status()
            data[indicator] = response.json()['value']
        except requests.exceptions.RequestException as e:
            flash(f"Error fetching data for indicator {indicator}: {e}")
            data[indicator] = []

    return render_template('who_data.html', title='WHO Data', data=data, indicator_names=indicator_names)

@app.route('/visualizations')
def visualizations():
    return render_template('visualizations.html', title='Data Visualizations')

@app.route('/language/<language>')
def set_language(language=None):
    session['lang'] = language
    return redirect(url_for('index'))

@app.route('/games')
@login_required
def games():
    return render_template('games.html', title='Educational Games')

@app.route('/fitness_game')
@login_required
def fitness_game():
    return render_template('fitness_game.html', title='Fitness Game')

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

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
        message = request.form['message']
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )
        return jsonify({'response': response.choices[0].message.content})
    return render_template('chatbot.html')

@app.route('/fitness_coach', methods=['POST'])
def fitness_coach():
    client = OpenAI(api_key=app.config['OPENAI_API_KEY'])
    message = request.form['message']
    prompt = f"You are a friendly and encouraging fitness coach. A user has asked you the following question about their workout: '{message}'. Provide a helpful and motivating response."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly and encouraging fitness coach."},
            {"role": "user", "content": message}
        ]
    )
    return jsonify({'response': response.choices[0].message.content})
