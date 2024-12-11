from flask import Blueprint, jsonify, request
from app.models import db, BankDetails, Investigator

bank_details_bp = Blueprint('bank_details', __name__)

# Get all bank details
@bank_details_bp.route('/bank-details', methods=['GET'])
def get_bank_details():
    bank_details = BankDetails.query.all()
    return jsonify([{
        "bank_id": bank.bank_id,
        "investigator_id": bank.investigator_id,
        "bank_name": bank.bank_name,
        "account_holder_name": bank.account_holder_name,
        "account_number": bank.account_number,
        "ifsc_code": bank.ifsc_code,
        "branch_name": bank.branch_name,
        "branch_address": bank.branch_address,
        "email": bank.email,
        "phone_number": bank.phone_number,
    } for bank in bank_details]), 200

# Get bank details by bank_id
@bank_details_bp.route('/bank-details/<int:bank_id>', methods=['GET'])
def get_bank_details_by_id(bank_id):
    bank = BankDetails.query.get(bank_id)
    if not bank:
        return jsonify({'message': 'Bank details not found'}), 404
    return jsonify({
        "bank_id": bank.bank_id,
        "investigator_id": bank.investigator_id,
        "bank_name": bank.bank_name,
        "account_holder_name": bank.account_holder_name,
        "account_number": bank.account_number,
        "ifsc_code": bank.ifsc_code,
        "branch_name": bank.branch_name,
        "branch_address": bank.branch_address,
        "email": bank.email,
        "phone_number": bank.phone_number,
    }), 200

# Add new bank details
@bank_details_bp.route('/post/bank-details', methods=['POST'])
def add_bank_details():
    data = request.get_json()
    try:
        # Create a new BankDetails instance with data from the request
        new_bank = BankDetails(
            investigator_id=data['investigator_id'],
            bank_name=data['bank_name'],
            account_holder_name=data['account_holder_name'],
            account_number=data['account_number'],
            ifsc_code=data['ifsc_code'],
            branch_name=data['branch_name'],
            branch_address=data.get('branch_address', None),
            email=data['email'],
            phone_number=data.get('phone_number', None),
        )

        # Add the new bank details to the database
        db.session.add(new_bank)
        db.session.commit()  # Commit to generate the bank_id

        return jsonify({
            "message": "Bank details added successfully!",
            "bank_id": new_bank.bank_id
        }), 201
    
    except KeyError as e:
        # Handle missing fields
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Update bank details by bank_id
@bank_details_bp.route('/put/bank-details/<int:bank_id>', methods=['PUT'])
def update_bank_details(bank_id):
    data = request.get_json()
    bank = BankDetails.query.get(bank_id)

    if not bank:
        return jsonify({"error": "Bank details not found"}), 404

    try:
        # Update fields if provided
        bank.bank_name = data.get('bank_name', bank.bank_name)
        bank.account_holder_name = data.get('account_holder_name', bank.account_holder_name)
        bank.account_number = data.get('account_number', bank.account_number)
        bank.ifsc_code = data.get('ifsc_code', bank.ifsc_code)
        bank.branch_name = data.get('branch_name', bank.branch_name)
        bank.branch_address = data.get('branch_address', bank.branch_address)
        bank.email = data.get('email', bank.email)
        bank.phone_number = data.get('phone_number', bank.phone_number)

        # Commit changes to the database
        db.session.commit()
        return jsonify({"message": "Bank details updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete bank details by bank_id
@bank_details_bp.route('/delete/bank-details/<int:bank_id>', methods=['DELETE'])
def delete_bank_details(bank_id):
    bank = BankDetails.query.get(bank_id)

    if not bank:
        return jsonify({"error": "Bank details not found"}), 404

    try:
        db.session.delete(bank)
        db.session.commit()
        return jsonify({"message": "Bank details deleted successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
       