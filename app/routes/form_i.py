from flask import Blueprint, jsonify, request
from app.models import db, FormI  # Ensure FormI is imported correctly

form_i_bp = Blueprint('form_i', __name__)

# Get all Form I entries
@form_i_bp.route('/form-i', methods=['GET'])
def get_all_form_i():
    forms = FormI.query.all()
    return jsonify([form.as_dict() for form in forms]), 200

# Get a single Form I entry by ID
@form_i_bp.route('/form-i/<int:form_id>', methods=['GET'])
def get_form_i_by_id(form_id):
    form = FormI.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form I entry not found'}), 404
    return jsonify(form.as_dict()), 200

# Create a new Form I entry
@form_i_bp.route('/post/form-i', methods=['POST'])
def create_form_i():
    data = request.get_json()
    try:
        new_form = FormI(
            project_id=data['project_id'],
            project_title=data['project_title'],
            principal_agency_name=data.get('principal_agency_name'),
            principal_agency_address=data.get('principal_agency_address'),
            project_leader=data.get('project_leader'),
            sub_agency_name=data.get('sub_agency_name'),
            sub_agency_address=data.get('sub_agency_address'),
            co_investigator=data.get('co_investigator'),
            definition_of_issue=data.get('definition_of_issue'),
            objectives=data.get('objectives'),
            justification=data.get('justification'),
            benefit_to_coal_industry=data.get('benefit_to_coal_industry'),
            work_plan=data.get('work_plan'),
            methodology=data.get('methodology'),
            organization_of_work_elements=data.get('organization_of_work_elements'),
            time_schedule=data.get('time_schedule'),
            land_building_cost=data.get('land_building_cost', 0.0),
            equipment_cost=data.get('equipment_cost', 0.0),
            salary_allowances=data.get('salary_allowances', 0.0),
            consumables_cost=data.get('consumables_cost', 0.0),
            travel_cost=data.get('travel_cost', 0.0),
            workshop_cost=data.get('workshop_cost', 0.0),
            contingency_cost=data.get('contingency_cost', 0.0),
            overheads=data.get('overheads', 0.0),
            taxes=data.get('taxes', 0.0),
            total_cost=data.get('total_cost', 0.0),
            foreign_exchange_component=data.get('foreign_exchange_component'),
            exchange_rate=data.get('exchange_rate', 0.0),
            fund_phasing=data.get('fund_phasing'),
            land_outlay=data.get('land_outlay'),
            equipment_outlay=data.get('equipment_outlay'),
            consumables_outlay=data.get('consumables_outlay'),
            cv_details=data.get('cv_details'),
            past_experience=data.get('past_experience'),
            others=data.get('others')
        )
        db.session.add(new_form)
        db.session.commit()
        return jsonify({'message': 'Form I entry created successfully!', 'id': new_form.id}), 201

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an existing Form I entry
@form_i_bp.route('/put/form-i/<int:form_id>', methods=['PUT'])
def update_form_i(form_id):
    form = FormI.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form I entry not found'}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            if hasattr(form, key):
                setattr(form, key, value)

        db.session.commit()
        return jsonify({'message': 'Form I entry updated successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a Form I entry
@form_i_bp.route('/delete/form-i/<int:form_id>', methods=['DELETE'])
def delete_form_i(form_id):
    form = FormI.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form I entry not found'}), 404

    try:
        db.session.delete(form)
        db.session.commit()
        return jsonify({'message': 'Form I entry deleted successfully!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Helper method to convert model instance to dict
def model_as_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}

FormI.as_dict = model_as_dict
