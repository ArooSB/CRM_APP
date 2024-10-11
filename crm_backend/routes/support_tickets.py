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

    Query Parameters:
        - customer_id (int, optional): The ID of the customer associated with the support tickets.
        - status (str, optional): The status of the support tickets to filter by.
        - page (int, optional): The page number for pagination (default is 1).
        - per_page (int, optional): The number of tickets to return per page (default is 10).

    Returns:
        JSON response containing:
            - support_tickets (list): A list of support tickets with fields id, customer_id, description, status, and created_at.
            - total (int): Total number of support tickets that match the filters.
            - pages (int): Total number of pages available based on pagination.
            - current_page (int): The current page number being viewed.
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

    support_tickets = query.paginate(page=page, per_page=per_page,
                                     error_out=False)

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

    Args:
        id (int): The ID of the support ticket to retrieve.

    Returns:
        JSON response containing:
            - id (int): The ID of the support ticket.
            - customer_id (int): The ID of the customer associated with the support ticket.
            - description (str): The description of the support ticket.
            - status (str): The current status of the support ticket.
            - created_at (str): The timestamp when the support ticket was created, formatted as 'YYYY-MM-DD HH:MM:SS'.

    Raises:
        404: If the support ticket with the given ID does not exist.
    """
    support_ticket = SupportTicket.query.get_or_404(id)
    return jsonify({
        'id': support_ticket.id,
        'customer_id': support_ticket.customer_id,
        'description': support_ticket.description,
        'status': support_ticket.status,
        'created_at': support_ticket.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@bp.route('/', methods=['POST'])
@jwt_required()
def create_support_ticket():
    """
    Create a new support ticket.

    The request must include the customer ID, description, and status.

    Request Body:
        JSON object containing:
            - customer_id (int): The ID of the customer associated with the support ticket.
            - description (str): A description of the support ticket.
            - status (str): The current status of the support ticket.

    Returns:
        JSON response containing:
            - id (int): The ID of the newly created support ticket.
            - message (str): Confirmation message indicating successful creation.

    Raises:
        400: If any required fields are missing.
        404: If the specified customer does not exist.
    """
    data = request.get_json()

    if not data.get('customer_id') or not data.get(
            'description') or not data.get('status'):
        return jsonify({
                           'message': 'Missing required fields: customer_id, description, status'}), 400

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
        return jsonify(
            {'message': 'Error creating support ticket', 'error': str(e)}), 500

    return jsonify({'id': support_ticket.id,
                    'message': 'Support ticket created successfully'}), 201


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_support_ticket(id):
    """
    Update an existing support ticket by its ID.

    The request can include any combination of fields to be updated.

    Request Body:
        JSON object containing any of the following optional fields:
            - description (str): Updated description of the support ticket.
            - status (str): Updated status of the support ticket.

    Args:
        id (int): The ID of the support ticket to update.

    Returns:
        JSON response containing:
            - message (str): Confirmation message indicating successful update.

    Raises:
        404: If the support ticket with the given ID does not exist.
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
        return jsonify(
            {'message': 'Error updating support ticket', 'error': str(e)}), 500

    return jsonify({'message': 'Support ticket updated successfully'})


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_support_ticket(id):
    """
    Delete a specific support ticket by its ID.

    Args:
        id (int): The ID of the support ticket to delete.

    Returns:
        JSON response containing:
            - message (str): Confirmation message indicating successful deletion.

    Raises:
        404: If the support ticket with the given ID does not exist.
    """
    support_ticket = SupportTicket.query.get_or_404(id)

    try:
        db.session.delete(support_ticket)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {'message': 'Error deleting support ticket', 'error': str(e)}), 500

    return jsonify({'message': 'Support ticket deleted successfully'})


def register_routes(app):
    """
    Register the support tickets Blueprint with the Flask application.

    Args:
        app (Flask): The Flask application instance to register the Blueprint with.
    """
    app.register_blueprint(bp)
