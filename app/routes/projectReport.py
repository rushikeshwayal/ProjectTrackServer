from flask import Blueprint, jsonify, request
from app.models import db, ProjectReport
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import mimetypes

# Set the base directory for credentials file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')

# Define upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# Blueprint for Project Report
project_Report_bp = Blueprint('Project_Report', __name__)
def authenticate_google_drive():
    """Authenticate and get Google Drive credentials."""
    try:
        # Check if token.json exists to avoid re-authentication
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            # Define the redirect URI and handle port conflicts
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)  # Use a specific port to avoid conflicts
            
            # Save the credentials to token.json
            with open('token.json', 'w') as token_file:
                token_file.write(creds.to_json())
        return creds
    except FileNotFoundError as e:
        raise RuntimeError(f"Credentials file not found: {CREDENTIALS_FILE}. Ensure it exists.")
    except Exception as e:
        raise RuntimeError(f"Authentication failed: {str(e)}")


def upload_to_drive(file_path, file_name):
    """Upload a file to Google Drive and return its URL."""
    try:
        creds = authenticate_google_drive()
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': file_name}
        mime_type, _ = mimetypes.guess_type(file_path)
        media = MediaFileUpload(file_path, mimetype=mime_type or 'application/octet-stream')

        uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id,webViewLink').execute()
        return uploaded_file.get('webViewLink')
    except Exception as e:
        raise RuntimeError(f"Failed to upload file to Google Drive: {str(e)}")

@project_Report_bp.route('/post/reports', methods=['POST'])
def create_report():
    """Create a new project report."""
    try:
        project_id = request.form.get('project_id')
        phase = request.form.get('phase')
        report_file = request.files.get('report_file')

        if not project_id or not phase or not report_file:
            return jsonify({"error": "Missing required fields"}), 400

        # Save the file locally
        file_name = report_file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        report_file.save(file_path)

        # Upload file to Google Drive
        drive_url = upload_to_drive(file_path, file_name)

        # Create the new report
        new_report = ProjectReport(
            project_id=project_id,
            phase=phase,
            report_doc=drive_url
        )

        # Add and commit to the database
        db.session.add(new_report)
        db.session.commit()

        return jsonify({"message": "Report created successfully", "report": new_report.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@project_Report_bp.route('/reports/<string:project_id>', methods=['GET'])
def get_reports_by_project_id(project_id):
    """Get all reports for a specific project ID."""
    reports = ProjectReport.query.filter_by(project_id=project_id).all()
    if not reports:
        return jsonify({"error": "No reports found for this project ID"}), 404

    return jsonify([report.to_dict() for report in reports]), 200
