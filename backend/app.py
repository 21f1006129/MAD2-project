from flask import Flask
from celery import Celery, Task
from flask_security import SQLAlchemyUserDatastore, Security
from application.models import db, User, Role
from application.routes import api
from werkzeug.security import generate_password_hash
from flask_cors import CORS

from application.worker import daily_reminder, monthly_reminder
from celery.schedules import crontab

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ringostarmccourtneypaul'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.sqlite3"
    app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"
    app.config["CELERY_RESULT_BACKEND"] = "redis://localhost:6379/0"

    db.init_app(app)
    CORS(app)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)

    with app.app_context():
        db.create_all()
        if not Role.query.filter_by(name="admin").first():
            role_admin = app.security.datastore.create_role(name='admin')
            app.security.datastore.create_role(name='user')
            app.security.datastore.create_role(name='service_professional')
            user = app.security.datastore.create_user(name='thanos',
                                                      username='thanos',
                                                      password=generate_password_hash('thanos!@#'))
            app.security.datastore.add_role_to_user(user, role_admin)
            db.session.commit()

    app.register_blueprint(api)

    celery = celery_init_app(app)  
    return app, celery  

def celery_init_app(app):
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"], backend=app.config["CELERY_RESULT_BACKEND"])
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask 
    celery.set_default()
    app.extensions["celery"] = celery  

    celery.conf.timezone = "Asia/Kolkata"  

    return celery


app, celery = create_app()  


celery_app = celery

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=0),  
        daily_reminder.s(),
        name="Daily Reminder Task",
    )
    sender.add_periodic_task(20,
        #crontab(day_of_month=1,hour=7,minute=0),  
        monthly_reminder.s(),
        name="Monthly Reminder Task",
    )

if __name__ == '__main__':
    app.run(debug=True)
