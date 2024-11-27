from sqlalchemy import Column, Integer, String, Date
from app.extensions import db

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50))
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(255))  # Store hashed passwords
#     access = db.Column(db.String(50))  # Access level

class Admin(db.Model):
    __tablename__ = 'admins'

    admin_id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    experience = db.Column(db.String(50), nullable=True)
    account_number = db.Column(db.String(20), nullable=True)
    security_clearance = db.Column(db.String(50), nullable=True)
    highest_qualification = db.Column(db.String(50), nullable=True)
    designation = db.Column(db.String(50), nullable=True)
    authority = db.Column(db.String(20), nullable=False)
    identification = db.Column(db.String(50), nullable=True)
    department = db.Column(db.String(50), nullable=True)
