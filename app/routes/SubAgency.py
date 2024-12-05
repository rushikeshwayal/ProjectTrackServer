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
    
    
# PUT route to update an existing sub-agency
@sub_agency_bp.route('/put/sub_agency/<int:sub_agency_id>', methods=['PUT'])
def update_sub_agency(sub_agency_id):
    data = request.get_json()

    # Retrieve the sub-agency to update
    sub_agency = SubAgency.query.get(sub_agency_id)
    if not sub_agency:
        return jsonify({"error": "Sub-agency not found"}), 404

    # Validate input data
    required_fields = [
        'sub_agency_name', 'phone_no', 'email', 'sub_agency_professionals',
        'head_of_agency', 'address', 'established_date'
    ]
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

    try:
        # Update the sub-agency details
        sub_agency.sub_agency_name = data.get('sub_agency_name', sub_agency.sub_agency_name)
        sub_agency.phone_no = data.get('phone_no', sub_agency.phone_no)
        sub_agency.email = data.get('email', sub_agency.email)
        sub_agency.sub_agency_professionals = data.get('sub_agency_professionals', sub_agency.sub_agency_professionals)
        sub_agency.head_of_agency = data.get('head_of_agency', sub_agency.head_of_agency)
        sub_agency.address = data.get('address', sub_agency.address)
        sub_agency.established_date = data.get('established_date', sub_agency.established_date)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Sub-agency updated successfully!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    
# DELETE route to delete an existing sub-agency
@sub_agency_bp.route('/delete/sub_agency/<int:sub_agency_id>', methods=['DELETE'])
def delete_sub_agency(sub_agency_id):
    try:
        # Retrieve the sub-agency to delete
        sub_agency = SubAgency.query.get(sub_agency_id)
        if not sub_agency:
            return jsonify({"error": "Sub-agency not found"}), 404

        # Delete the sub-agency from the database
        db.session.delete(sub_agency)
        db.session.commit()

        return jsonify({"message": "Sub-agency deleted successfully!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@sub_agency_bp.route('/sub_agency/<int:sub_agency_id>', methods=['GET'])
def get_sub_agency_by_id(sub_agency_id):
    sub_agency = SubAgency.query.get(sub_agency_id)
    if not sub_agency:
        return jsonify({'message': 'SubAgency not found'}), 404
    return jsonify({
        'sub_agency_id': sub_agency.sub_agency_id,
        'sub_agency_name': sub_agency.sub_agency_name,
        'phone_no': sub_agency.phone_no,
        'email': sub_agency.email,
        'sub_agency_professionals': sub_agency.sub_agency_professionals,
        'head_of_agency': sub_agency.head_of_agency,
        'address': sub_agency.address,
        'established_date': sub_agency.established_date
    })
