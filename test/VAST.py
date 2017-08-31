from flask import Flask, url_for, render_template, request, make_response
from flask import flash, session, g, redirect, send_file
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import bcrypt
import json
import sqlite3 as lite
from bson import BSON
from bson import json_util
from website_vcsub import BOINCupload, md5

app = Flask('VAST')
app.config['MONGO1_DBNAME'] = 'accountsdb'
mongo = PyMongo(app, config_prefix='MONGO1')
app.secret_key = os.urandom(12) #TODO not sure if this is a permanent solution
UPLOAD_FOLDER='./uploaded_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DATABASE = 'accounts.db'


# TODO: Externally Visible Server
# If you run the server you will notice that the server is only accessible from
#  your own computer, not from any other in the network. This is the default
#  because in debugging mode a user of the application can execute arbitrary
#  Python code on your computer.
# If you have the debugger disabled or trust the users on your network, you can
# make the server publicly available simply by adding --host=0.0.0.0 to the
# command line:
#
# flask run --host=0.0.0.0
#
# This tells your operating system to listen on all public IPs.

#check if the file is allowed and not trying to hack the server
NOT_ALLOWED_EXTENSIONS = set(['html', 'php'])
def allowed_file(filename):
    return not '.' in filename or \
           filename.rsplit('.', 1)[1].lower() not in NOT_ALLOWED_EXTENSIONS


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#When the user first goes to the website
@app.route("/", methods=['GET','POST'])
def index():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
    #render_template('login.html')
  else:
    return redirect(url_for('user'))

#If the user clicks the "forgot password" on the login page
@app.route('/forgotLogin')
def forgot_login():
    return "Hello World" #TODO have the password be changed

# If it is a post request, the function takes the post request and
# checks if the user is already in the user database
@app.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    users = mongo.db.users
    login_user = users.find_one({'Username' : request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'),
                        login_user['Password'].encode('utf-8')) == login_user['Password'].encode('utf-8'):
            session['logged_in'] = True
            session['loginName'] = request.form['username']
            return redirect(url_for('user'))

    flash('These credentials were not found. Please try again')
  return render_template('login.html')

# prints the JSON database of a user in the users database (not including
# the password and the _id, which mongdb automatically includes)
@app.route('/user', methods=['GET'])
def user():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  users = mongo.db.users
  user = users.find_one({'Username': session['loginName']})
  user.pop('Password', None)
  user.pop('_id', None)
  out = json.dumps(user, sort_keys=True, indent=4, separators=(',', ': '), default=json_util.default)
  return render_template('user.html', out=out)


# @app.route('/uploadtest', methods=['GET', 'POST'])
# def upload_test():
#     print "nay"
#     if request.method == 'POST':
#         print "yeet"
#         # check if the post request has the file part
#         if 'jobFile' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#             print "failed 1"
#         dafiles = request.files.getlist('inputFiles[]')
#         print dafiles
#         print len(dafiles)
#         i = 0
#         for file in dafiles:
#             print "loop"
#             # if user does not select file, browser also
#             # submit a empty part without filename
#             if file.filename == '':
#                 flash('No selected file')
#                 return redirect(request.url)
#                 print "failed 2"
#             if file and allowed_file(file.filename):
#                 print "yay made it"
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], "hi" + str(i)))
#                 i = i + 1
#         return redirect(url_for('user'))
#
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <p><input type=file name=file>
#          <input type=submit value=Upload>
#     </form>
#     '''

