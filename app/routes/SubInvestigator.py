from flask import Blueprint, jsonify, request
from app.models import db, SubInvestigator
from sqlalchemy.exc import SQLAlchemyError

sub_investigator_bp = Blueprint('sub_investigator', __name__)

# GET route to fetch all sub-investigators
@sub_investigator_bp.route('/sub_investigator', methods=['GET'])
def get_sub_investigators():
    try:
        sub_investigators = SubInvestigator.query.all()
        return jsonify([{
            "sub_investigator_id": si.sub_investigator_id,
            "email": si.email,
            "dob": si.dob.strftime('%Y-%m-%d'),
            "designation": si.designation,
            "department": si.department,
            "identification": si.identification,
            "sub_investigator_name": si.sub_investigator_name,
            "phone_no": si.phone_no,
            "address": si.address,
            "experience": si.experience,
            "highest_qualification": si.highest_qualification
        } for si in sub_investigators]), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# POST route to add a new sub-investigator
@sub_investigator_bp.route('/post/sub_investigator', methods=['POST'])
def add_sub_investigator():
    data = request.get_json()

    # Validate input data
    required_fields = [
        'email', 'dob', 'designation', 'department', 'identification',
        'sub_investigator_name', 'phone_no', 'address', 'experience', 'highest_qualification'
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        new_sub_investigator = SubInvestigator(
            email=data['email'],
            dob=data['dob'],
            designation=data['designation'],
            department=data['department'],
            identification=data['identification'],
            sub_investigator_name=data['sub_investigator_name'],
            phone_no=data['phone_no'],
            address=data['address'],
            experience=data['experience'],
            highest_qualification=data['highest_qualification']
        )
        db.session.add(new_sub_investigator)
        db.session.commit()
        return jsonify({"message": "Sub-Investigator added successfully!"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# PUT route to update a sub-investigator by ID
@sub_investigator_bp.route('/put/sub_investigator/<int:sub_investigator_id>', methods=['PUT'])
def update_sub_investigator(sub_investigator_id):
    data = request.get_json()

    # Fetch the sub-investigator by ID
    sub_investigator = SubInvestigator.query.get(sub_investigator_id)
    if not sub_investigator:
        return jsonify({"error": "Sub-investigator not found"}), 404

    try:
        # Update fields if they are present in the request data
        sub_investigator.sub_investigator_name = data.get('sub_investigator_name', sub_investigator.sub_investigator_name)
        sub_investigator.email = data.get('email', sub_investigator.email)
        sub_investigator.dob = data.get('dob', sub_investigator.dob)
        sub_investigator.designation = data.get('designation', sub_investigator.designation)
        sub_investigator.department = data.get('department', sub_investigator.department)
        sub_investigator.identification = data.get('identification', sub_investigator.identification)
        sub_investigator.phone_no = data.get('phone_no', sub_investigator.phone_no)
        sub_investigator.address = data.get('address', sub_investigator.address)
        sub_investigator.experience = data.get('experience', sub_investigator.experience)
        sub_investigator.highest_qualification = data.get('highest_qualification', sub_investigator.highest_qualification)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Sub-investigator updated successfully!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500    

# DELETE route to remove a sub-investigator by ID
@sub_investigator_bp.route('/delete/sub_investigator/<int:sub_investigator_id>', methods=['DELETE'])
def delete_sub_investigator(sub_investigator_id):
    try:
        # Fetch the sub-investigator by ID
        sub_investigator = SubInvestigator.query.get(sub_investigator_id)
        if not sub_investigator:
            return jsonify({"error": "Sub-investigator not found"}), 404

        # Delete the sub-investigator
        db.session.delete(sub_investigator)
        db.session.commit()

        return jsonify({"message": "Sub-investigator deleted successfully!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@sub_investigator_bp.route('/sub_investigator/<int:sub_investigator_id>', methods=['GET'])
def get_sub_investigator_by_id(sub_investigator_id):
    sub_investigator = SubInvestigator.query.get(sub_investigator_id)
    if not sub_investigator:
        return jsonify({'message': 'SubInvestigator not found'}), 404
    return jsonify({
        'sub_investigator_id': sub_investigator.sub_investigator_id,
        'email': sub_investigator.email,
        'dob': sub_investigator.dob,
        'designation': sub_investigator.designation,
        'department': sub_investigator.department,
        'identification': sub_investigator.identification,
        'sub_investigator_name': sub_investigator.sub_investigator_name,
        'phone_no': sub_investigator.phone_no,
        'address': sub_investigator.address,
        'experience': sub_investigator.experience,
        'highest_qualification': sub_investigator.highest_qualification
    })
