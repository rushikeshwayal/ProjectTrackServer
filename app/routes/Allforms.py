from flask import Blueprint, jsonify, request, send_file
from app.models import db, FileStorage
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import mimetypes

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'credentials.json')
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

file_bp = Blueprint('file_bp', __name__)

def authenticate_google_drive():
    """Authenticate and return Google Drive credentials."""
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)
            with open('token.json', 'w') as token_file:
                token_file.write(creds.to_json())
        return creds
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

@file_bp.route('/files/upload', methods=['POST'])
def upload_file():
    """Upload a file to Google Drive and store metadata in the database."""
    file_path = None  # Initialize file_path to avoid UnboundLocalError
    try:
        project_id = request.form.get('project_id')
        file_name = request.form.get('file_name')  # Get the selected file name
        file = request.files.get('file')

        if not project_id or not file or not file_name:
            return jsonify({"error": "Missing required fields"}), 400

        # Save the file locally with the selected file_name instead of file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        file.save(file_path)

        # Upload to Google Drive
        drive_url = upload_to_drive(file_path, file_name)

        # Save file details in the database
        new_file = FileStorage(
            project_id=project_id,
            file_name=file_name,  # Use the selected file name
            file_url=drive_url
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully", "file": new_file.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)



@file_bp.route('/files/<string:project_id>', methods=['GET'])
def get_files_by_project_id(project_id):
    """Retrieve all files for a specific project ID."""
    files = FileStorage.query.filter_by(project_id=project_id).all()
    if not files:
        return jsonify({"error": "No files found for this project ID"}), 404

    return jsonify([file.to_dict() for file in files]), 200

@file_bp.route('/files/download/<int:file_id>', methods=['GET'])
def download_file(file_id):
    """Generate a Google Drive file link for users to download."""
    file = FileStorage.query.get(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404

    return jsonify({"file_name": file.file_name, "download_link": file.file_url}), 200
