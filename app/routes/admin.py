from flask import Blueprint, jsonify, request
from app.models import db, Admin , Investigator
from sqlalchemy.exc import SQLAlchemyError
from flask import Blueprint, jsonify, request
from app.models import db, Admin
from datetime import datetime
import os
import pickle
from email.mime.text import MIMEText
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

admin_bp = Blueprint('admin', __name__)
@admin_bp.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Admin route is working!"})

@admin_bp.route('/admin', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([{
        "admin_id": admin.admin_id,
        "adminUniqe_id":admin.adminUniqe_id,
        "admin_name": admin.admin_name,
        "email": admin.email,
        "phone_no": admin.phone_no, 
        "dob": admin.dob,
        "address": admin.address,
        "username": admin.username,
        "password": admin.password,
        "experience": admin.experience,
        "account_number": admin.account_number,
        "security_clearance": admin.security_clearance,
        "highest_qualification": admin.highest_qualification,
        "designation": admin.designation,
        "authority": admin.authority,
        "identification": admin.identification,
        "department": admin.department
    } for admin in admins])

# PUT API Endpoint to update an Admin record
@admin_bp.route('/admin/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    data = request.get_json()

    # Retrieve the admin record from the database
    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({"message": "Admin not found"}), 404

    try:
        # Update the fields with the provided data
        admin.admin_name = data.get('admin_name', admin.admin_name)
        admin.email = data.get('email', admin.email)
        admin.phone_no = data.get('phone_no', admin.phone_no)
        admin.dob = data.get('dob', admin.dob)
        admin.address = data.get('address', admin.address)
        admin.username = data.get('username', admin.username)
        admin.password = data.get('password', admin.password)
        admin.experience = data.get('experience', admin.experience)
        admin.account_number = data.get('account_number', admin.account_number)
        admin.security_clearance = data.get('security_clearance', admin.security_clearance)
        admin.highest_qualification = data.get('highest_qualification', admin.highest_qualification)
        admin.designation = data.get('designation', admin.designation)
        admin.authority = data.get('authority', admin.authority)
        admin.identification = data.get('identification', admin.identification)
        admin.department = data.get('department', admin.department)

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Admin updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback if there's an error
        return jsonify({"message": f"Error updating admin: {str(e)}"}), 500
    
@admin_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin_by_id(admin_id):
    # Query the admin by ID
    admin = Admin.query.get(admin_id)
    # If admin not found, return a 404 error
    if not admin:
        return jsonify({"message": "Admin not found"}), 404
    
    # Return the admin data in the response
    return jsonify({
        "admin_id": admin.admin_id,
        "admin_name": admin.admin_name,
        "email": admin.email,
        "phone_no": admin.phone_no,
        "dob": admin.dob,
        "address": admin.address,
        "username": admin.username,
        "password": admin.password,
        "experience": admin.experience,
        "account_number": admin.account_number,
        "security_clearance": admin.security_clearance,
        "highest_qualification": admin.highest_qualification,
        "designation": admin.designation,
        "authority": admin.authority,
        "identification": admin.identification,
        "department": admin.department
    })

# ==================================================================================================
# Email Sending Functionality
TOKEN_FILE = os.path.join(os.path.dirname(__file__), 'token.pickle')  # Path to store the token
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')  # Path to credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_email_notification(recipient_email, name, username, password):
    try:
        creds = None

        # Load existing token if it exists
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token_file:
                creds = pickle.load(token_file)

        # If no valid credentials are available, prompt the user to log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=8080)

                # Save the credentials for future use
                with open(TOKEN_FILE, 'wb') as token_file:
                    pickle.dump(creds, token_file)

        # Create Gmail API service
        service = build('gmail', 'v1', credentials=creds)

        # Create email message
        message = MIMEText(f"Hello {name},\n\nYour admin credentials:\nUsername: {username}\nPassword: {password}\n\nThank you.")
        message['to'] = recipient_email
        message['from'] = 'rushikeshwayal6@gmail.com'
        message['subject'] = "Admin Credentials Notification"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        service.users().messages().send(userId="me", body={'raw': raw}).execute()
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")

# ==================================================================================================

@admin_bp.route('/post/admin', methods=['POST'])
def add_admin():
    if request.method == 'OPTIONS':
        # CORS preflight response
        response = jsonify({'status': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response

    data = request.get_json()

    try:
        # Create a new Admin instance with data from the request
        new_admin = Admin(
            admin_name=data['admin_name'],
            email=data['email'],
            phone_no=data['phone_no'],
            dob=data.get('dob'),
            address=data.get('address'),
            username=data['username'],
            password=data['password'],
            experience=data.get('experience'),
            account_number=data.get('account_number'),
            security_clearance=data.get('security_clearance'),
            highest_qualification=data.get('highest_qualification'),
            designation=data.get('designation'),
            authority=data['authority'],
            identification=data.get('identification'),
            department=data.get('department')
        )

        # Add the new admin to the database
        db.session.add(new_admin)
        db.session.commit()  # Commit to generate the admin_id

        # Assign the adminUniqe_id after the admin_id is generated
        new_admin.adminUniqe_id = f"admin_{new_admin.admin_id}"
        db.session.commit()  # Commit again to save the updated adminUniqe_id

        # Send notification email
        send_email_notification(
            recipient_email="rushikeshwayal6@gmail.com",
            name=data['admin_name'],
            username=data['username'],
            password=data['password']
        )

        # Return success response
        return jsonify({
            "message": "Admin added successfully!",
            "adminUniqe_id": new_admin.adminUniqe_id,
            "admin_id": new_admin.admin_id
        }), 201

    except KeyError as e:
        # Handle missing fields
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        # Rollback on error and log the error for debugging
        db.session.rollback()
        print(f"Error occurred: {str(e)}")  # This will help log the error
        return jsonify({"error": str(e)}), 500
