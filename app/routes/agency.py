from flask import Blueprint, jsonify, request
from app.models import db , Agency

agency_bp = Blueprint('agency', __name__)
#get
@agency_bp.route('/agency', methods=['GET'])
def get_agency():
    agencies = Agency.query.all()
    return jsonify([{
        "agency_id": agency.agency_id,
        "agency_name": agency.agency_name,
        "agency_professionals": agency.agency_professionals,
        "agency_address": agency.address,
        "agency_phone_no": agency.phone_no,
        "agency_email": agency.email,
        "agency_ceo": agency.ceo,
        "agency_established_date": agency.established_date,
    } for agency in agencies])
#post
@agency_bp.route('/post/agency', methods=['POST'])
def add_agency():
    data = request.get_json()
    new_agency = Agency(
        agency_name=data['agency_name'],
        phone_no=data['phone_no'],
        email=data['email'],
        agency_professionals=data['agency_professionals'],
        ceo=data['ceo'],
        address=data['address'],
        established_date=data['established_date']
    )
    db.session.add(new_agency)
    db.session.commit()
    return jsonify({"message": "Agency added successfully!"})

#put
@agency_bp.route('/put/agency/<int:agency_id>', methods=['PUT'])
def update_agency(agency_id):
    data = request.get_json()
    agency = Agency.query.get(agency_id)

    if not agency:
        return jsonify({"error": "Agency not found"}), 404

    try:
        agency.agency_name = data.get('agency_name', agency.agency_name)
        agency.phone_no = data.get('phone_no', agency.phone_no)
        agency.email = data.get('email', agency.email)
        agency.agency_professionals = data.get('agency_professionals', agency.agency_professionals)
        agency.ceo = data.get('ceo', agency.ceo)
        agency.address = data.get('address', agency.address)
        agency.established_date = data.get('established_date', agency.established_date)

        db.session.commit()
        return jsonify({"message": "Agency updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
#delete
@agency_bp.route('/delete/agency/<int:agency_id>', methods=['DELETE'])
def delete_agency(agency_id):
    agency = Agency.query.get(agency_id)

    if not agency:
        return jsonify({"error": "Agency not found"}), 404

    try:
        db.session.delete(agency)
        db.session.commit()
        return jsonify({"message": "Agency deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@agency_bp.route('/agency/<int:agency_id>', methods=['GET'])
def get_agency_by_id(agency_id):
    agency = Agency.query.get(agency_id)
    if not agency:
        return jsonify({'message': 'Agency not found'}), 404
    return jsonify({
        'agency_id': agency.agency_id,
        'agency_name': agency.agency_name,
        'phone_no': agency.phone_no,
        'email': agency.email,
        'agency_professionals': agency.agency_professionals,
        'ceo': agency.ceo,
        'address': agency.address,
        'established_date': agency.established_date
    })

    

        



