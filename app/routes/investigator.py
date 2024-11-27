from flask import Blueprint, jsonify, request
from app.models import db , Investigator

investigator_bp = Blueprint('investigator', __name__)
# @admin_bp.route('/test', methods=['GET'])
# def test_route():
#     return jsonify({"message": "Admin route is working!"})

@investigator_bp.route('/investigator', methods=['GET'])
def get_investigators():
    investigators = Investigator.query.all()
    return jsonify([{
        "investigator_id": investigator.investigator_id,
        "investigator_name": investigator.investigator_name,
        "email": investigator.email,
        "phone_no": investigator.phone_no, 
        "dob": investigator.dob,
        "address": investigator.address,
        "username": investigator.username,
        "password": investigator.password,
        "experience": investigator.experience,
        "account_number": investigator.account_number,
        "security_clearance": investigator.security_clearance,
        "highest_qualification": investigator.highest_qualification,
        "designation": investigator.designation,
        "authority": investigator.authority,
        "identification": investigator.identification,
        "department": investigator.department
    } for investigator in investigators])


# @i.route('/investigator', methods=['GET'])
# def get_admins():
#     admins = Admin.query.all()
#     return jsonify([{
#         "admin_id": admin.admin_id,
#         "admin_name": admin.admin_name,
#         "email": admin.email,
#         "phone_no": admin.phone_no, 
#         "dob": admin.dob,
#         "address": admin.address,
#         "username": admin.username,
#         "password": admin.password,
#         "experience": admin.experience,
#         "account_number": admin.account_number,
#         "security_clearance": admin.security_clearance,
#         "highest_qualification": admin.highest_qualification,
#         "designation": admin.designation,
#         "authority": admin.authority,
#         "identification": admin.identification,
#         "department": admin.department
#     } for admin in admins])
     
   