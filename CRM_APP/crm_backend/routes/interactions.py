from flask import Blueprint, request, jsonify
from crm_backend import db
from crm_backend.models import Interaction
from flask_jwt_extended import jwt_required

bp = Blueprint('interactions', __name__, url_prefix='/interactions')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_interactions():
    interactions = Interaction.query.all()
    return jsonify([{'id': interaction.id, 'customer_id': interaction.customer_id, 'notes': interaction.notes} for interaction in interactions])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_interaction(id):
    interaction = Interaction.query.get_or_404(id)
    return jsonify({'id': interaction.id, 'customer_id': interaction.customer_id, 'notes': interaction.notes})

@bp.route('/', methods=['POST'])
@jwt_required()
def create_interaction():
    data = request.get_json()
    interaction = Interaction(customer_id=data['customer_id'], notes=data['notes'])
    db.session.add(interaction)
    db.session.commit()
    return jsonify({'id': interaction.id, 'message': 'Interaction created'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_interaction(id):
    interaction = Interaction.query.get_or_404(id)
    data = request.get_json()
    interaction.notes = data['notes']
    db.session.commit()
    return jsonify({'message': 'Interaction updated'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_interaction(id):
    interaction = Interaction.query.get_or_404(id)
    db.session.delete(interaction)
    db.session.commit()
    return jsonify({'message': 'Interaction deleted'})
