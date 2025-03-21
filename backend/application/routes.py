from flask import current_app as app
from flask import Blueprint, request
from flask_security import login_user,auth_required,roles_required
from .models import db, User, Service, Serviceprofessional, Customer
from werkzeug.security import check_password_hash, generate_password_hash
import json
import os
import datetime

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
    
    if not user.active:
        return {'message':"Account is not active"},403
    
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
    customer = Customer(name = fullname,
                        username = username)
    user_role = app.security.datastore.find_role('user')
    app.security.datastore.add_role_to_user(user, user_role)

    db.session.add(customer)
    db.session.commit()


    return json.dumps({'message':'Successful!'}),200

@api.route("/servicepro-signup", methods=["POST"])
def servicepro_signup():
    fullname = request.form.get('fullname')
    username = request.form.get('username')
    password = request.form.get('password')
    pincode = request.form.get('pincode')
    service_type = request.form.get('service_type')
    pdf_file = request.files.get('pdfFile')  

    # Input validation
    if not fullname or not username or not password or not pincode or not service_type or not pdf_file:
        return json.dumps({'message': 'All fields including PDF file are required.'}), 400

    # Check if user already exists
    if app.security.datastore.find_user(username=username):
        return json.dumps({'message': "Username already exists."}), 409


    upload_folder = 'uploads/service_professionals'  
    os.makedirs(upload_folder, exist_ok=True)  
    pdf_filename = f"{username}_{pdf_file.filename}"
    pdf_path = os.path.join(upload_folder, pdf_filename)
    pdf_file.save(pdf_path)  # Save the file

    # Create user and hash password
    user = app.security.datastore.create_user(
        name=fullname,
        username=username,
        password=generate_password_hash(password),
        active=0
    )

    # Assign 'service_professional' role
    service_pro_role = app.security.datastore.find_role('service_professional')

    app.security.datastore.add_role_to_user(user, service_pro_role)
    service_pro = Serviceprofessional(
        name=fullname,
        username=username,
        service_type=service_type,
        date_created=datetime.datetime.now(),  
        experience=0,                    
        requests_completed=0,            
        cumulative_rating=0,
        active = 0              
    )

    db.session.add(service_pro)  
    
    db.session.commit()

    return json.dumps({'message': 'Service professional signup successful!'}), 200

### Read Service API ###
@api.route("/service", methods=["GET"])
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

@api.route("/service_professionals", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def get_serviceprofessionals():
    result = []
    for service_professional in Serviceprofessional.query.all():
        result.append({
            "id":service_professional.id,
            "name": service_professional.name,
            "service_type": service_professional.service_type,
            "cumulative_rating": service_professional.cumulative_rating,
            "active":service_professional.active
        }) 
    return result, 200 


@api.route("/service_professionals/status/<int:id>", methods=["PATCH"])
@auth_required("token")
@roles_required("admin")
def toggle_service_professional_status(id):
    service_pro = Serviceprofessional.query.get(id)

    if not service_pro:
        return json.dumps({"message": "Service Professional not found"}), 404

    # Toggle active status
    user = User.query.filter_by(username=service_pro.username).first()
    service_pro.active = not service_pro.active  # Switch between True and False
    user.active = not user.active

    db.session.commit()  # Save changes
    return json.dumps({"message": "Status updated successfully", "active": service_pro.active}), 200


@api.route("/customers", methods=["GET"])
@auth_required("token")
@roles_required("admin")
def get_customers():
    result = []
    for customer in Customer.query.all():
        result.append({
            "id":customer.id,
            "name": customer.name,
            "username": customer.username,
            "active":customer.active
        }) 
    return result, 200 

@api.route("/customers/status/<int:id>", methods=["PATCH"])
@auth_required("token")
@roles_required("admin")
def toggle_customer_status(id):
    customer = Customer.query.get(id)

    if not customer:
        return json.dumps({"message": "Customer not found"}), 404

    # Toggle active status
    user = User.query.filter_by(username=customer.username).first()
    customer.active = not customer.active  # Switch between True and False
    user.active = not user.active

    db.session.commit()  # Save changes
    return json.dumps({"message": "Status updated successfully", "active": customer.active}), 200