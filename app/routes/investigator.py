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


@investigator_bp.route('/put/investigator/<int:investigator_id>', methods=['PUT'])
def investigatorput(investigator_id):
    data = request.get_json()
    investigator = Investigator.query.get(investigator_id)

    if not investigator:
        return jsonify({"error": "Investigator not found"}), 404

    try:
        # Update fields if provided
        investigator.email = data.get('email', investigator.email)
        investigator.username = data.get('username', investigator.username)
        investigator.password = data.get('password', investigator.password)
        investigator.dob = data.get('dob', investigator.dob)
        investigator.designation = data.get('designation', investigator.designation)
        investigator.department = data.get('department', investigator.department)
        investigator.identification = data.get('identification', investigator.identification)
        investigator.investigator_name = data.get('investigator_name', investigator.investigator_name)
        investigator.phone_no = data.get('phone_no', investigator.phone_no)
        investigator.address = data.get('address', investigator.address)
        investigator.experience = data.get('experience', investigator.experience)
        investigator.account_number = data.get('account_number', investigator.account_number)
        investigator.security_clearance = data.get('security_clearance', investigator.security_clearance)
        investigator.authority = data.get('authority', investigator.authority)
        investigator.highest_qualification = data.get('highest_qualification', investigator.highest_qualification)

        db.session.commit()
        return jsonify({"message": "Investigator updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


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
     
   