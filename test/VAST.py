from flask import Flask, url_for, render_template, request, make_response
from flask import flash, session, g, redirect
import os
from datetime import datetime
import hashlib
import json
import sqlite3 as lite

app = Flask('test')
app.secret_key = os.urandom(12)
DATABASE = 'accounts.db'
def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = lite.connect(DATABASE)
  db.row_factory = lite.Row
  return db

  #def make_dicts(cursor, row):
    #return dict((cursor.description[idx][0], value)
    #            for idx, value in enumerate(row))
    # db.row_factory = make_dicts

def insert(table, fields=(), values=()):
    # g.db is the database connection
    db = get_db()
    cur = db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    db.commit()
    id = cur.lastrowid
    cur.close()
    return id

def query_db(query, args=(), one=False):
  cur = get_db().cursor()
  cur.execute(query, args)
  r = [dict((cur.description[i][0], value) \
       for i, value in enumerate(row)) for row in cur.fetchall()]
  cur.close()
  return (r[0] if r else None) if one else r

#cur = get_db().execute(query, args)
#rv = cur.fetchall()
#cur.close()
#return (rv[0] if rv else None) if one else rv


def sha256sum(t):
    return hashlib.sha256(t).hexdigest()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
    #render_template('login.html')
  else:
    return redirect(url_for('user'))

@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
      if valid_login(request.form['username'],
                      sha256sum(request.form['password'])):
        session['logged_in'] = True
        session['loginName'] = request.form['username']
        return redirect(url_for('user'))
    #log_the_user_in(request.form['username'])
      else:
        flash('These credentials were not found. Please try again')
  return render_template('login.html')

def valid_login(usr, psw):
  user = query_db('select * from Accounts where Username = ?',
                  [usr], one=True)
  if user is None:
    return False
  elif user['Password'] != psw:
    return False
  else:
    return True

@app.route('/user')
def user():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  user = query_db('select * from Accounts where Username = ?',
                    [session['loginName']], one=True)
  user.pop('Password', None)
  out = json.dumps(user, sort_keys=True, indent=4, separators=(',', ': '))
  return render_template('user.html', out=out)

@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for('index'))


@app.route("/signup", methods=['GET','POST'])
def signup():
  if request.method == 'POST':
      if valid_signup(request.form['username']):
        session['logged_in'] = True
        session['loginName'] = request.form['username']
        insert('Accounts', ('Username', 'Password', 'Name', 'Email', 'Created'),
               (request.form['username'], sha256sum(request.form['password']),
               request.form['name'], request.form['email'], str(datetime.now())))
        return redirect(url_for('user'))
      else:
        flash('These credentials were already found. Please try a different username')
  return render_template('signup.html')


def valid_signup(usr):
  user = query_db('select * from Accounts where Username = ?',
                  [usr], one=True)
  if user is None:
    return True
  else:
    return False
  #return "Hello World"

#with app.test_request_context():
  #url_for('index')
  #url_for('login')
 # url_for('login', chuck='hi')
#  url_for('profile', username='Marshall Lerner')
