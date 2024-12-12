from flask import Blueprint, jsonify, request
from app.models import db, Expenditure, ProjectTable

expenditure_bp = Blueprint('expenditure', __name__)





@expenditure_bp.route('/post/expenditure', methods=['POST'])
def add_expenditure():
    try:
        data = request.get_json()

        # Extracting and validating fields from the request data
        project_id = int(data.get('project_id', 0))
        land_building = float(data.get('land_building', 0.0))
        equipment = float(data.get('equipment', 0.0))
        totalCapital = float(data.get('totalCapital', 0.0))

        salary = float(data.get('salary', 0.0))
        consumables = float(data.get('consumables', 0.0))
        travel = float(data.get('travel', 0.0))
        workshopSeminar = float(data.get('workshopSeminar', 0.0))
        totalRevenue = float(data.get('totalRevenue', 0.0))

        contingency = float(data.get('contingency', 0.0))
        institutionalOverhead = float(data.get('institutionalOverhead', 0.0))
        applicableTaxes = float(data.get('applicableTaxes', 0.0))
        grandTotal = float(data.get('grandTotal', 0.0))

        implementingAgency = bool(data.get('implementingAgency', False))
        subImplementingAgency1 = bool(data.get('subImplementingAgency1', False))
        subImplementingAgency2 = bool(data.get('subImplementingAgency2', False))
        subImplementingAgency3 = bool(data.get('subImplementingAgency3', False))

        # Creating new Expenditure entry
        new_expenditure = Expenditure(
            project_id=project_id,
            land_building=land_building,
            equipment=equipment,
            totalCapital=totalCapital,
            salary=salary,
            consumables=consumables,
            travel=travel,
            workshopSeminar=workshopSeminar,
            totalRevenue=totalRevenue,
            contingency=contingency,
            institutionalOverhead=institutionalOverhead,
            applicableTaxes=applicableTaxes,
            grandTotal=grandTotal,
            implementingAgency=implementingAgency,
            subImplementingAgency1=subImplementingAgency1,
            subImplementingAgency2=subImplementingAgency2,
            subImplementingAgency3=subImplementingAgency3
        )

        # Add the new Expenditure to the DB
        db.session.add(new_expenditure)
        db.session.commit()
        return jsonify({'message': 'Expenditure added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to add expenditure: {str(e)}"}), 400


@expenditure_bp.route('/expenditure', methods=['GET'])
def get_expenditures():
    expenditures = Expenditure.query.all()
    return jsonify([{
        'id': exp.id,
        'project_id': exp.project_id,
        'land_building': exp.land_building,
        'equipment': exp.equipment,
        'totalCapital': exp.totalCapital,
        'salary': exp.salary,
        'consumables': exp.consumables,
        'travel': exp.travel,
        'workshopSeminar': exp.workshopSeminar,
        'totalRevenue': exp.totalRevenue,
        'contingency': exp.contingency,
        'institutionalOverhead': exp.institutionalOverhead,
        'applicableTaxes': exp.applicableTaxes,
        'grandTotal': exp.grandTotal,
        'implementingAgency': exp.implementingAgency,
        'subImplementingAgency1': exp.subImplementingAgency1,
        'subImplementingAgency2': exp.subImplementingAgency2,
        'subImplementingAgency3': exp.subImplementingAgency3
    } for exp in expenditures]), 200

