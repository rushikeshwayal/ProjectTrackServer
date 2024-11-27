from flask import Blueprint, jsonify, request
from app.models import db , Agency

agency_bp = Blueprint('agency', __name__)

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


        



