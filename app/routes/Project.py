from flask import Blueprint, jsonify, request
from app.models import db, ProjectTable

project_bp = Blueprint('project', __name__)

# GET API to retrieve all projects
@project_bp.route('/project', methods=['GET'])
def get_projects():
    projects = ProjectTable.query.all()
    return jsonify([{
        "project_id": project.project_id,
        "project_name": project.project_name,
        "approval_date": project.approval_date,
        "investigator_id": project.investigator_id,
        "project_fund_id": project.project_fund_id,
        "project_status_id": project.project_status_id,
        "sub_agency_id": project.sub_agency_id,
        "agency_id": project.agency_id,
        "sub_investigator_id": project.sub_investigator_id,
        "project_type": project.project_type,
        "project_start_date": project.project_start_date,
        "project_end_date": project.project_end_date,
        "project_coordinator_id": project.project_coordinator_id,
        "project_description": project.project_description
    } for project in projects])

# POST API to create a new project
@project_bp.route('/post/project', methods=['POST'])
def create_project():
    data = request.get_json()
    try:
        new_project = ProjectTable(
            project_name=data['project_name'],
            approval_date=data['approval_date'],
            investigator_id=data['investigator_id'],
            project_fund_id=data['project_fund_id'],
            project_status_id=data['project_status_id'],
            sub_agency_id=data['sub_agency_id'],
            agency_id=data['agency_id'],
            sub_investigator_id=data['sub_investigator_id'],
            project_type=data['project_type'],
            project_start_date=data['project_start_date'],
            project_end_date=data['project_end_date'],
            project_coordinator_id=data['project_coordinator_id'],
            project_description=data.get('project_description')
        )
        db.session.add(new_project)
        db.session.commit()
        return jsonify({"message": "Project created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# PUT API to update an existing project
@project_bp.route('/put/project/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.get_json()
    project = ProjectTable.query.get(project_id)

    if not project:
        return jsonify({"error": "Project not found"}), 404

    try:
        project.project_name = data.get('project_name', project.project_name)
        project.approval_date = data.get('approval_date', project.approval_date)
        project.investigator_id = data.get('investigator_id', project.investigator_id)
        project.project_fund_id = data.get('project_fund_id', project.project_fund_id)
        project.project_status_id = data.get('project_status_id', project.project_status_id)
        project.sub_agency_id = data.get('sub_agency_id', project.sub_agency_id)
        project.agency_id = data.get('agency_id', project.agency_id)
        project.sub_investigator_id = data.get('sub_investigator_id', project.sub_investigator_id)
        project.project_type = data.get('project_type', project.project_type)
        project.project_start_date = data.get('project_start_date', project.project_start_date)
        project.project_end_date = data.get('project_end_date', project.project_end_date)
        project.project_coordinator_id = data.get('project_coordinator_id', project.project_coordinator_id)
        project.project_description = data.get('project_description', project.project_description)

        db.session.commit()
        return jsonify({"message": "Project updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
