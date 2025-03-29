from celery import shared_task
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import  MIMEText
from jinja2 import Template
from datetime import datetime,timedelta
from csv import DictWriter
from io import StringIO


from application.models import User,Servicerequest,Serviceprofessional, Customer


@shared_task
def daily_reminder():
    smtpObj = smtplib.SMTP('localhost',1025)

    with open("templates/daily-reminder.html") as file:
        content = Template(file.read())

    pending_requests = Servicerequest.query.filter_by(service_status="pending").all()

    professional_ids = {req.professional_id for req in pending_requests if req.professional_id}

    professionals = Serviceprofessional.query.filter(Serviceprofessional.id.in_(professional_ids)).all()
    for professional in professionals:
        email = MIMEMultipart()
        email["To"] = professional.username
        email["From"] = "admin@HHservice.com"
        email["Subject"] = f"Daily Reminder - {professional.name}"

        html = MIMEText(content.render(professional=professional),'html')
        email.attach(html)

        smtpObj.sendmail("admin@HHservice.com", professional.username, email.as_string())
    

@shared_task
def monthly_reminder():
    smtpObj = smtplib.SMTP('localhost',1025)

    with open("templates/monthly-reminder.html") as file:
        content = Template(file.read())

    customers = Customer.query.all()

    usernames = {customer.username for customer in customers}

    users = User.query.filter(User.username.in_(usernames)).all()
    
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)

    first_day_of_last_month = (first_day_of_current_month - timedelta(days=1)).replace(day=1)

    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
    for user in users:
        email = MIMEMultipart()
        email["To"] = user.username
        email["From"] = "admin@HHservice.com"
        email["Subject"] = f"Monthly Report - {user.name}"

        pending_requests = Servicerequest.query.filter(Servicerequest.user_id == user.id,
                                                       Servicerequest.date_of_request >= first_day_of_last_month,
                                                       Servicerequest.date_of_request <= last_day_of_last_month,
                                                       Servicerequest.service_status != "completed").all()
        
        completed_requests = Servicerequest.query.filter(Servicerequest.user_id == user.id,
                                                         Servicerequest.date_of_request >= first_day_of_last_month,
                                                         Servicerequest.date_of_request <= last_day_of_last_month,
                                                         Servicerequest.service_status == "completed").all()
        total_requests ={
            "Requested": len(pending_requests),
            "Closed": len(completed_requests)
        }

        pending_requests = [
            {"id":req.id,
             "service_name":req.service_name,
             "total_amount":req.total_amount,
             "date_of_request":req.date_of_request
            }
        for req in pending_requests]

        completed_requests = [
            {"id":req.id,
             "service_name":req.service_name,
             "total_amount":req.total_amount,
             "date_of_request":req.date_of_request,
             "date_of_completion":req.date_of_completion
            }
        for req in completed_requests]
        


        html = MIMEText(content.render(total_requests=total_requests,pending_requests = pending_requests,completed_requests = completed_requests),'html')
        email.attach(html)

        smtpObj.sendmail("admin@HHservice.com", user.username, email.as_string())


@shared_task
def export_csv():
  
    file = StringIO()
    writer = DictWriter(file, fieldnames= ['service_id','customer_id','professional_id','date_of_request','remarks'])
    writer.writeheader()
    service_requests = Servicerequest.query.filter_by(service_status="completed").all()
    for request in service_requests:
        
        writer.writerow({'service_id':request.service_id,
                         'customer_id':request.user_id,
                         'professional_id':request.professional_id,
                         'date_of_request':request.date_of_request,
                         'remarks':request.feedback})
    file.seek(0)
    return file.read()


