from flask import Blueprint, jsonify, request
from app.models import db, ProjectFund  # Ensure ProjectFund model is imported
from sqlalchemy import Column, Integer, Float, String, Date
from datetime import datetime  # Import datetime module

# Create a Blueprint for Project Fund
project_fund_bp = Blueprint('project_fund', __name__)

# Route to Get All Project Funds
@project_fund_bp.route('/project_fund', methods=['GET'])
def get_project_fund():
    project_funds = ProjectFund.query.all()
    return jsonify([{
        "project_fund_id": fund.project_fund_id,
        "fund_amount": fund.fund_amount,
        "fund_releasing_authority": fund.fund_releasing_authority,
        "project_phase": fund.project_phase,
        "fund_release_date": fund.fund_release_date.strftime('%Y-%m-%d'),  # Format date as string
        "project_id": fund.project_id
    } for fund in project_funds])

# Route to Add a New Project Fund
@project_fund_bp.route('/post/project_fund', methods=['POST'])
def add_project_fund():
    data = request.get_json()
    try:
        new_project_fund = ProjectFund(
            fund_amount=data['fund_amount'],
            fund_releasing_authority=data['fund_releasing_authority'],
            project_phase=data['project_phase'],
            fund_release_date=data['fund_release_date'],
            project_id=data['project_id']
        )
        db.session.add(new_project_fund)
        db.session.commit()
        return jsonify({"message": "Project Fund added successfully!"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# put api to Update a Project Fund
@project_fund_bp.route('/put/project_fund/<int:project_fund_id>', methods=['PUT'])
def update_project_fund(project_fund_id):
    data = request.get_json()
    project_fund = ProjectFund.query.get(project_fund_id)

    if not project_fund:
        return jsonify({"error": "Project Fund not found"}), 404

    try:
        # Update the project fund details
        project_fund.fund_amount = data.get('fund_amount', project_fund.fund_amount)
        project_fund.fund_releasing_authority = data.get('fund_releasing_authority', project_fund.fund_releasing_authority)
        project_fund.project_phase = data.get('project_phase', project_fund.project_phase)
        project_fund.project_id = data.get('project_id', project_fund.project_id)
        
        # Date field requires conversion to proper date format
        fund_release_date = data.get('fund_release_date', None)
        if fund_release_date:
            project_fund.fund_release_date = datetime.strptime(fund_release_date, '%Y-%m-%d').date()
        
        db.session.commit()

        return jsonify({"message": "Project Fund updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    
@project_fund_bp.route('/delete/project_fund/<int:project_fund_id>', methods=['DELETE'])
def delete_project_fund(project_fund_id):
    try:
        # Fetch the project fund by ID
        project_fund = ProjectFund.query.get(project_fund_id)

        if not project_fund:
            return jsonify({"error": "Project Fund not found"}), 404

        # Delete the project fund from the database
        db.session.delete(project_fund)
        db.session.commit()

        return jsonify({"message": f"Project Fund with ID {project_fund_id} deleted successfully!"}), 200
    except Exception as e:
        # If any exception occurs, roll back the transaction and return the error message
        db.session.rollback()
        return jsonify({"error": f"An error occurred while deleting the Project Fund: {str(e)}"}), 500