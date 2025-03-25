from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin


db = SQLAlchemy()



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def get_role(self):
        return [role.name for role in self.roles]

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class RoleUsers(db.Model):
    __tablename__ ='roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey(User.id))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey(Role.id))

class Customer(db.Model):
    __tablename__='customer'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    active = db.Column(db.Boolean())
class Serviceprofessional(db.Model):
    __tablename__='service_professional'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(), unique=True, nullable=False)
    pincode = db.Column(db.Integer())
    date_created = db.Column(db.DateTime())
    service_type = db.Column(db.String(), nullable=False)
    experience = db.Column(db.Integer())
    requests_completed = db.Column(db.Integer())
    cumulative_rating = db.Column(db.Integer())
    active = db.Column(db.Boolean())
    requests_on_date = db.relationship('Servicerequest', backref='professional', lazy=True)

class Service(db.Model):
    __tablename__='service'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(),nullable=False)
    description = db.Column(db.String())

class Servicerequest(db.Model):
    __tablename__ = 'service_request'
    id = db.Column(db.Integer(), primary_key=True)
    service_id  = db.Column('service_id',db.Integer(), db.ForeignKey(Service.id))
    service_name  = db.Column('service_name',db.String(), db.ForeignKey(Service.name))
    user_id = db.Column('user_id',db.Integer(), db.ForeignKey(User.id))
    professional_id = db.Column('professional_id',db.Integer(), db.ForeignKey(Serviceprofessional.id),nullable=True)
    total_amount = db.Column(db.Integer())
    address = db.Column(db.String(200))
    pincode = db.Column(db.Integer())
    date_of_request = db.Column(db.Date())
    date_of_completion = db.Column(db.Date())
    service_status = db.Column(db.String(),default="pending")
    rejected_by = db.Column(db.JSON(), default=list)
    rating = db.Column(db.Integer())
    feedback = db.Column(db.String(200))
