from flask import Blueprint, request, jsonify
from crm_backend import db
from crm_backend.models import SupportTicket
from flask_jwt_extended import jwt_required

bp = Blueprint('support_tickets', __name__, url_prefix='/support_tickets')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_support_tickets():
    support_tickets = SupportTicket.query.all()
    return jsonify([{'id': ticket.id, 'customer_id': ticket.customer_id, 'description': ticket.description, 'status': ticket.status} for ticket in support_tickets])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_support_ticket(id):
    support_ticket = SupportTicket.query.get_or_404(id)
    return jsonify({'id': support_ticket.id, 'customer_id': support_ticket.customer_id, 'description': support_ticket.description, 'status': support_ticket.status})

@bp.route('/', methods=['POST'])
@jwt_required()
def create_support_ticket():
    data = request.get_json()
    support_ticket = SupportTicket(customer_id=data['customer_id'], description=data['description'], status=data['status'])
    db.session.add(support_ticket)
    db.session.commit()
    return jsonify({'id': support_ticket.id, 'message': 'Support Ticket created'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_support_ticket(id):
    support_ticket = SupportTicket.query.get_or_404(id)
    data = request.get_json()
    support_ticket.description = data['description']
    support_ticket.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Support Ticket updated'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_support_ticket(id):
    support_ticket = SupportTicket.query.get_or_404(id)
    db.session.delete(support_ticket)
    db.session.commit()
    return jsonify({'message': 'Support Ticket deleted'})
