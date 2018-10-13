from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from app.models import User
from flask_login import login_required
from app import db
from app.forms import RegistrationForm
from app.forms import PostForm
from app.models import Post
#from app.forms import UploadForm

#---------------------------
#def connect_db():
    #return sqlite3.connect(app.config['DATABASE'])

#---------------------------

@app.route('/')
@app.route('/index')
@login_required
def index():
    #user = {'username': 'Miguel'}
    #posts = [
        #{
            #'author': {'username': 'John'},
            #'body': 'Beautiful day in Portland!'
        #},
        #{
            #'author': {'username': 'Susan'},
            #'body': 'The Avengers movie was so cool!'
        #}
    #]
    #return render_template('index.html', title='Home', user=user, posts=posts)
    return render_template('index.html', title='Home')

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
        #next_page = request.args.get('next')
        #if not next_page or url_parse(next_page).netloc != '':
            #next_page = url_for('index')     
        #return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

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

#------------post-----------------------
@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, image=form.image.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Congratulations, you have uploaded a post!')
        return redirect(url_for('index'))
    return render_template('post.html',title='Post',form=form)