#This is the webpage for when a user uploads a file and its inputFiles to the server
@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template('upload.html')
    # check if the post request has the file part
    if 'jobFile' not in request.files:
        flash('No file')
        return redirect(request.url)
    afile = request.files['jobFile']
    # if user does not select file, browser also
    # submit a empty part without filename
    if afile.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if afile and allowed_file(afile.filename):
        users = mongo.db.users
        files = mongo.db.files
        # get the BOINC authorization code from the user profile
        user = users.find_one({'Username': session.get('loginName')})
        boincCode = user['BOINCauth']
        if boincCode == "":
            #TODO get the boinc code from the user and then store it in the users mongoDB
            hi = "1"
        # get the input files
        inputFiles = request.files.getlist('inputFiles[]')
        # TODO: BOINCupload(session.get('loginName'), boincCode, afile, inputFiles) #TODO add this back
        jobName = secure_filename(afile.filename)
        # this is the only way I could get it to work. I would have to save the
        # file and then hash the file and then check if the hashname is already
        # in the files collection and if it is then remove the file, otherwise
        # it will add the file metadata to the files collection
        afile.save(os.path.join(app.config['UPLOAD_FOLDER'], jobName))
        hashName = md5(os.path.join(app.config['UPLOAD_FOLDER'], afile.filename))
        jobHashName = hashName
        jobExists = files.find_one({'HashName': hashName})
        if jobExists is None:
            flash("uploaded " + afile.filename)
            os.rename(os.path.join(app.config['UPLOAD_FOLDER'], jobName), os.path.join(app.config['UPLOAD_FOLDER'], hashName))
            files.insert_one({
            #    "File": afile,
                "SecureName": jobName,
                "HashName": hashName,
                "NormalName": afile.filename,
                "Users": [session.get('loginName')],
                "UploadedFirst": str(datetime.now())
            })
        else:
            flash(afile.filename + " was already found on this server")
            os.remove("uploaded_files/" + jobName)
            files.update(
            { "HashName": hashName },
            { '$addToSet': {"Users": session.get('loginName')}
            })
        # this is the same procedure as the job file comment above, except this
        # runs through the input files and also appends their names to an array
        inputFileNames = []
        for job in inputFiles:
            if allowed_file(job.filename):
                jobName = secure_filename(job.filename)
                job.save(os.path.join(app.config['UPLOAD_FOLDER'], jobName))
                hashName = md5(os.path.join(app.config['UPLOAD_FOLDER'],job.filename))
                inputFileNames.append(hashName)
                inputFileExists = files.find_one({'HashName' : hashName})
                if inputFileExists is None:
                    flash("uploaded " + job.filename)
                    os.rename(os.path.join(app.config['UPLOAD_FOLDER'], jobName), os.path.join(app.config['UPLOAD_FOLDER'], hashName))
                    files.insert_one({
                    #    "File": job,
                        "SecureName": jobName,
                        "HashName": hashName,
                        "NormalName": job.filename,
                        "Users": [session.get('loginName')],
                        "UploadedFirst": str(datetime.now())
                    })
                else:
                    flash(job.filename + " was already found on this server")
                    os.remove("uploaded_files/" + jobName)
                    files.update(
                    {"HashName": hashName},
                    {'$addToSet': {
                    "Users": session.get('loginName')}
                    })

        # updates the users collection to include the batch that was just uploaded
        users.update(
        {"Username": session.get("loginName")},
        {'$push': {
        "Batches": {
            "jobFile": afile.filename,
            "JobFileHash": jobHashName,
            "InputFiles": inputFileNames,
            "Created": str(datetime.now()),
            "LastUpdated": str(datetime.now()),
            "Active": "Ready",
            "Results": []
        }
        }})
        return redirect(url_for('user'))

# clears the user from the session
@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for('index'))

#the function is pressed when the user clicks the tutorial on the upload page
@app.route("/downloadTutorial")
def downloadInputFileFinder():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  dir = os.path.dirname(__file__)
  filename = os.path.join(dir, '../getInputFiles.py')
  return send_file("getInputFiles.py", as_attachment=True)

# the tutorial function
@app.route("/tutorial")
def tutorial():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  return render_template("tutorial.html")

# the function called when a user signs up. If it is a post request, the user
# database is checked to see if the username is already used, and if so, makes
# the user signing up to try a new username. Otherwise, it adds
@app.route("/signup", methods=['GET','POST'])
def signup():
  if request.method == 'POST':
      users = mongo.db.users
      existing_user = users.find_one({'Username': request.form['username']})
      if existing_user is None:
          hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
          users.insert_one({
              "BOINCauth": "",
              "Batches": [],
              "Created": str(datetime.now()),
              "Email": request.form['email'],
              "Name": request.form['name'],
              "Password": hashpass,
              "Results": [],
              "Username": request.form['username']
          })
          return redirect(url_for('user'))
      else:
         flash('These credentials were already found. Please try a different username')
  return render_template('signup.html')
