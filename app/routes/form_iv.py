from flask import Blueprint, jsonify, request
from app.models import db, FormIV
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

form_iv_bp = Blueprint('form_iv', __name__)

# CRUD API for Form IV
@form_iv_bp.route('/form-iv', methods=['GET'])
def get_all_form_iv():
    forms = FormIV.query.all()
    return jsonify([form.as_dict() for form in forms]), 200

@form_iv_bp.route('/form-iv/<int:form_id>', methods=['GET'])
def get_form_iv_by_id(form_id):
    form = FormIV.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form IV entry not found'}), 404
    return jsonify(form.as_dict()), 200

@form_iv_bp.route('/post/form-iv', methods=['POST'])
def create_form_iv():
    data = request.get_json()
    try:
        new_form = FormIV(**data)
        db.session.add(new_form)
        db.session.commit()
        return jsonify({'message': 'Form IV entry created successfully!', 'id': new_form.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@form_iv_bp.route('/put/form-iv/<int:form_id>', methods=['PUT'])
def update_form_iv(form_id):
    form = FormIV.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form IV entry not found'}), 404

    data = request.get_json()
    try:
        for key, value in data.items():
            if hasattr(form, key):
                setattr(form, key, value)
        db.session.commit()
        return jsonify({'message': 'Form IV entry updated successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@form_iv_bp.route('/delete/form-iv/<int:form_id>', methods=['DELETE'])
def delete_form_iv(form_id):
    form = FormIV.query.get(form_id)
    if not form:
        return jsonify({'error': 'Form IV entry not found'}), 404
    try:
        db.session.delete(form)
        db.session.commit()
        return jsonify({'message': 'Form IV entry deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
