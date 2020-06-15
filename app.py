from flask import Flask, request, render_template, flash, redirect, url_for, session, logging

# from data import Articles #used without db connection
# used different from turorial based on:
# https://flask-mysql.readthedocs.io/en/latest/#
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL

from functools import wraps
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)

# Config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'rockclimber!'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

# getting the data from data.py
# Articles = Articles()

# Home
@app.route('/')
def index():
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# Articles
# articles are imported from line 2
@app.route('/articles')
def articles():
    # return render_template('articles.html', articles=Articles)

    # Create cursor
    cur = mysql.connection.cursor()
    # getting articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()
    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)

# Single Article
# Note: ngle brakets to make the field dynamic.  <string: id>
@app.route('/article/<string:id>/')
def article(id):

    # Create cursor
    cur = mysql.connection.cursor()
    # getting articles
    result = cur.execute("SELECT * FROM articles where id =%s", [id])
    article = cur.fetchone()

    return render_template('article.html', article=article)


class RegisterForm(Form):
    # Documentation on how to use Forms from WTF here:
    # https://wtforms.readthedocs.io/en/2.3.x/forms/#defining-forms
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # request comes from import.
    form = RegisterForm(request.form)
    # cursor = mysql.connect().cursor()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        print('BEFORE CURSOR EXECUTE')
        cursor = mysql.connection.cursor()
        # cursor = con.cursor()
        print(cursor)

        # Create MYSQL_CURSOR
        # cur = mysql.get_db().cursor()
        # Executre query
        cursor.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                       (name, email, username, password))
        print('PASS CURSOR EXECUTE')
        # Commit to DB
        mysql.connection.commit()

        print('PASS CURSOR COMMIT')

        cursor.close()
        # message to confirm. the flask uses the _messages.html template.
        flash('you are now registered and can login', 'success')
        redirect(url_for('index'))

    # passsing form values to template.
    return render_template('register.html', form=form)

# User Register
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields (not going to use wtforms)
        username = request.form['username']
        password_candidate = request.form['password']

        # Create a curson
        cur = mysql.connection.cursor()

        # Get user by Username
        result = cur.execute(
            "SELECT * FROM users where username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # app.logger.info('PASSWORD MATCHED')  # pass is 123
                # if it passes, then create a session variable
                session['logged_in'] = True
                session['username'] = username
                flash('You are now Logger in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Login'
                return render_template('login.html', error=error)
                # Close connection
                cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


def is_logged_id(f):
    # Check if user is logged-in
    # Note that this takes another funciton as parameter, so it will be used
    # as a decorator on other route functions.
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthrorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_id
def logout():
    session.clear()
    flash('You are logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_id
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()
    # getting articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()
    if result > 0:
        print('true')
        return render_template('dashboard.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)


class ArticleForm(Form):
    # Documentation on how to use Forms from WTF here:
    # https://wtforms.readthedocs.io/en/2.3.x/forms/#defining-forms
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Dashboard
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_id
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE
        cur.execute("INSERT INTO articles(title, body, author)VALUES (%s, %s, %s)",
                    (title, body, session['username']))

        # commit
        mysql.connection.commit()
        cur.close

        flash('Article Created', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


if (__name__) == '__main__':
    # this is to enable writing to the database.
    app.secret_key = 'secret123'
    # debug = true makes it so that changes go live without having
    # to restart the server.
    app.run(debug=True)
