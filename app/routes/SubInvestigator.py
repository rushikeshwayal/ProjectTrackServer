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
