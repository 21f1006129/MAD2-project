from flask import current_app as app
from flask import Blueprint, request, send_file
from flask_security import login_user,auth_required,roles_required,roles_accepted,current_user
from werkzeug.security import check_password_hash, generate_password_hash
from io import BytesIO
import json
import os
import datetime

from application.models import db, User, Service, Serviceprofessional, Customer, Servicerequest
from application.worker import export_csv
from application.cache import cache
from celery.result import AsyncResult

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
                        username = username,
                        active = 1)
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
        pincode = pincode,
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
@cache.cached(30)
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
    if not service:
        return {'message': 'No service with this id was found'}, 400
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

@api.route("/service_requests/all", methods=["GET"])
@auth_required("token")
@roles_required("admin")
@cache.cached(30)
def get_admin_service_requests():
    requests = Servicerequest.query.all()
    
    result = []
    for req in requests:
        result.append({
            "id": req.id,
            "service_name": req.service_name,
            "user_id":req.user_id,
            "professional_id":req.professional_id,
            "date_of_request": req.date_of_request,
            "service_status": req.service_status
        })
    return (result), 200

@api.route("/service_professionals", methods=["GET"])
@auth_required("token")
@roles_accepted("admin","user")
@cache.cached(30)
def get_service_professionals():
    result = []
    for service_professional in Serviceprofessional.query.all():
        result.append({
            "id":service_professional.id,
            "name": service_professional.name,
            "service_type": service_professional.service_type,
            "pincode": service_professional.pincode,
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


#Get service requests
@api.route("/service_requests/professional", methods=["GET"])
@auth_required("token")
@roles_required("service_professional")
def get_professional_requests():
    service_professional = Serviceprofessional.query.filter_by(username=current_user.username).first()
    requests = Servicerequest.query.filter_by(professional_id=service_professional.id).all()
    
    result = []
    for req in requests:
        result.append({
            "id": req.id,
            "service_name": req.service_name,
            "date_of_request": req.date_of_request,
            "address": req.address,
            "pincode": req.pincode,
            "service_status": req.service_status,
            "feedback": req.feedback
        })
    return (result), 200


#Booking a Service

@api.route("/book_service", methods=["POST"])
@auth_required("token")
@roles_required("user")
def book_service():

    service_type = request.json.get("service_name")
    date = request.json.get("date")
    address = request.json.get("address")
    pincode = request.json.get("pincode")
    total_amount = request.json.get("total_amount")
    user_id = current_user.id

    # Find available professionals
    professionals = Serviceprofessional.query.filter_by(pincode=pincode, service_type=service_type).all()

    if not professionals:
        return json.dumps({"message": "No service professionals available in this area."}), 409

    # Sort by least assignments for the selected date
    professionals.sort(key=lambda p: len([r for r in p.requests_on_date if str(r.date_of_request) == str(date)]))

    for professional in professionals:
        if professional.active:
            service_request = Servicerequest(
                service_id=Service.query.filter_by(name=service_type).first().id,
                service_name = service_type,
                professional_id=professional.id,
                user_id=user_id,
                date_of_request=datetime.datetime.strptime(date, "%Y-%m-%d").date(),
                total_amount = total_amount,
                address = address,
                pincode = pincode
            )
            db.session.add(service_request)
            db.session.commit()
            return json.dumps({"message": f"Assigned to {professional.name}", "request_id": service_request.id}), 200

    return json.dumps({"message": "All professionals rejected or unavailable. Please try another date."}), 400

# Service professional Accepts a service request
@api.route("/accept_service/<int:request_id>", methods=["PATCH"])
@auth_required("token")
@roles_required("service_professional")
def accept_service(request_id):
    request_entry = Servicerequest.query.get(request_id)
    if not request_entry:
        return json.dumps({"message": "Request not found"}), 404

    request_entry.service_status = "assigned"
    db.session.commit()

    return json.dumps({"message": "Service request accepted."}), 200

# Service professional Rejecting a service request
@api.route("/reject_service/<int:request_id>", methods=["PATCH"])
@auth_required("token")
@roles_required("service_professional")
def reject_service(request_id):
    request_entry = Servicerequest.query.get(request_id)
    if not request_entry:
        return json.dumps({"message": "Request not found"}), 404

    # Add current professional ID to rejected_by list
    service_professional = Serviceprofessional.query.filter_by(username=current_user.username).first()
    updated_rejected_list = request_entry.rejected_by + [service_professional.id]  # Create a new list
    request_entry.rejected_by = updated_rejected_list
    request_entry.service_status = "pending"
    db.session.commit()

    return reassign_service(request_entry)

def reassign_service(request_entry):
    print(request_entry.rejected_by)
    pincode = request_entry.pincode
    service_name = request_entry.service_name
    date = request_entry.date_of_request
    # Get all professionals in the same pincode & service type
    professionals = Serviceprofessional.query.filter_by(pincode=pincode, service_type=service_name).all()

    # Sort by least requests and exclude those who rejected
    professionals = sorted(professionals, key=lambda p: len([r for r in p.requests_on_date if r.date_of_request == date]))
    available_professionals = [p for p in professionals if p.id not in request_entry.rejected_by and p.active]
    if available_professionals:
        new_professional = available_professionals[0]  # Pick the least busy available professional
        request_entry.professional_id = new_professional.id
        request_entry.status = "pending"  # Set status back to pending
        db.session.commit()
        return json.dumps({"message": f"Reassigned to {new_professional.name}", "professional_id": new_professional.id}), 200
    else:
        request_entry.professional_id = None
        db.session.commit()

    # If no professionals left, notify customer
    return json.dumps({"message": "All professionals rejected this request."}), 400

@api.route("/service_requests/user", methods=["GET"])
@auth_required("token")
@roles_required("user")
def get_user_requests():
    requests = Servicerequest.query.filter_by(user_id=current_user.id).all()
    
    result = []
    for req in requests:
        result.append({
            "id": req.id,
            "service_name": req.service_name,
            "professional_id":req.professional_id,
            "date_of_request": req.date_of_request,
            "address": req.address,
            "pincode": req.pincode,
            "service_status": req.service_status,
            "feedback": req.feedback
        })
    return (result), 200

@api.route("/close-service/<int:request_id>", methods=["PATCH"])
@auth_required("token")
@roles_required("user")
def close_service(request_id):
    request_entry = Servicerequest.query.get(request_id)
    if not request_entry:
        return json.dumps({"message": "Request not found"}), 404

    request_entry.service_status = "completed"
    request_entry.date_of_completion = datetime.date.today() 
    db.session.commit()

    return json.dumps({"message": "Service request marked as completed."}), 200


@api.route("/delete_service_request/<int:request_id>", methods=["DELETE"])
@auth_required("token")
@roles_required("user")
def delete_service_request(request_id):
    request_entry = Servicerequest.query.get(request_id)
    if not request_entry:
        return json.dumps({"message": "Request not found"}), 404

    db.session.delete(request_entry)
    db.session.commit()

    return json.dumps({"message": "Service request deleted. Please book again."}), 200

@api.route("/service_request/<int:request_id>", methods=["GET"])
@auth_required("token")
@roles_required("user")
def get_service_request(request_id):
    request = Servicerequest.query.get(request_id)
    if not request:
        return json.dumps({"message": "Request not found"}), 404

    return ({
        "id": request.id,
        "service_name": request.service_name
    }), 200

@api.route("/submit-feedback/<int:request_id>", methods=["PATCH"])
@auth_required("token")
@roles_required("user")
def submit_feedback(request_id):
    request_entry = Servicerequest.query.get(request_id)
    if not request_entry:
        return json.dumps({"message": "Request not found"}), 404

    request_entry.feedback = request.json.get("feedback", "")
    request_entry.rating = request.json.get("rating", None)
    service_professional = Serviceprofessional.query.get(request_entry.professional_id)
    num_of_requests = service_professional.requests_completed
    cumulative_rating = service_professional.cumulative_rating
    service_professional.cumulative_rating = ((num_of_requests*cumulative_rating)+int(request_entry.rating))/(num_of_requests+1)
    service_professional.requests_completed = service_professional.requests_completed+1
    db.session.commit()
    return json.dumps({"message": "Feedback submitted successfully."}), 200


#### CELERY EXPORT CSV TASK ######
@api.route("/export")
def export():
    task = export_csv.delay()
    return {"id": task.id}


@api.route("/export/<string:tid>/status")
def export_status(tid):
    result = AsyncResult(tid)
    return {"status": result.status}


@api.route("/export/<string:tid>")
def export_download(tid):
    result = AsyncResult(tid)
    file = BytesIO(result.result.encode())
    return send_file(file, 
                     "text", 
                     as_attachment=True, 
                     download_name="export.csv")

