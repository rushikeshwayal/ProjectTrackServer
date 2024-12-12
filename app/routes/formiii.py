from flask import Blueprint, jsonify, request
from app.models import db, FormIII
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

# Create Blueprint for FormIII
form_iii_bp = Blueprint('form_iii', __name__)

# Route to get all Form III records
@form_iii_bp.route('/form_iii', methods=['GET'])
def get_form_iii():
    try:
        form_iii_records = FormIII.query.all()
        return jsonify([{
            'id': form.id,
            'project_id': form.project_id,
            'quarter_end_date': form.quarter_end_date.strftime('%Y-%m-%d'),
            'land_building_cost': form.land_building_cost,
            'capital_equipment_cost': form.capital_equipment_cost,
            'manpower_cost': form.manpower_cost,
            'consumable_cost': form.consumable_cost,
            'ta_da_cost': form.ta_da_cost,
            'contingencies_cost': form.contingencies_cost,
            'seminar_cost': form.seminar_cost,
            'other_costs': form.other_costs,
            'funds_advanced': form.funds_advanced,
            'expenditure_incurred': form.expenditure_incurred,
            'unspent_balance': form.unspent_balance
        } for form in form_iii_records]), 200
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Route to get a specific Form III record by its ID
@form_iii_bp.route('/form_iii/<int:id>', methods=['GET'])
def get_form_iii_by_id(id):
    try:
        form_iii = FormIII.query.get(id)
        if not form_iii:
            return jsonify({"error": "Form III record not found"}), 404
        return jsonify({
            'id': form_iii.id,
            'project_id': form_iii.project_id,
            'quarter_end_date': form_iii.quarter_end_date.strftime('%Y-%m-%d'),
            'land_building_cost': form_iii.land_building_cost,
            'capital_equipment_cost': form_iii.capital_equipment_cost,
            'manpower_cost': form_iii.manpower_cost,
            'consumable_cost': form_iii.consumable_cost,
            'ta_da_cost': form_iii.ta_da_cost,
            'contingencies_cost': form_iii.contingencies_cost,
            'seminar_cost': form_iii.seminar_cost,
            'other_costs': form_iii.other_costs,
            'funds_advanced': form_iii.funds_advanced,
            'expenditure_incurred': form_iii.expenditure_incurred,
            'unspent_balance': form_iii.unspent_balance
        }), 200
    except NoResultFound:
        return jsonify({"error": "Form III record not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Route to create a new Form III record
@form_iii_bp.route('/post/form_iii', methods=['POST'])
def add_form_iii():
    data = request.get_json()
    try:
        # Create a new FormIII instance
        new_form_iii = FormIII(
            project_id=data['project_id'],
            quarter_end_date=datetime.strptime(data['quarter_end_date'], '%Y-%m-%d').date(),
            land_building_cost=data.get('land_building_cost', 0.0),
            capital_equipment_cost=data.get('capital_equipment_cost', 0.0),
            manpower_cost=data.get('manpower_cost', 0.0),
            consumable_cost=data.get('consumable_cost', 0.0),
            ta_da_cost=data.get('ta_da_cost', 0.0),
            contingencies_cost=data.get('contingencies_cost', 0.0),
            seminar_cost=data.get('seminar_cost', 0.0),
            other_costs=data.get('other_costs', 0.0),
            funds_advanced=data.get('funds_advanced', 0.0),
            expenditure_incurred=data.get('expenditure_incurred', 0.0),
            unspent_balance=data.get('unspent_balance', 0.0)
        )

        # Add and commit the new record to the database
        db.session.add(new_form_iii)
        db.session.commit()
        return jsonify({"message": "Form III record added successfully!"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
    
    # Route to Update an Existing Form III Record
@form_iii_bp.route('/form_iii/<int:id>', methods=['PUT'])
def update_form_iii(id):
    data = request.get_json()
    form_iii_record = FormIII.query.get(id)

    if not form_iii_record:
        return jsonify({"error": "Form III record not found"}), 404

    try:
        # Update fields if provided in the request
        form_iii_record.project_id = data.get('project_id', form_iii_record.project_id)
        form_iii_record.quarter_end_date = datetime.strptime(
            data.get('quarter_end_date', form_iii_record.quarter_end_date.strftime('%Y-%m-%d')),
            '%Y-%m-%d'
        ).date()
        form_iii_record.land_building_cost = data.get('land_building_cost', form_iii_record.land_building_cost)
        form_iii_record.capital_equipment_cost = data.get('capital_equipment_cost', form_iii_record.capital_equipment_cost)
        form_iii_record.manpower_cost = data.get('manpower_cost', form_iii_record.manpower_cost)
        form_iii_record.consumable_cost = data.get('consumable_cost', form_iii_record.consumable_cost)
        form_iii_record.ta_da_cost = data.get('ta_da_cost', form_iii_record.ta_da_cost)
        form_iii_record.contingencies_cost = data.get('contingencies_cost', form_iii_record.contingencies_cost)
        form_iii_record.seminar_cost = data.get('seminar_cost', form_iii_record.seminar_cost)
        form_iii_record.other_costs = data.get('other_costs', form_iii_record.other_costs)
        form_iii_record.funds_advanced = data.get('funds_advanced', form_iii_record.funds_advanced)
        form_iii_record.expenditure_incurred = data.get('expenditure_incurred', form_iii_record.expenditure_incurred)
        form_iii_record.unspent_balance = data.get('unspent_balance', form_iii_record.unspent_balance)

        db.session.commit()
        return jsonify({"message": "Form III record updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500