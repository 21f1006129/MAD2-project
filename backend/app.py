
from flask import Flask

from flask_security import SQLAlchemyUserDatastore, Security

from application.models import db,User,RoleUsers, Role
from application.routes import api
from werkzeug.security import generate_password_hash
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'ringostarmccourtneypaul'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.sqlite3" 

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
            user  = app.security.datastore.create_user(name = 'thanos',
                                                       username='thanos',
                                                        password=generate_password_hash('thanos!@#'))
            
            app.security.datastore.add_role_to_user(user, role_admin)
            db.session.commit()

    app.register_blueprint(api)

    return app

app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)