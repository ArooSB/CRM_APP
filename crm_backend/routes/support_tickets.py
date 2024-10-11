from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import SupportTicket, Customer
from flask_jwt_extended import jwt_required


bp = Blueprint('support_tickets', __name__, url_prefix='/support_tickets')


@bp.route('/', methods=['GET'])
@jwt_required()
def get_support_tickets():
    """
    Retrieve a list of support tickets.

    Supports optional filtering by customer ID and status, along with pagination.
    """
    customer_id = request.args.get('customer_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = SupportTicket.query

    if customer_id:
        query = query.filter_by(customer_id=customer_id)

    if status:
        query = query.filter_by(status=status)

    support_tickets = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'support_tickets': [{
            'id': ticket.id,
            'customer_id': ticket.customer_id,
            'description': ticket.description,
            'status': ticket.status,
            'created_at': ticket.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for ticket in support_tickets.items],
        'total': support_tickets.total,
        'pages': support_tickets.pages,
        'current_page': support_tickets.page
    })


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_support_ticket(id):
    """
    Retrieve a specific support ticket by its ID.
    """
    support_ticket = SupportTicket.query.get_or_404(id)
    return jsonify({
        'id': support_ticket.id,
        'customer_id': support_ticket.customer_id,
        'description': support_ticket.description,
        'status': support_ticket.status,
        'created_at': support_ticket.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@bp.route('/status', methods=['GET'])
@jwt_required()
def get_ticket_status():
    """
    Retrieve the count of support tickets based on their status.
    """
    active = SupportTicket.query.filter_by(status='active').count()
    deactivated = SupportTicket.query.filter_by(status='deactivated').count()
    in_process = SupportTicket.query.filter_by(status='in process').count()

    return jsonify({
        'active': active,
        'deactivated': deactivated,
        'inProcess': in_process
    })


@bp.route('/', methods=['POST'])
@jwt_required()
def create_support_ticket():
    """
    Create a new support ticket.
    """
    data = request.get_json()

    if not data.get('customer_id') or not data.get('description') or not data.get('status'):
        return jsonify({'message': 'Missing required fields: customer_id, description, status'}), 400

    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    support_ticket = SupportTicket(
        customer_id=data['customer_id'],
        description=data['description'],
        status=data['status']
    )

    try:
        db.session.add(support_ticket)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating support ticket', 'error': str(e)}), 500

    return jsonify({'id': support_ticket.id, 'message': 'Support ticket created successfully'}), 201


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_support_ticket(id):
    """
    Update an existing support ticket by its ID.
    """
    support_ticket = SupportTicket.query.get_or_404(id)
    data = request.get_json()

    if 'description' in data:
        support_ticket.description = data['description']
    if 'status' in data:
        support_ticket.status = data['status']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating support ticket', 'error': str(e)}), 500

    return jsonify({'message': 'Support ticket updated successfully'})


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_support_ticket(id):
    """
    Delete a specific support ticket by its ID.
    """
    support_ticket = SupportTicket.query.get_or_404(id)

    try:
        db.session.delete(support_ticket)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting support ticket', 'error': str(e)}), 500

    return jsonify({'message': 'Support ticket deleted successfully'})


def register_routes(app):
    """
    Register the support tickets Blueprint with the Flask application.
    """
    app.register_blueprint(bp)
