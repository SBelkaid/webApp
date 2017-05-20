from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import g, url_for, abort, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os, click

app = Flask(__name__, instance_path='/Users/johndoe/Programming/Python/flask-web/webApp/instance')
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'app.db'),
    SECRET_KEY='Meikah5aiyai2iez1Uw0',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_pass(password)


    def hash_pass(self, passw):
        return generate_password_hash(passw, method='pbkdf2:sha1', salt_length=8)


    def check_pass(self, passw):
        return check_password_hash(self.password, passw)


    def store_user(self):
        conn = get_db()
        c = conn.cursor()
        query = 'INSERT INTO user (username, password) VALUES (?,?)'
        c.execute(query, [self.username, self.password])
        conn.commit()


def connect_db():
    """Connecting DB"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Opens a new databse connection if there's none
    yet for the current application app_context
    """
    if not hasattr(g,'sqlite_db'):
        g.sqlite_db=connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('showentries')
def show_all():
    """
    Show all entries in db
    """
    command = 'select * from entries'
    c = get_db()
    print c.execute(command).fetchall()


@app.cli.command('initdb')
def initdb_command():
    """Initilize db"""
    init_db()
    print 'Initialized db'


@app.teardown_appcontext
def close_db(error):
    """Close db connection at end of request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select * from entries')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/user/<name>')
def user(name):
    return 'Hello %s' % name


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text, price) values (?, ?, ?)',
                 [request.form['title'], request.form['text'], int(100)])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/redirect')
def redirect_me():
    return redirect('http://www.example.com')


if __name__ == '__main__':
    app.run(debug=True)
