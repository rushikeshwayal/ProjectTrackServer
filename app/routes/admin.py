from flask import Blueprint, jsonify, request
from app.models import db, Admin , Investigator

admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Admin route is working!"})

@admin_bp.route('/admin', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([{
        "admin_id": admin.admin_id,
        "admin_name": admin.admin_name,
        "email": admin.email,
        "phone_no": admin.phone_no, 
        "dob": admin.dob,
        "address": admin.address,
        "username": admin.username,
        "password": admin.password,
        "experience": admin.experience,
        "account_number": admin.account_number,
        "security_clearance": admin.security_clearance,
        "highest_qualification": admin.highest_qualification,
        "designation": admin.designation,
        "authority": admin.authority,
        "identification": admin.identification,
        "department": admin.department
    } for admin in admins])
     
   