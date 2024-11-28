from flask import Blueprint, jsonify, request
from app.models import db, ProjectFund  # Ensure ProjectFund model is imported
from sqlalchemy import Column, Integer, Float, String, Date

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
        "fund_release_date": fund.fund_release_date.strftime('%Y-%m-%d')  # Format date as string
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
            fund_release_date=data['fund_release_date']
        )
        db.session.add(new_project_fund)
        db.session.commit()
        return jsonify({"message": "Project Fund added successfully!"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500