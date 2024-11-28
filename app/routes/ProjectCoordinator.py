from flask import Blueprint, jsonify, request, current_app
from app.models import db, ProjectCoordinator
import logging

projectcoordinator_bp = Blueprint('projectcoordinator', __name__)

@projectcoordinator_bp.route('/project-coordinator', methods=['GET'])
def get_project_coordinators():
    try:
        current_app.logger.info('Fetching all project coordinators')
        coordinators = ProjectCoordinator.query.all()

        if coordinators:
            current_app.logger.info(f'Found {len(coordinators)} coordinators')
        else:
            current_app.logger.warning('No project coordinators found')

        return jsonify([{
            "coordinator_id": coordinator.project_coordinator_id,
            "coordinator_name": coordinator.project_coordinator_name,
            "email": coordinator.email,
            "phone_no": coordinator.phone_number,
            "department": coordinator.department,
            "years_of_experience": coordinator.experience,
            "current_projects": coordinator.branch,  # Assuming 'branch' refers to projects for simplicity
            "specialization": coordinator.highest_qualification
        } for coordinator in coordinators])

    except Exception as e:
        current_app.logger.error(f'Error fetching project coordinators: {e}')
        return jsonify({"error": "Failed to fetch project coordinators"}), 500


@projectcoordinator_bp.route('/post/project-coordinator', methods=['POST'])
def add_project_coordinator():
    try:
        data = request.get_json()

        # Log the incoming data
        current_app.logger.info('Received data to add new project coordinator: %s', data)

        # Create a new project coordinator object
        new_coordinator = ProjectCoordinator(
            project_coordinator_name=data['coordinator_name'],
            email=data['email'],
            phone_number=data['phone_no'],
            department=data['department'],
            experience=data['years_of_experience'],
            branch=data['current_projects'],
            highest_qualification=data['specialization'],
            bank_details=data.get('bank_details', ''),
            security_clearance=data.get('security_clearance', ''),
            dob=data['dob'],
            designation=data['designation'],
            identification=data['identification'],
            address=data['address']
        )

        # Add to the database
        db.session.add(new_coordinator)
        db.session.commit()
        
        current_app.logger.info(f"Project Coordinator {new_coordinator.project_coordinator_name} added successfully.")
        return jsonify({"message": "Project Coordinator added successfully!"})

    except Exception as e:
        current_app.logger.error(f'Error adding project coordinator: {e}')
        return jsonify({"error": "Failed to add project coordinator"}), 500