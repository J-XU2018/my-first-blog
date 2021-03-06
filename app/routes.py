from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, EditprofileForm, AddpostForm
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
            {
                'author' : {'username' : 'Katie'}, 'body' : 'Beautiful day'
             },
             {
                'author' : {'username' : 'Laura'}, 'body' : 'The Auckland is cool..'
             },
             {
                'author' : {'username' : 'Jack'}, 'body' : 'Love NZ, Love Katie & Laura...'
             }
            ]
    return render_template('index.html', title = 'Home Page', posts = posts)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('/login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # db.session.close()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title = 'Register', form = form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username = username).first_or_404()
    # posts = [
        # {'author' : user, 'body' : 'Test post #1'},
        # {'author' : user, 'body' : 'Test post #2'}
    # ]
    posts = Post.query.filter_by(user_id = current_user.id)
    return render_template('user.html', title = 'User', user = user,  posts = posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        # db.session.close()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditprofileForm()

    if form.validate_on_submit():
    # if request.method == 'POST' and form.validate():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
        # return redirect(url_for('user.html'), )
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/add_post', methods = ['GET', 'POST'])
def add_post():
    form = AddpostForm()
    post = Post()
    if form.validate_on_submit():
        post.user_id = current_user.id
        post.body = form.body.data
        # post.timestamp = datetime.utcnow()
        db.session.add(post)
        db.session.commit()
        flash('Cons, new post successfully')
        return redirect(url_for('add_post'))
    return render_template('add_post.html ', title = 'Add Post', form = form )
