from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('blog.cfg')
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)

class Post(db.Model):
    _tablename__ = 'post'
    id = db.Column('blod_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    content = db.Column(db.TEXT)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.pub_date = datetime.utcnow()
    

class User(db.Model):
    _tablename__ = 'user'
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60))

    def __init__(self, username,password, email=""):
        self.username = username
        self.password = password
        self.email = email

        
@app.route('/')
def hello():
    return render_template("welcome.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            user = User.query.filter_by(username=username).one()
            if user.username == username and user.password == password:
                return render_template('welcome.html', username=user.username)
            else:
                error = "This user is invalid"
                return render_template('login.html', error = error)
        else:
            error = "You need to input both username and password"
            return render_template('login.html', error = error)
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if username and password:
            newUser = User(username = username, password = password, email = email)
            db.session.add(newUser)
            db.session.commit()
            return redirect(url_for('hello'))
        else:
            error = "You need to input both usernam and password"
            return render_template('signup.html', error = error)
    else:
        return render_template('signup.html')


@app.route('/blog/post')
def all_posts():
    ''''Show all post of blog'''
    
    posts = Post.query.order_by(Post.pub_date.desc()).all()
    return render_template("allpost.html", posts = posts)


@app.route('/blog/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).one()
    return render_template("post.html", post = post)


@app.route('/blog/newpost', methods=['GET','POST'])
def new_post():
    ''''Create a new post'''
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        error = "We need both a title and some content!"
        if title and content:
            newPost = Post(title = title, content = content.replace("\n", "<br>"))
            db.session.add(newPost)
            db.session.commit()
            return redirect(url_for('all_posts'))
        else:
            return render_template('newpost.html', error = error)
    else:
        return render_template('newpost.html')

@app.route('/about')
def about():
    return "this is about page"
    

if __name__ == "__main__":
    #app.debug = True
    app.run()
