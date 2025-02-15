from flask import current_app as app
from flask import Blueprint, request
from flask_security import login_user
from .models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
import json

api = Blueprint('api',__name__)

### Login api Implementation ###

@api.route("/signin",methods = ['POST'])
def signin():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        return {'message':'Invalid username '}, 400
    if not password:
        return {'message':'Invalid password '}, 400

    user = app.security.datastore.find_user(username=username)

    if not user:
        return {'message':'User not found'},404
    
    if not check_password_hash(user.password, password):
        return {'message':'User not found'},404

    login_user(user)

    return {'token':user.get_auth_token(),
        'role': user.get_role()}

### Signup Api Implementation ###
@api.route("/signup",methods = ['POST'])
def signup():
    fullname = request.json.get('fullname')
    username = request.json.get('username')
    password = request.json.get('password')

    if app.security.datastore.find_user(username=username):
        
        return json.dumps({'message':"Username already exists"}),409
    
    user = app.security.datastore.create_user(name = fullname,
                                              username = username,
                                              password = generate_password_hash(password))
    user_role = app.security.datastore.find_role('user')
    app.security.datastore.add_role_to_user(user, user_role)
    db.session.commit()


    return json.dumps({'message':'Successful!'}),200

@api.route("/servicepro-signup",methods=["POST"])
def servicepro_signup():

    return json.dumps({'message':'Successful'}),200
