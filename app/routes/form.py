from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
from app import db
from app.models import Form

upload_bp = Blueprint('upload', __name__)

# Set the upload folder for the forms
UPLOAD_FOLDER = 'F:/project track/ProjectTrackServer/app/uploads/forms'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('/upload/forms', methods=['POST'])
def upload_forms():
    if 'files' not in request.files:
        return jsonify({"message": "No file part"}), 400

    files = request.files.getlist('files')  # Get all files in the form

    if len(files) == 0:
        return jsonify({"message": "No files selected"}), 400

    uploaded_files = []

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)  # Save the file to the server

        with open(filepath, 'rb') as f:
            file_data = f.read()  # Read the binary data from the file

        # Store the form in the database
        new_form = Form(form_name=filename, file_data=file_data)
        db.session.add(new_form)
        uploaded_files.append(filename)

    db.session.commit()
    return jsonify({
        "message": "Files uploaded successfully!",
        "uploaded_files": uploaded_files
    }), 201
from flask import send_file
import os

@upload_bp.route('/download/form/<int:file_id>', methods=['GET'])
def download_form(file_id):
    form = Form.query.get_or_404(file_id)

    # Save the file content to a temporary file in the upload directory
    file_path = os.path.join(UPLOAD_FOLDER, form.form_name)

    with open(file_path, 'wb') as f:
        f.write(form.file_data)  # Write the binary data to the file

    # Return the file as an attachment
    return send_file(file_path, as_attachment=True, download_name=form.form_name)
