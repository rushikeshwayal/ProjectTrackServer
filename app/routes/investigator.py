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
        "investigatorUniqe_id":investigator.investigatorUniqe_id,
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


@investigator_bp.route('/post/investigator', methods=['POST'])
def add_investigator():
    if request.method == 'OPTIONS':
        # CORS preflight response
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    data = request.get_json()
    
    try:
        # Create a new Investigator instance with data from the request
        new_investigator = Investigator(
            investigator_name=data['investigator_name'],
            email=data['email'],
            phone_no=data['phone_no'],
            dob=data['dob'],
            address=data['address'],
            username=data['username'],
            password=data['password'],
            experience=data['experience'],
            account_number=data['account_number'],
            security_clearance=data.get('security_clearance'),  # Optional field
            highest_qualification=data['highest_qualification'],
            designation=data['designation'],
            authority=data['authority'],
            identification=data['identification'],
            department=data['department']
        )

        # Add the new investigator to the database
        db.session.add(new_investigator)
        db.session.commit()  # Commit to generate the investigator_id

        # Assign the investigatorUniqe_id after the investigator_id is generated
        new_investigator.investigatorUniqe_id = f"investigator_{new_investigator.investigator_id}"
        db.session.commit()  # Commit again to save the updated investigatorUniqe_id

        # Return success response
        return jsonify({
            "message": "Investigator added successfully!",
            "investigatorUniqe_id": new_investigator.investigatorUniqe_id,
            "investigator_id": new_investigator.investigator_id
        }), 201

    except KeyError as e:
        # Handle missing fields
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        # Rollback on error and log the error for debugging
        db.session.rollback()
        print(f"Error occurred: {str(e)}")  # This will help log the error
        return jsonify({"error": str(e)}), 500

    


#put api    
@investigator_bp.route('/put/investigator/<int:investigator_id>', methods=['PUT'])
def update_investigator(investigator_id):
    data = request.get_json()
    investigator = Investigator.query.get(investigator_id)

    if not investigator:
        return jsonify({"error": "Investigator not found"}), 404

    try:
        # Update investigator details with provided data or keep existing values
        investigator.investigator_name = data.get('investigator_name', investigator.investigator_name)
        investigator.email = data.get('email', investigator.email)
        investigator.phone_no = data.get('phone_no', investigator.phone_no)
        investigator.dob = data.get('dob', investigator.dob)
        investigator.address = data.get('address', investigator.address)
        investigator.username = data.get('username', investigator.username)
        investigator.password = data.get('password', investigator.password)
        investigator.experience = data.get('experience', investigator.experience)
        investigator.account_number = data.get('account_number', investigator.account_number)
        investigator.security_clearance = data.get('security_clearance', investigator.security_clearance)
        investigator.highest_qualification = data.get('highest_qualification', investigator.highest_qualification)
        investigator.designation = data.get('designation', investigator.designation)
        investigator.authority = data.get('authority', investigator.authority)
        investigator.identification = data.get('identification', investigator.identification)
        investigator.department = data.get('department', investigator.department)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Investigator updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
 #delete api   
@investigator_bp.route('/delete/investigator/<int:investigator_id>', methods=['DELETE'])
def delete_investigator(investigator_id):
    investigator = Investigator.query.get(investigator_id)

    if not investigator:
        return jsonify({"error": "Investigator not found"}), 404

    try:
        # Delete the investigator from the database
        db.session.delete(investigator)
        db.session.commit()
        return jsonify({"message": "Investigator deleted successfully!"}), 200

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


@investigator_bp.route('/investigator/<int:investigator_id>', methods=['GET'])
def get_investigator_by_id(investigator_id):
    investigator = Investigator.query.get(investigator_id)
    if not investigator:
        return jsonify({'message': 'Investigator not found'}), 404
    return jsonify({
        'investigator_id': investigator.investigator_id,
        'email': investigator.email,
        'username': investigator.username,
        'dob': investigator.dob,
        'designation': investigator.designation,
        'department': investigator.department,
        'identification': investigator.identification,
        'investigator_name': investigator.investigator_name,
        'phone_no': investigator.phone_no,
        'address': investigator.address,
        'experience': investigator.experience,
        'account_number': investigator.account_number,
        'security_clearance': investigator.security_clearance,
        'authority': investigator.authority,
        'highest_qualification': investigator.highest_qualification
    })
