from flask import Blueprint, jsonify, request
from app.models import db, SubAgency
from sqlalchemy.exc import SQLAlchemyError

sub_agency_bp = Blueprint('sub_agency', __name__)

# GET route to fetch all sub-agencies
@sub_agency_bp.route('/sub_agency', methods=['GET'])
def get_sub_agencies():
    try:
        sub_agencies = SubAgency.query.all()
        return jsonify([{
            "sub_agency_id": sa.sub_agency_id,
            "sub_agency_name": sa.sub_agency_name,
            "phone_no": sa.phone_no,
            "email": sa.email,
            "sub_agency_professionals": sa.sub_agency_professionals,
            "head_of_agency": sa.head_of_agency,
            "address": sa.address,
            "established_date": sa.established_date.strftime('%Y-%m-%d')
        } for sa in sub_agencies]), 200

    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# POST route to add a new sub-agency
@sub_agency_bp.route('/post/sub_agency', methods=['POST'])
def add_sub_agency():
    data = request.get_json()

    # Validate input data
    required_fields = [
        'sub_agency_name', 'phone_no', 'email', 'sub_agency_professionals',
        'head_of_agency', 'address', 'established_date'
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        new_sub_agency = SubAgency(
            sub_agency_name=data['sub_agency_name'],
            phone_no=data['phone_no'],
            email=data['email'],
            sub_agency_professionals=data['sub_agency_professionals'],
            head_of_agency=data['head_of_agency'],
            address=data['address'],
            established_date=data['established_date']
        )
        db.session.add(new_sub_agency)
        db.session.commit()
        return jsonify({"message": "Sub-Agency added successfully!"}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500