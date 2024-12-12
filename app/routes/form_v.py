from flask import Blueprint, jsonify, request
from app.models import db, FormV
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

form_v_bp = Blueprint('form_v', __name__)

# CRUD API for Form V
@form_v_bp.route('/form-v', methods=['GET'])
def get_all_form_v():
    forms = FormV.query.all()
    return jsonify([form.as_dict() for form in forms]), 200

@form_v_bp.route('/form-v/<int:form_id>', methods=['GET'])
def get_form_v_by_id(form_id):
    form = FormV.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form V entry not found'}), 404
    return jsonify(form.as_dict()), 200

@form_v_bp.route('/post/form-v', methods=['POST'])
def create_form_v():
    data = request.get_json()
    try:
        new_form = FormV(**data)
        db.session.add(new_form)
        db.session.commit()
        return jsonify({'message': 'Form V entry created successfully!', 'id': new_form.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@form_v_bp.route('/put/form-v/<int:form_id>', methods=['PUT'])
def update_form_v(form_id):
    form = FormV.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form V entry not found'}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            if hasattr(form, key):
                setattr(form, key, value)
        db.session.commit()
        return jsonify({'message': 'Form V entry updated successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@form_v_bp.route('/delete/form-v/<int:form_id>', methods=['DELETE'])
def delete_form_v(form_id):
    form = FormV.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form V entry not found'}), 404
    try:
        db.session.delete(form)
        db.session.commit()
        return jsonify({'message': 'Form V entry deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
