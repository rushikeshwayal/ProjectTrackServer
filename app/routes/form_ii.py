from flask import Blueprint, jsonify, request
from app.models import db, FormII  # Ensure FormII is imported correctly

form_ii_bp = Blueprint('form_ii', __name__)

# Get all Form II entries
@form_ii_bp.route('/form-ii', methods=['GET'])
def get_all_form_ii():
    forms = FormII.query.all()
    return jsonify([form.as_dict() for form in forms]), 200

# Get a single Form II entry by ID
@form_ii_bp.route('/form-ii/<int:form_id>', methods=['GET'])
def get_form_ii_by_id(form_id):
    form = FormII.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form II entry not found'}), 404
    return jsonify(form.as_dict()), 200

# Create a new Form II entry
@form_ii_bp.route('/post/form-ii', methods=['POST'])
def create_form_ii():
    data = request.get_json()
    try:
        new_form = FormII(
            project_id=data['project_id'],
            project_code=data['project_code'],
            company_name=data['company_name'],
            year_or_period=data['year_or_period'],
            total_approved_cost=data['total_approved_cost'],
            total_fund_received=data['total_fund_received'],
            interest_earned=data.get('interest_earned', 0.0),
            expenditure_incurred=data['expenditure_incurred'],
            balance_fund_available=data['balance_fund_available'],
            fund_provision=data['fund_provision'],
            fund_required=data['fund_required'],
            land_building=data.get('land_building', 0.0),
            capital_equipment=data.get('capital_equipment', 0.0),
            manpower=data.get('manpower', 0.0),
            consumables=data.get('consumables', 0.0),
            travel=data.get('travel', 0.0),
            contingencies=data.get('contingencies', 0.0),
            workshop_seminar=data.get('workshop_seminar', 0.0),
            associate_finance_officer=data['associate_finance_officer'],
            project_leader=data['project_leader'],
            signature_finance_officer=data['signature_finance_officer'],
            signature_project_leader=data['signature_project_leader']
        )
        db.session.add(new_form)
        db.session.commit()
        return jsonify({'message': 'Form II entry created successfully!', 'id': new_form.id}), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an existing Form II entry
@form_ii_bp.route('/put/form-ii/<int:form_id>', methods=['PUT'])
def update_form_ii(form_id):
    form = FormII.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form II entry not found'}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            if hasattr(form, key):
                setattr(form, key, value)

        db.session.commit()
        return jsonify({'message': 'Form II entry updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a Form II entry
@form_ii_bp.route('/delete/form-ii/<int:form_id>', methods=['DELETE'])
def delete_form_ii(form_id):
    form = FormII.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form II entry not found'}), 404

    try:
        db.session.delete(form)
        db.session.commit()
        return jsonify({'message': 'Form II entry deleted successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
