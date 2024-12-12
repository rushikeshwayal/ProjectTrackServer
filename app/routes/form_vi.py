from flask import Blueprint, jsonify, request
from app.models import db, FormVI

form_vi_bp = Blueprint('form_vi', __name__)

# Get all Form VI entries
@form_vi_bp.route('/form-vi', methods=['GET'])
def get_all_form_vi():
    forms = FormVI.query.all()
    return jsonify([{
        "id": form.id,
        "project_id": form.project_id,
        "title": form.title,
        "start_date": form.start_date.strftime('%Y-%m-%d') if form.start_date else None,
        "approved_completion_date": form.approved_completion_date.strftime('%Y-%m-%d') if form.approved_completion_date else None,
        "actual_completion_date": form.actual_completion_date.strftime('%Y-%m-%d') if form.actual_completion_date else None,
        "objectives": form.objectives,
        "work_programme": form.work_programme,
        "work_done_details": form.work_done_details,
        "objectives_fulfillment": form.objectives_fulfillment,
        "scope_for_further_studies": form.scope_for_further_studies,
        "conclusions": form.conclusions,
        "recommendations": form.recommendations,
        "industry_application_scope": form.industry_application_scope,
        "associated_persons": form.associated_persons,
        "final_expenditure_statement": form.final_expenditure_statement,
    } for form in forms]), 200

# Get Form VI entry by ID
@form_vi_bp.route('/form-vi/<int:form_id>', methods=['GET'])
def get_form_vi_by_id(form_id):
    form = FormVI.query.get(form_id)
    if not form:
        return jsonify({'message': 'Form VI entry not found'}), 404
    return jsonify({
        "id": form.id,
        "project_id": form.project_id,
        "title": form.title,
        "start_date": form.start_date.strftime('%Y-%m-%d') if form.start_date else None,
        "approved_completion_date": form.approved_completion_date.strftime('%Y-%m-%d') if form.approved_completion_date else None,
        "actual_completion_date": form.actual_completion_date.strftime('%Y-%m-%d') if form.actual_completion_date else None,
        "objectives": form.objectives,
        "work_programme": form.work_programme,
        "work_done_details": form.work_done_details,
        "objectives_fulfillment": form.objectives_fulfillment,
        "scope_for_further_studies": form.scope_for_further_studies,
        "conclusions": form.conclusions,
        "recommendations": form.recommendations,
        "industry_application_scope": form.industry_application_scope,
        "associated_persons": form.associated_persons,
        "final_expenditure_statement": form.final_expenditure_statement,
    }), 200

# Create a new Form VI entry
@form_vi_bp.route('/post/form-vi', methods=['POST'])
def create_form_vi():
    data = request.get_json()
    try:
        new_form = FormVI(
            project_id=data['project_id'],
            title=data['title'],
            start_date=data.get('start_date'),
            approved_completion_date=data.get('approved_completion_date'),
            actual_completion_date=data.get('actual_completion_date'),
            objectives=data.get('objectives'),
            work_programme=data.get('work_programme'),
            work_done_details=data.get('work_done_details'),
            objectives_fulfillment=data.get('objectives_fulfillment'),
            scope_for_further_studies=data.get('scope_for_further_studies'),
            conclusions=data.get('conclusions'),
            recommendations=data.get('recommendations'),
            industry_application_scope=data.get('industry_application_scope'),
            associated_persons=data.get('associated_persons'),
            final_expenditure_statement=data.get('final_expenditure_statement'),
        )
        db.session.add(new_form)
        db.session.commit()
        return jsonify({'message': 'Form VI entry created successfully!', 'id': new_form.id}), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an existing Form VI entry
@form_vi_bp.route('/put/form-vi/<int:form_id>', methods=['PUT'])
def update_form_vi(form_id):
    data = request.get_json()
    form = FormVI.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form VI entry not found'}), 404

    try:
        form.title = data.get('title', form.title)
        form.start_date = data.get('start_date', form.start_date)
        form.approved_completion_date = data.get('approved_completion_date', form.approved_completion_date)
        form.actual_completion_date = data.get('actual_completion_date', form.actual_completion_date)
        form.objectives = data.get('objectives', form.objectives)
        form.work_programme = data.get('work_programme', form.work_programme)
        form.work_done_details = data.get('work_done_details', form.work_done_details)
        form.objectives_fulfillment = data.get('objectives_fulfillment', form.objectives_fulfillment)
        form.scope_for_further_studies = data.get('scope_for_further_studies', form.scope_for_further_studies)
        form.conclusions = data.get('conclusions', form.conclusions)
        form.recommendations = data.get('recommendations', form.recommendations)
        form.industry_application_scope = data.get('industry_application_scope', form.industry_application_scope)
        form.associated_persons = data.get('associated_persons', form.associated_persons)
        form.final_expenditure_statement = data.get('final_expenditure_statement', form.final_expenditure_statement)

        db.session.commit()
        return jsonify({'message': 'Form VI entry updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
