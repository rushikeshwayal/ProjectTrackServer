from flask import Blueprint, jsonify, request
from app.models import db, FormVII

form_vii_bp = Blueprint('form_vii', __name__)

# Get all Form VII entries
@form_vii_bp.route('/form-vii', methods=['GET'])
def get_all_form_vii():
    forms = FormVII.query.all()
    return jsonify([{
        "id": form.id,
        "project_id": form.project_id,
        "principal_agency": form.principal_agency,
        "project_leader": form.project_leader,
        "start_date": form.start_date.strftime('%Y-%m-%d') if form.start_date else None,
        "scheduled_completion_date": form.scheduled_completion_date.strftime('%Y-%m-%d') if form.scheduled_completion_date else None,
        "approved_objectives": form.approved_objectives,
        "approved_work_programme": form.approved_work_programme,
        "work_done_details": form.work_done_details,
        "revised_schedule": form.revised_schedule,
        "extension_time": form.extension_time,
        "extension_reason": form.extension_reason,
        "total_project_cost": form.total_project_cost,
        "actual_expenditure": form.actual_expenditure
    } for form in forms]), 200

# Get Form VII entry by ID
@form_vii_bp.route('/form-vii/<int:form_id>', methods=['GET'])
def get_form_vii_by_id(form_id):
    form = FormVII.query.get(form_id)
    if not form:
        return jsonify({'message': 'Form VII entry not found'}), 404
    return jsonify({
        "id": form.id,
        "project_id": form.project_id,
        "principal_agency": form.principal_agency,
        "project_leader": form.project_leader,
        "start_date": form.start_date.strftime('%Y-%m-%d') if form.start_date else None,
        "scheduled_completion_date": form.scheduled_completion_date.strftime('%Y-%m-%d') if form.scheduled_completion_date else None,
        "approved_objectives": form.approved_objectives,
        "approved_work_programme": form.approved_work_programme,
        "work_done_details": form.work_done_details,
        "revised_schedule": form.revised_schedule,
        "extension_time": form.extension_time,
        "extension_reason": form.extension_reason,
        "total_project_cost": form.total_project_cost,
        "actual_expenditure": form.actual_expenditure
    }), 200

# Create a new Form VII entry
@form_vii_bp.route('/post/form-vii', methods=['POST'])
def create_form_vii():
    data = request.get_json()
    try:
        new_form = FormVII(
            project_id=data['project_id'],
            principal_agency=data['principal_agency'],
            project_leader=data['project_leader'],
            start_date=data.get('start_date'),
            scheduled_completion_date=data.get('scheduled_completion_date'),
            approved_objectives=data.get('approved_objectives'),
            approved_work_programme=data.get('approved_work_programme'),
            work_done_details=data.get('work_done_details'),
            revised_schedule=data.get('revised_schedule'),
            extension_time=data.get('extension_time'),
            extension_reason=data.get('extension_reason'),
            total_project_cost=data.get('total_project_cost', 0.0),
            actual_expenditure=data.get('actual_expenditure', 0.0),
        )
        db.session.add(new_form)
        db.session.commit()
        return jsonify({'message': 'Form VII entry created successfully!', 'id': new_form.id}), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an existing Form VII entry
@form_vii_bp.route('/put/form-vii/<int:form_id>', methods=['PUT'])
def update_form_vii(form_id):
    data = request.get_json()
    form = FormVII.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form VII entry not found'}), 404

    try:
        form.principal_agency = data.get('principal_agency', form.principal_agency)
        form.project_leader = data.get('project_leader', form.project_leader)
        form.start_date = data.get('start_date', form.start_date)
        form.scheduled_completion_date = data.get('scheduled_completion_date', form.scheduled_completion_date)
        form.approved_objectives = data.get('approved_objectives', form.approved_objectives)
        form.approved_work_programme = data.get('approved_work_programme', form.approved_work_programme)
        form.work_done_details = data.get('work_done_details', form.work_done_details)
        form.revised_schedule = data.get('revised_schedule', form.revised_schedule)
        form.extension_time = data.get('extension_time', form.extension_time)
        form.extension_reason = data.get('extension_reason', form.extension_reason)
        form.total_project_cost = data.get('total_project_cost', form.total_project_cost)
        form.actual_expenditure = data.get('actual_expenditure', form.actual_expenditure)

        db.session.commit()
        return jsonify({'message': 'Form VII entry updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
