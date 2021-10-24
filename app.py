from flask import Flask, request, send_file, session
import os
import json
import firebase_admin
from datetime import datetime

#Setting up basic server stuff
app = Flask(__name__)
app.secret_key = "asdfasfdasfdsafasddfsadfasdfsadfdas"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
base = os.getcwd()
app.config['UPLOAD_FOLDER'] = base +'/static'

f_credential = json.loads(os.environ['GOOGLE_APPLICATION_CREDS'])
f_credentials = firebase_admin.credentials.Certificate(f_credential)
fb = firebase_admin.initialize_app(f_credentials, {'databaseURL': 'https://riggy-72c18-default-rtdb.firebaseio.com/'})

from firebase_admin import db as database

def login(user, passw):
    key = user + ":" + passw
    if key in database.reference('/users').get(shallow=True):
        session["is_logged_in"] = True
        session["user"] = user
        session["passw"] = passw
        session["type"] = str(database.reference('/users/'+key + '/type').get())
        return True
    return False

def createUser(user, passw, type):
    key = user + ":" + passw
    ref = database.reference('/users/' + key)
    ref.update({"dateCreated": datetime.now()})
    ref.update({"type": type})

def signUp(user, passw, type):
    createUser(user, passw, type)
    login(user, passw)

def signOut(user, passw):
    if "is_logged_in" in session and session["is_logged_in"]:
        session["is_logged_in"] = False
        del session["user"]
        del session["passw"]
        del session['type']
        return True
    return False

@app.route('/')
def hello_world():
    return 'Hello, World'

if __name__ == '__main__':
    session.clear()
    app.run()