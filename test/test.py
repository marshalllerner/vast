from flask import Flask, url_for, render_template
app = Flask('test')

@app.route("/")
def index():
  return render_template('home.html')

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/user/<username>')
def profile(username): pass

with app.test_request_context():
  url_for('index')
  url_for('login')
  url_for('login', chuck='hi')
  url_for('profile', username='Marshall Lerner')
