from flask import Blueprint, jsonify, request
from app.models import db, Admin
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Admin route is working!"})

# Get all admins
@admin_bp.route('/admin', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([{
        "admin_id": admin.admin_id,
        "adminUniqe_id": admin.adminUniqe_id,
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
        "department": admin.department,
        "is_verified": admin.is_verified  # Include is_verified
    } for admin in admins])

# Get a single admin by ID
@admin_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin_by_id(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    return jsonify({
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
        "department": admin.department,
        "is_verified": admin.is_verified  # Include is_verified
    })

# Add a new admin
@admin_bp.route('/post/admin', methods=['POST'])
def add_admin():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    data = request.get_json()

    try:
        new_admin = Admin(
            admin_name=data['admin_name'],
            email=data['email'],
            phone_no=data['phone_no'],
            dob=data.get('dob'),
            address=data.get('address'),
            username=data['username'],
            password=data['password'],
            experience=data.get('experience'),
            account_number=data.get('account_number'),
            security_clearance=data.get('security_clearance'),
            highest_qualification=data.get('highest_qualification'),
            designation=data.get('designation'),
            authority=data['authority'],
            identification=data.get('identification'),
            department=data.get('department'),
            is_verified=data.get('is_verified', False)  # Default to False if not provided
        )

        db.session.add(new_admin)
        db.session.commit()

        new_admin.adminUniqe_id = f"admin_{new_admin.admin_id}"
        db.session.commit()

        return jsonify({
            "message": "Admin added successfully!",
            "adminUniqe_id": new_admin.adminUniqe_id,
            "admin_id": new_admin.admin_id
        }), 201

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Update an existing admin
@admin_bp.route('/admin/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    data = request.get_json()
    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    try:
        admin.admin_name = data.get('admin_name', admin.admin_name)
        admin.email = data.get('email', admin.email)
        admin.phone_no = data.get('phone_no', admin.phone_no)
        admin.dob = data.get('dob', admin.dob)
        admin.address = data.get('address', admin.address)
        admin.username = data.get('username', admin.username)
        admin.password = data.get('password', admin.password)
        admin.experience = data.get('experience', admin.experience)
        admin.account_number = data.get('account_number', admin.account_number)
        admin.security_clearance = data.get('security_clearance', admin.security_clearance)
        admin.highest_qualification = data.get('highest_qualification', admin.highest_qualification)
        admin.designation = data.get('designation', admin.designation)
        admin.authority = data.get('authority', admin.authority)
        admin.identification = data.get('identification', admin.identification)
        admin.department = data.get('department', admin.department)
        admin.is_verified = data.get('is_verified', admin.is_verified)  # Allow updating is_verified

        db.session.commit()
        return jsonify({"message": "Admin updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating admin: {str(e)}"}), 500
