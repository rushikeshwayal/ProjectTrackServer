from flask import Blueprint, jsonify, request
from app.models import db, FundUtilization  # Ensure FundUtilization model is imported
from datetime import datetime

# Create a Blueprint for Fund Utilization
fund_utilization_bp = Blueprint('fund_utilization', __name__)

# Route to Get All Fund Utilizations
@fund_utilization_bp.route('/fund_utilization', methods=['GET'])
def get_fund_utilization():
    try:
        fund_utilizations = FundUtilization.query.all()
        return jsonify([{
            "utilization_id": fund.utilization_id,
            "project_id": fund.project_id,
            "submission_date": fund.submission_date.strftime('%Y-%m-%d'),
            "utilized_amount": fund.utilized_amount,
            "quarter": fund.quarter,
            "agency_name": fund.agency_name,
            "budget_head": fund.budget_head
        } for fund in fund_utilizations]), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to Get Fund Utilization by Project ID
@fund_utilization_bp.route('/fund_utilization/<int:project_id>', methods=['GET'])
def get_fund_utilization_by_project_id(project_id):
    try:
        fund_utilizations = FundUtilization.query.filter_by(project_id=project_id).all()
        if not fund_utilizations:
            return jsonify({"error": "No fund utilization records found for the given project_id"}), 404

        return jsonify([{
            "utilization_id": fund.utilization_id,
            "project_id": fund.project_id,
            "submission_date": fund.submission_date.strftime('%Y-%m-%d'),
            "utilized_amount": fund.utilized_amount,
            "quarter": fund.quarter,
            "agency_name": fund.agency_name,
            "budget_head": fund.budget_head
        } for fund in fund_utilizations]), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to Add a New Fund Utilization
@fund_utilization_bp.route('/post/fund_utilization', methods=['POST'])
def add_fund_utilization():
    data = request.get_json()
    try:
        new_fund_utilization = FundUtilization(
            project_id=data['project_id'],
            submission_date=datetime.strptime(data['submission_date'], '%Y-%m-%d').date(),
            utilized_amount=data['utilized_amount'],
            quarter=data['quarter'],
            agency_name=data['agency_name'],
            budget_head=data['budget_head']
        )
        db.session.add(new_fund_utilization)
        db.session.commit()
        return jsonify({"message": "Fund Utilization record added successfully!"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to Update Fund Utilization
@fund_utilization_bp.route('/put/fund_utilization/<int:utilization_id>/<int:project_id>', methods=['PUT'])
def update_fund_utilization(utilization_id, project_id):
    # Fetch the record using the composite key
    fund_utilization = FundUtilization.query.get((utilization_id, project_id))
    
    if not fund_utilization:
        return jsonify({"error": "Fund Utilization record not found"}), 404

    # Example: Update fields based on JSON request data
    data = request.get_json()
    fund_utilization.utilized_amount = data.get('utilized_amount', fund_utilization.utilized_amount)
    fund_utilization.agency_name = data.get('agency_name', fund_utilization.agency_name)

    db.session.commit()
    return jsonify({"message": "Fund Utilization updated successfully"})


# Route to Delete Fund Utilization
@fund_utilization_bp.route('/delete/fund_utilization/<int:utilization_id>/<int:project_id>', methods=['DELETE'])
def delete_fund_utilization(utilization_id, project_id):
    # Fetch the record using composite key
    fund_utilization = FundUtilization.query.get((utilization_id, project_id))
    
    if not fund_utilization:
        return jsonify({"error": "Fund Utilization record not found"}), 404

    # Delete the record
    db.session.delete(fund_utilization)
    db.session.commit()

    return jsonify({"message": "Fund Utilization record deleted successfully"}), 200
