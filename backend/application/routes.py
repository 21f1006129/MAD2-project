from flask import current_app as app
from flask import Blueprint, request
from flask_security import login_user,auth_required,roles_required
from .models import db, User, Service
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

    if not username:
        return {'message':'Invalid response '}, 400
    if not password:
        return {'message':'Invalid response '}, 400
    if not fullname:
        return {'message':'Invalid response '}, 400


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

### Read Service API ###
@api.route("/service", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def get_service():
    result = []
    for service in Service.query.all():
        result.append({
            "id":service.id,
            "name": service.name,
            "price": service.price,
            "description": service.description
        })
    return result, 200 

### Create Service API ###
@api.route("/service/create",methods=["POST"])
@auth_required("token")
@roles_required("admin")
def create_service():
    servicename = request.json.get('servicename')
    description = request.json.get('description')
    baseprice = request.json.get('baseprice')

    if not servicename:
        return {'message':'Invalid response '}, 400
    if not description:
        return {'message':'Invalid response '}, 400
    if not baseprice:
        return {'message':'Invalid response'}, 400
    service = Service.query.filter_by(name=servicename).first()
    if service:
        return {'message':'This Service name already exists'}, 409
    service = Service(name=servicename,description=description,price=baseprice)
    db.session.add(service)
    db.session.commit()
    return {'message': 'Service creation Successful'}, 200


### Update Service API ###
@api.route("/service/update",methods=["POST"])
@auth_required("token")
@roles_required("admin")
def update_service():
    id = request.json.get('id')
    servicename = request.json.get('new_servicename')
    description = request.json.get('new_description')
    baseprice = request.json.get('new_baseprice')

    if not servicename:
        return {'message':'Invalid response '}, 400
    if not description:
        return {'message':'Invalid response '}, 400
    if not baseprice:
        return {'message':'Invalid response'}, 400
    service = Service.query.filter_by(id=id).first()
    service.name = servicename
    service.description = description
    service.price = baseprice
    db.session.commit()
    return {'message': 'Service creation Successful'}, 200

### Delete Service API ###
@api.route("/service/delete/<int:service_id>",methods=["DELETE"])
@auth_required("token")
@roles_required("admin")
def delete_service(service_id):
    service = Service.query.filter_by(id = service_id).first()

    if not service:
        return {'message':'Service Not Found'}, 404
    db.session.delete(service)
    db.session.commit()
    return {'message':"Successfully Deleted"}, 200