from flask import Blueprint, request, jsonify
from app.models import db, FormVIII

form_viii_bp = Blueprint('form_viii', __name__)

# Create a new FormVIII entry
@form_viii_bp.route('/post/form-viii', methods=['POST'])
def create_form_viii():
    data = request.get_json()
    try:
        # Create a new FormVIII instance
        new_form_viii = FormVIII(
            project_id=data['project_id'],
            project_name=data['project_name'],
            project_code=data['project_code'],
            principal_agency_name=data.get('principal_agency_name'),
            sub_implementing_agency_name=data.get('sub_implementing_agency_name'),
            project_leader=data.get('project_leader'),
            project_start_date=data.get('project_start_date'),
            scheduled_completion_date=data.get('scheduled_completion_date'),
            approved_objectives=data.get('approved_objectives'),
            approved_work_programme=data.get('approved_work_programme'),
            work_done_details=data.get('work_done_details'),
            total_approved_cost=data.get('total_approved_cost'),
            revised_cost=data.get('revised_cost'),
            justification_for_revision=data.get('justification_for_revision'),
            revised_time_schedule=data.get('revised_time_schedule'),
            actual_expenditure_till_last_quarter=data.get('actual_expenditure_till_last_quarter'),
            associate_finance_officer_signature=data.get('associate_finance_officer_signature'),
            project_leader_signature=data.get('project_leader_signature'),
            comments=data.get('comments')
        )

        db.session.add(new_form_viii)
        db.session.commit()
        return jsonify({'message': 'Form VIII entry created successfully!', 'id': new_form_viii.id}), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Get all FormVIII entries
@form_viii_bp.route('/form-viii', methods=['GET'])
def get_all_form_viii():
    forms = FormVIII.query.all()
    return jsonify([form.as_dict() for form in forms]), 200

# Get FormVIII entry by ID
@form_viii_bp.route('/form-viii/<int:form_id>', methods=['GET'])
def get_form_viii_by_id(form_id):
    form = FormVIII.query.get(form_id)
    if not form:
        return jsonify({'message': 'Form VIII entry not found'}), 404
    return jsonify(form.as_dict()), 200

# Update an existing FormVIII entry
@form_viii_bp.route('/put/form-viii/<int:form_id>', methods=['PUT'])
def update_form_viii(form_id):
    data = request.get_json()
    form = FormVIII.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form VIII entry not found'}), 404

    try:
        for key, value in data.items():
            if hasattr(form, key):
                setattr(form, key, value)

        db.session.commit()
        return jsonify({'message': 'Form VIII entry updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Delete a FormVIII entry
@form_viii_bp.route('/delete/form-viii/<int:form_id>', methods=['DELETE'])
def delete_form_viii(form_id):
    form = FormVIII.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form VIII entry not found'}), 404

    try:
        db.session.delete(form)
        db.session.commit()
        return jsonify({'message': 'Form VIII entry deleted successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500