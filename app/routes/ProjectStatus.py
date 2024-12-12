from flask import Blueprint, jsonify, request
from app.models import db, ProjectStatus
from datetime import datetime

# Create a Blueprint for Project Status
project_status_bp = Blueprint('project_status', __name__)

# Route to Get All Project Statuses
@project_status_bp.route('/project_status', methods=['GET'])
def get_project_status():
    project_statuses = ProjectStatus.query.all()
    return jsonify([
        {
            "project_status_id": status.project_status_id,
            "phase": status.phase,
            "description": status.description,
            "start_date": status.start_date.strftime('%Y-%m-%d') if status.start_date else None,
            "end_date": status.end_date.strftime('%Y-%m-%d') if status.end_date else None,
            "project_completion_status": status.project_completion_status,
            "project_id": status.project_id
        }
        for status in project_statuses
    ])

# Route to Add a New Project Status
@project_status_bp.route('/post/project_status', methods=['POST'])
def add_project_status():
    data = request.get_json()
    try:
        new_project_status = ProjectStatus(
            phase=data['phase'],
            description=data.get('description'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            project_completion_status=data.get('project_completion_status', "In Progress"),
            project_id=data['project_id']
        )
        db.session.add(new_project_status)
        db.session.commit()
        return jsonify({"message": "Project Status added successfully!"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to Update an Existing Project Status
@project_status_bp.route('/put/project_status/<int:status_id>', methods=['PUT'])
def update_project_status(status_id):
    data = request.get_json()
    status = ProjectStatus.query.get(status_id)

    if not status:
        return jsonify({"error": "Project Status not found"}), 404

    try:
        # Update the project status fields
        status.phase = data.get('phase', status.phase)
        status.description = data.get('description', status.description)
        status.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date() if data.get('start_date') else status.start_date
        status.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else status.end_date
        status.project_completion_status = data.get('project_completion_status', status.project_completion_status)
        status.project_id = data.get('project_id', status.project_id)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Project Status updated successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to Delete a Project Status
@project_status_bp.route('/delete/project_status/<int:status_id>', methods=['DELETE'])
def delete_project_status(status_id):
    try:
        status = ProjectStatus.query.get(status_id)

        if not status:
            return jsonify({"error": "Project Status not found"}), 404

        db.session.delete(status)
        db.session.commit()

        return jsonify({"message": "Project Status deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
