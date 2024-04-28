import os
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from models import db, User, Friend, Post, PrivateMessage
from datetime import datetime
import argon2
import math
import re

hasher = argon2.PasswordHasher()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.secret_key = '7c19a9c83258791f711591a505b467d9'
app.config['UPLOAD_FOLDER'] = 'static/images/posts'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # limit uploads to 16MB
FILETYPES = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in FILETYPES

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        content = request.form['content']
        image = request.files['image']
        image_url = None

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            image_url = url_for('uploaded_file', filename=image_name)

        new_post = Post(userid=session["id"], content=content, image_url=image_url, creation_date=datetime.now())
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    posts = Post.query.order_by(Post.creation_date.desc()).all()
    return render_template('home.html', session=session, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()
        
        user = User.query.filter(User.username.ilike(username)).first()

        if user and argon2.PasswordHasher().verify(user.password, password):
            session['loggedin'] = True
            session['id'] = user.userid
            session['username'] = user.username
            session['profile_image'] = user.profile_image
            session['admin'] = bool(user.admin_status)

            return redirect(url_for('profile', username=user.username))
        else:
            msg = 'Invalid username or password'
            return render_template('login.html', msg=msg)

    return render_template('login.html', session=session)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    login_status = require_login_status(must_be_logged_out=True)
    if login_status is not None:
        return login_status

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'confirm-password' in request.form and 'email' in request.form:
        email = request.form['email'].strip()
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        confirmPassword = request.form['confirm-password'].strip()

        account = User.query.filter(User.username.ilike(username)).first()

        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif len(password) < 5:
            msg = 'Password too short!'
        elif password != confirmPassword:
            msg = 'Passwords do not match!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            hashed_password = hasher.hash(password)
            new_user = User(username=username, password=hashed_password, email=email, account_creation_date=datetime.now(), profile_image="/static/images/required/Default_Profile_Picture.png", banner_image="/static/images/required/Default_Banner_Picture.png")
            db.session.add(new_user)
            db.session.commit()
            msg = 'You have successfully registered!'
            return render_template('register.html', session=session, msg=msg)

    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', session=session, msg=msg)


# example on how to link to profile {{ url_for('profile', username=user.username) }}
@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        posts = Post.query.filter_by(userid=user.userid).all()
        return render_template('profile.html', session=session, username=username, user=user, posts=posts)
    else:
        return "No profile found!", 404


@app.route("/messages")
def messages():
    return render_template("messages.html", session=session)


@app.route("/settings")
def settings():
    return render_template("settings.html", session=session)


@app.route("/notifications")
def notifications():
    return render_template("notifications.html", session=session)


@app.route('/create_post', methods=['POST'])
def create_post():
    if 'username' in session:
        username = session['username']
        user = User.query.filter_by(username=username).first()
        if user:
            content = request.form.get('content')
            image_url = request.form.get('image_url')

            new_post = Post(userid=user.userid,
                            content=content,
                            image_url=image_url,
                            creation_date=datetime.now())

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('home'))
        else:
            return "User not found", 404
    else:
        return redirect(url_for('login'))

# check status of user
def require_login_status(must_be_logged_out=False, must_be_admin=False, destination='profile'):
    if 'loggedin' not in session.keys() and not must_be_logged_out:
        return redirect(url_for('login') + '?destination=' + destination)

    if 'loggedin' in session.keys() and must_be_logged_out:
        return redirect('/' + destination)

    if must_be_admin and not session['admin']:
        abort(403)

if __name__ == '__main__':
    app.run(port=45710)
