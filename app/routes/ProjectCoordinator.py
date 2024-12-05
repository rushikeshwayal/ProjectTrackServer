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
             project_coordinator_name=data['project_coordinator_name'],
            email=data['email'],
            phone_number=data['phone_no'],
            department=data['department'],
            experience=data['years_of_experience'],
            branch=data['branch'],
            highest_qualification=data['highest_qualification'],
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
    
    # PUT route to update an existing project coordinator
@projectcoordinator_bp.route('/put/project-coordinator/<int:id>', methods=['PUT'])
def update_project_coordinator(id):
    try:
        data = request.get_json()

        # Log the incoming data
        current_app.logger.info(f'Received data to update project coordinator with ID: {id} - {data}')

        # Fetch the existing project coordinator
        coordinator = ProjectCoordinator.query.get(id)
        
        if not coordinator:
            current_app.logger.warning(f'Project Coordinator with ID {id} not found.')
            return jsonify({"error": f"Project Coordinator with ID {id} not found"}), 404

        # Update the coordinator details
        coordinator.project_coordinator_name = data.get('coordinator_name', coordinator.project_coordinator_name)
        coordinator.phone_number = data.get('phone_no', coordinator.phone_number)
        coordinator.email = data.get('email', coordinator.email)
        coordinator.department = data.get('department', coordinator.department)
        coordinator.experience = data.get('years_of_experience', coordinator.experience)
        coordinator.branch = data.get('current_projects', coordinator.branch)
        coordinator.highest_qualification = data.get('specialization', coordinator.highest_qualification)
        coordinator.bank_details = data.get('bank_details', coordinator.bank_details)
        coordinator.security_clearance = data.get('security_clearance', coordinator.security_clearance)
        coordinator.dob = data.get('dob', coordinator.dob)
        coordinator.designation = data.get('designation', coordinator.designation)
        coordinator.identification = data.get('identification', coordinator.identification)
        coordinator.address = data.get('address', coordinator.address)

        # Commit the changes to the database
        db.session.commit()
        
        current_app.logger.info(f'Project Coordinator with ID {id} updated successfully.')
        return jsonify({"message": "Project Coordinator updated successfully!"})

    except Exception as e:
        current_app.logger.error(f'Error updating project coordinator with ID {id}: {e}')
        return jsonify({"error": "Failed to update project coordinator"}), 500
    
    
# DELETE route to remove a project coordinator by ID
@projectcoordinator_bp.route('/delete/project-coordinator/<int:id>', methods=['DELETE'])
def delete_project_coordinator(id):
    try:
        # Log the request to delete a project coordinator
        current_app.logger.info(f'Request received to delete project coordinator with ID: {id}')

        # Fetch the project coordinator by ID
        coordinator = ProjectCoordinator.query.get(id)

        if not coordinator:
            current_app.logger.warning(f'Project Coordinator with ID {id} not found.')
            return jsonify({"error": f"Project Coordinator with ID {id} not found"}), 404

        # Delete the project coordinator from the database
        db.session.delete(coordinator)
        db.session.commit()

        current_app.logger.info(f'Project Coordinator with ID {id} deleted successfully.')
        return jsonify({"message": "Project Coordinator deleted successfully!"})

    except Exception as e:
        # Log the error and respond with a failure message
        current_app.logger.error(f'Error deleting project coordinator with ID {id}: {e}')
        return jsonify({"error": "Failed to delete project coordinator"}), 500

@projectcoordinator_bp.route('/project-coordinator/<int:project_coordinator_id>', methods=['GET'])
def get_project_coordinator_by_id(project_coordinator_id):
    project_coordinator = ProjectCoordinator.query.get(project_coordinator_id)
    if not project_coordinator:
        return jsonify({'message': 'Project Coordinator not found'}), 404
    return jsonify({
        'project_coordinator_id': project_coordinator.project_coordinator_id,
        'project_coordinator_name': project_coordinator.project_coordinator_name,
        'phone_number': project_coordinator.phone_number,
        'address': project_coordinator.address,
        'experience': project_coordinator.experience,
        'bank_details': project_coordinator.bank_details,
        'security_clearance': project_coordinator.security_clearance,
        'highest_qualification': project_coordinator.highest_qualification,
        'email': project_coordinator.email,
        'dob': project_coordinator.dob,
        'designation': project_coordinator.designation,
        'department': project_coordinator.department,
        'identification': project_coordinator.identification,
        'branch': project_coordinator.branch
    })
