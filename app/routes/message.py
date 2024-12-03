from flask import Blueprint, jsonify, request
from app.models import db, Message

message_bp = Blueprint('message', __name__)

# Route to send a message
from flask import Blueprint, jsonify, request
from app.models import db, Message

message_bp = Blueprint('message', __name__)

# Route to send a message
# Route to send a message
@message_bp.route('/chat/send', methods=['POST'])
def send_message():
    try:
        # Get form data
        sender_id = request.form.get('sender_id')
        sender_type = request.form.get('sender_type')
        receiver_id = request.form.get('receiver_id')
        receiver_type = request.form.get('receiver_type')
        subject = request.form.get('subject')
        body = request.form.get('body')
        file = request.files.get('attachment')  # Get the file attachment

        # Validate required fields (file is optional)
        if not all([sender_id, sender_type, receiver_id, receiver_type, subject, body]):
            return jsonify({"error": "Missing required fields."}), 400

        # Prepare the attachment details if a file is provided
        attachment_data = None
        attachment_name = None
        attachment_mime_type = None
        
        if file:
            attachment_data = file.read()  # Read the file data (binary)
            attachment_name = file.filename  # Get the file name
            attachment_mime_type = file.mimetype  # Get MIME type of the file

        # Create a new message
        new_message = Message(
            sender_id=sender_id,
            sender_type=sender_type,
            receiver_id=receiver_id,
            receiver_type=receiver_type,
            subject=subject,
            body=body,
            attachment=attachment_data,  # Store the binary file data
            attachment_name=attachment_name,  # Store the file name
            attachment_mime_type=attachment_mime_type,  # Store the MIME type of the file
        )

        db.session.add(new_message)
        db.session.commit()

        return jsonify({"message": "Message sent successfully!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



# Route to get a single message
@message_bp.route('/chat/message/<int:message_id>', methods=['GET'])
def get_message(message_id):
    try:
        message = Message.query.get(message_id)

        if not message:
            return jsonify({"error": "Message not found."}), 404

        # Prepare the response data
        response = {
            "message_id": message.message_id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type,
            "receiver_id": message.receiver_id,
            "receiver_type": message.receiver_type,
            "subject": message.subject,
            "body": message.body,
            "timestamp": message.timestamp.isoformat(),
            "attachment_name": message.attachment_name,
            "attachment_mime_type": message.attachment_mime_type,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to download the attachment
@message_bp.route('/chat/message/<int:message_id>/attachment', methods=['GET'])
def download_attachment(message_id):
    try:
        message = Message.query.get(message_id)
        if not message or not message.attachment:
            return jsonify({"error": "Attachment not found."}), 404
            
        

        # Send the file with the correct MIME type and filename
        return (
            message.attachment,  # Binary content of the file
            200,
            {
                "Content-Type": message.attachment_mime_type,  # Correct MIME type
                "Content-Disposition": f"attachment; filename={message.attachment_name}",  # Correct filename
            },
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@message_bp.route('/chat/messages', methods=['GET'])
def get_all_messages():
    try:
        sort_order = request.args.get('sort_order', default='desc')
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        messages_query = Message.query.order_by(
            Message.timestamp.asc() if sort_order == 'asc' else Message.timestamp.desc()
        )
        messages_paginated = messages_query.paginate(page=page, per_page=per_page, error_out=False)

        messages = [
            {    "sender_id":message.sender_id,
                 "receiver_id":message.receiver_id,
                "message_id": message.message_id,
                "subject": message.subject,
                "body": message.body,
                "timestamp": message.timestamp.isoformat(),
                "attachment_name": message.attachment_name,
            }
            for message in messages_paginated.items
        ]

        response = {
            "messages": messages,
            "page": messages_paginated.page,
            "total_pages": messages_paginated.pages,
            "total_messages": messages_paginated.total,
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
