from flask import Blueprint, jsonify, request
from app.models import db, ProjectStatus
from datetime import datetime

# Create a Blueprint for Project Status
project_status_bp = Blueprint('project_status', __name__)

# Route to Get All Project Statuses
@project_status_bp.route('/project_status', methods=['GET'])
def get_project_status():
    project_statuses = ProjectStatus.query.all()
    return jsonify([{
        "project_status_id": status.project_status_id,
        "phase": status.phase,
        "description": status.description,
        "date_of_updation": status.date_of_updation.strftime('%Y-%m-%d'),  # Format date
        "time_of_updation": status.time_of_updation.strftime('%H:%M:%S'),  # Format time
        "project_id": status.project_id
    } for status in project_statuses])

# Route to Add a New Project Status
@project_status_bp.route('/post/project_status', methods=['POST'])
def add_project_status():
    data = request.get_json()
    try:
        # Convert the string date and time to actual Date and Time objects
        date_of_updation = datetime.strptime(data['date_of_updation'], '%Y-%m-%d').date()
        time_of_updation = datetime.strptime(data['time_of_updation'], '%H:%M:%S').time()

        new_project_status = ProjectStatus(
            phase=data['phase'],
            description=data['description'],
            date_of_updation=date_of_updation,
            time_of_updation=time_of_updation,
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

 
@project_status_bp.route('/put/project_status/<int:status_id>', methods=['PUT'])
def update_project_status(status_id):
    data = request.get_json()
    status = ProjectStatus.query.get(status_id)

    if not status:
        return jsonify({"error": "Project Status not found"}), 404

    try:
        # Update the project status fields using data.get() method to allow partial updates
        status.phase = data.get('phase', status.phase)
        status.description = data.get('description', status.description)
        status.date_of_updation = data.get('date_of_updation', status.date_of_updation)
        status.time_of_updation = data.get('time_of_updation', status.time_of_updation)
        status.project_id = data.get('project_id', status.project_id)

        # Commit the changes to the database
        db.session.commit()
        return jsonify({"message": "Project Status updated successfully!"}), 200
    except Exception as e:
        # If any exception occurs, roll back the transaction and return the error message
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@project_status_bp.route('/delete/project_status/<int:status_id>', methods=['DELETE'])
def delete_project_status(status_id):
    try:
        # Fetch the project status to delete
        status = ProjectStatus.query.get(status_id)

        if not status:
            return jsonify({"error": "Project Status not found"}), 404

        # Delete the project status
        db.session.delete(status)
        db.session.commit()

        return jsonify({"message": "Project Status deleted successfully!"}), 200

    except Exception as e:
        # Rollback the transaction in case of an error
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
