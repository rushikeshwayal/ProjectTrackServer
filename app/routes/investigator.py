from flask import Blueprint, jsonify, request
from app.models import db, Investigator
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import os
import pickle
# Define the Blueprint
investigator_bp = Blueprint('investigator', __name__)

# Constants for Gmail API
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')   # Replace with the actual path


@investigator_bp.route('/investigator', methods=['GET'])
def get_investigators():
    investigators = Investigator.query.all()
    return jsonify([{
        "investigator_id": investigator.investigator_id,
        "investigatorUniqe_id":investigator.investigatorUniqe_id,
        "investigator_name": investigator.investigator_name,
        "email": investigator.email,
        "phone_no": investigator.phone_no, 
        "dob": investigator.dob,
        "address": investigator.address,
        "username": investigator.username,
        "password": investigator.password,
        "experience": investigator.experience,
        "account_number": investigator.account_number,
        "security_clearance": investigator.security_clearance,
        "highest_qualification": investigator.highest_qualification,
        "designation": investigator.designation,
        "authority": investigator.authority,
        "identification": investigator.identification,
        "department": investigator.department
    } for investigator in investigators])


@investigator_bp.route('/put/investigator/<int:investigator_id>', methods=['PUT'])
def investigatorput(investigator_id):
    data = request.get_json()
    investigator = Investigator.query.get(investigator_id)

    if not investigator:
        return jsonify({"error": "Investigator not found"}), 404

    try:
        # Update fields if provided
        investigator.email = data.get('email', investigator.email)
        investigator.username = data.get('username', investigator.username)
        investigator.password = data.get('password', investigator.password)
        investigator.dob = data.get('dob', investigator.dob)
        investigator.designation = data.get('designation', investigator.designation)
        investigator.department = data.get('department', investigator.department)
        investigator.identification = data.get('identification', investigator.identification)
        investigator.investigator_name = data.get('investigator_name', investigator.investigator_name)
        investigator.phone_no = data.get('phone_no', investigator.phone_no)
        investigator.address = data.get('address', investigator.address)
        investigator.experience = data.get('experience', investigator.experience)
        investigator.account_number = data.get('account_number', investigator.account_number)
        investigator.security_clearance = data.get('security_clearance', investigator.security_clearance)
        investigator.authority = data.get('authority', investigator.authority)
        investigator.highest_qualification = data.get('highest_qualification', investigator.highest_qualification)

        db.session.commit()
        return jsonify({"message": "Investigator updated successfully!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@investigator_bp.route('/investigator/<int:investigator_id>', methods=['GET'])
def get_investigator_by_id(investigator_id):
    investigator = Investigator.query.get(investigator_id)
    if not investigator:
        return jsonify({'message': 'Investigator not found'}), 404
    return jsonify({
        'investigator_id': investigator.investigator_id,
        'email': investigator.email,
        'username': investigator.username,
        'dob': investigator.dob,
        'designation': investigator.designation,
        'department': investigator.department,
        'identification': investigator.identification,
        'investigator_name': investigator.investigator_name,
        'phone_no': investigator.phone_no,
        'address': investigator.address,
        'experience': investigator.experience,
        'account_number': investigator.account_number,
        'security_clearance': investigator.security_clearance,
        'authority': investigator.authority,
        'highest_qualification': investigator.highest_qualification
    })

# ================
@investigator_bp.route('/post/investigator', methods=['POST'])
def add_investigator():
    data = request.get_json()
    try:
        new_investigator = Investigator(
            investigator_name=data['investigator_name'],
            email=data['email'],
            phone_no=data['phone_no'],
            dob=data['dob'],
            address=data['address'],
            username=data['username'],
            password=data['password'],
            experience=data['experience'],
            account_number=data['account_number'],
            highest_qualification=data['highest_qualification'],
            designation=data['designation'],
            authority=data['authority'],
            identification=data['identification'],
            department=data['department']
        )
        db.session.add(new_investigator)
        db.session.flush()
        new_investigator.investigatorUniqe_id = f"investigator_{new_investigator.investigator_id}"
        db.session.commit()

        send_email(data['email'], data['investigator_name'], data['username'], data['password'])

        return jsonify({
            "message": "Investigator added successfully!",
            "investigator_id": new_investigator.investigator_id
        }), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email or Username already exists."}), 400
    except KeyError as e:
        db.session.rollback()
        return jsonify({"error": f"Missing field: {e}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# ================





@investigator_bp.route('/delete/investigator/<int:investigator_id>', methods=['DELETE'])
def delete_investigator(investigator_id):
    investigator = Investigator.query.get(investigator_id)
    if not investigator:
        return jsonify({"error": "Investigator not found"}), 404
    try:
        db.session.delete(investigator)
        db.session.commit()
        return jsonify({"message": "Investigator deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# =======================================================================================================================================================================
TOKEN_FILE = os.path.join(BASE_DIR, 'token.pickle')  # Path to store the token
def send_email(recipient_email, name, username, password):
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
        message = MIMEText(f"Hello {name},\n\nYour credentials:\nUsername: {username}\nPassword: {password}")
        message['to'] = recipient_email
        message['from'] = 'rushikeshwayl6@gmail.com'
        message['subject'] = "Welcome Investigator Credentials"
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        service.users().messages().send(userId="me", body={'raw': raw}).execute()
        print("Email sent successfully")

    except Exception as e:
        print(f"Failed to send email: {e}")