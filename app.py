from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json, decimal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']           = 'mysql+pymysql://root:root@localhost/blog_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']    = False

db = SQLAlchemy(app)

class Article(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(50))
    subtitle    = db.Column(db.String(50))
    author      = db.Column(db.String(30))
    date_posted = db.Column(db.DateTime)
    content     = db.Column(db.Text)

@app.route('/')
def index():
    posts = Article.query.order_by(Article.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Article.query.filter_by(id=post_id).one()
    post.data_baru = 'ini adalah data assignment'
    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title       = request.form['title']
    subtitle    = request.form['subtitle']
    author      = request.form['author']
    content     = request.form['content']

    post = Article(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
