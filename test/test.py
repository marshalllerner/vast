from flask import Flask, url_for, render_template, request, make_response
from flask import flash, session
import os

app = Flask('test')
app.secret_key = os.urandom(12)

@app.route("/")
def index():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return display_user(session.get('loginName'))

@app.route('/login', methods=['POST'])
def login():
  if valid_login(request.form['username'],
                 request.form['password']):
    session['logged_in'] = True
    session['loginName'] = request.form['username']
    return index()
    #log_the_user_in(request.form['username'])
  else:
    flash('These credentials were not found. Please try again')
    return render_template('login.html')

def valid_login(usr, psw):
    # TODO
    #set_cookie("loginActive", value=usr,max_age=14400)
    return True

@app.route('/user')
def display_user(username):
   return "Hello World"

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

  #return "Hello World"

#with app.test_request_context():
  #url_for('index')
  #url_for('login')
 # url_for('login', chuck='hi')
#  url_for('profile', username='Marshall Lerner')
