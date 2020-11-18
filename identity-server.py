import flask
import json
import os
from db import Database
import tankersdk_identity
import requests

app = flask.Flask(__name__)
app.debug = True
db = Database()

#### source:https://github.com/TankerHQ/identity-python/blob/master/examples/flask/server.py
def load_config():
    current_path = os.getcwd()
    json_path = os.path.join(current_path, "config-app.json")
    with open(json_path) as stream:
        app_config = json.load(stream)
    app.config["TANKER"] = app_config

load_config()
####

app_id = app.config["TANKER"]["app_id"]
app_secret = app.config["TANKER"]["app_secret"]
auth_token = app.config["TANKER"]["auth_token"]

class User(object):

    def __init__(self,name,passwd,idenity):
        self.name = name
        self.passwd = passwd
        self.identity = idenity
        self.public_key = ""

@app.route("/create_identity")
def identity():
    #TODO implement inputs verificarion 

    request_args = flask.request.args
    name = request_args.get("name")
    passwd = request_args.get("passwd")

    identity = tankersdk_identity.create_identity(app_id, app_secret, name)
    user = User(name,passwd,identity)
    user.public_key = tankersdk_identity.get_public_identity(identity)
    db.write_object_into_file(user)

    return identity

@app.route("/create_provisory_identity")
def provisory_identity():
    #TODO implement inputs verificarion 

    request_args = flask.request.args
    email = request_args.get("email")

    identity = tankersdk_identity.create_provisional_identity(app_id,email)
    #TODO implement a dedicated database for unregistered users
    user = User(email,"",identity)
    user.public_key = tankersdk_identity.get_public_identity(identity)
    db.write_object_into_file(user)


    #Fetch code verification  
    myobj = {"app_id": app_id,
             "auth_token": auth_token,
             "email":email,
            }

    x = requests.post('https://api.tanker.io/verification/email/code', json = myobj)
    code = json.loads(x.text)

    return {"email":email,"identity":identity,"code":code["verification_code"]}

@app.route("/get_public_key")
def get_public_key():
    #TODO implement inputs verificarion 

    request_args = flask.request.args
    name = request_args.get("name")

    public_key = db.get_public_key(name)

    return public_key

@app.route("/get_user_identity")
def get_user_identity():
    #TODO implement inputs verificarion 

    request_args = flask.request.args
    name = request_args.get("name")
    passwd = request_args.get("passwd")

    user_identity = db.get_user(name)
    # pseudo authentification 
    if( user_identity[1] != passwd):
        user_identity[2] = 1 

    return user_identity[2]
