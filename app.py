from flask import Flask, request, send_file, session
import os
import json

#Setting up basic server stuff
app = Flask(__name__)
app.secret_key = "asdfasfdasfdsafasddfsadfasdfsadfdas"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
base = os.getcwd()
app.config['UPLOAD_FOLDER'] = base +'/static'

@app.route('/')
def hello_world():
    return 'Hello, World'

if __name__ == '__main__':
    app.run()