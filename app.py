import sqlite3
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class CodeSpeedyBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(100), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    num_like = db.Column(db.Integer, default=0)
    def __repr__(self):
        return self.title
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()
db.session.commit()
@app.route('/')
@app.route('/login',methods=['GET', 'POST'])
def login():
    return render_template('login.html')
@app.route('/signup',  methods=['GET', 'POST'])
def signup():
     msg = ''
     if request.method == 'POST':
        user_name = request.form['Username']
        user_email = request.form['email']
        user_pwd = request.form['psw']
        new_user = User(username=user_name,email=user_email,password=user_pwd)
        conn = sqlite3.connect('database.db')
        cursorObj = conn.cursor()
        cursorObj.execute('SELECT * FROM user WHERE username = ?', (user_name, ))
        rows = cursorObj.fetchone()
        if rows:
            msg = 'Username already exists !'
            return render_template('signup.html',msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',user_email):
            msg = 'Invalid email address !'
            return render_template('signup.html',msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', user_name):
            msg = 'Username must contain only characters and numbers !'
            return render_template('signup.html',msg=msg)
        elif not user_name or not user_pwd or not user_email:
            msg = 'Please fill out the form !'
            return render_template('signup.html',msg=msg)
        else:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
     else:
        msg='Please fill out the form !'
        return render_template('signup.html',msg=msg)
@app.route('/posts',  methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = CodeSpeedyBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts')
    else:
        all_posts = CodeSpeedyBlog.query.order_by(CodeSpeedyBlog.posted_on).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = CodeSpeedyBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    to_edit = CodeSpeedyBlog.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.posted_by = request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=to_edit)
@app.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = CodeSpeedyBlog.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/posts')
@app.route('/posts/like/<int:id>', methods=['GET', 'POST'])
def like(id):
    to_like = CodeSpeedyBlog.query.get_or_404(id)
    if request.method == 'POST':
       to_like.num_like = request.form['numlike'] + 1
       db.session.commit()
       return redirect('/posts')
    else:
        all_posts = CodeSpeedyBlog.query.order_by(CodeSpeedyBlog.posted_on).all()
        return render_template('posts.html', posts=all_posts)
if __name__ == "__main__":
    app.run(debug=True)