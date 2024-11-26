from flask import Blueprint, jsonify, request
from app.models import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "access": user.access
    } for user in users])

@user_bp.route('/create/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        access=data['access']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201
