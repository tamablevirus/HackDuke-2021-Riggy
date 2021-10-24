from flask import Flask, request, send_file, session, redirect, url_for, render_template
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

#f_credential = json.loads(os.environ['GOOGLE_APPLICATION_CREDS'])
f = open('secret.json')
f_credential = json.load(f)
f.close()
f_credentials = firebase_admin.credentials.Certificate(f_credential)
fb = firebase_admin.initialize_app(f_credentials, {'databaseURL': 'https://riggy-72c18-default-rtdb.firebaseio.com/'})

from firebase_admin import db as database

def keygen(user, passw):
    user = user.replace('@', '!!').replace('.','!')
    key = user + "|" + passw
    return key
def login(user, passw):
    key = keygen(user, passw)
    if key in database.reference('/users').get(shallow=True):
        session["is_logged_in"] = True
        session["user"] = user
        session["passw"] = passw
        session["type"] = str(database.reference('/users/'+key + '/type').get())
        return True
    return False

def createUser(user, passw, type, name, address1, address2, city, state, zip):
    key = keygen(user, passw)
    ref = database.reference('/users/' + key)
    ref.update({"dateCreated": datetime.now().strftime("%m/%d/%Y;%H:%M:%S")})
    ref.update({"type": type,
                "name": name,
                "address1": address1,
                "address2": address2,
                "city": city,
                "state": state,
                "zip": zip})

def signUp(user, passw, type, name, address1, address2, city, state, zip):
    createUser(user, passw, type, name, address1, address2, city, state, zip)
    login(user, passw)

def signOut():
    if "is_logged_in" in session and session["is_logged_in"]:
        session["is_logged_in"] = False
        del session["user"]
        del session["passw"]
        del session['type']
        return True
    return False

def isLoggedIn():
    return "is_logged_in" in session and session['is_logged_in']

@app.route('/')
def home():
    if not isLoggedIn():
        return redirect('/login')
    return 'Hello, World'

@app.route('/signOut')
def signOutP():
    res = signOut()
    return redirect('/')
@app.route("/login", methods = ["POST", "GET"])
def loginP():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        login(email, password)
        return redirect('/')
    else:
        return render_template('login.html')


@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        address_1 = result["address1"]
        address_2 = result["address2"]
        city = result["city"]
        state = result["state"]
        zip = result["zip"]
        account_type = result["account_type"]
        signUp(email, password, account_type, name, address_1, address_2, city, state, zip)
        return redirect('/')
    else:
        return render_template('signup.html')
if __name__ == '__main__':
    app.run(debug=True)