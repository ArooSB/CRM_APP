from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Interaction, Customer
from flask_jwt_extended import jwt_required
from datetime import datetime

bp = Blueprint('interactions', __name__, url_prefix='/interactions')


@bp.route('/', methods=['GET'])
@jwt_required()
def get_interactions():
    """
    Retrieve all interactions, optionally filtering by customer ID, with pagination.

    Query parameters:
        customer_id (int): Optional filter to retrieve interactions for a specific customer.
        page (int): The page number for pagination (default is 1).
        per_page (int): The number of results per page (default is 10).

    Returns:
        A JSON response containing a paginated list of interactions and pagination details.
    """
    customer_id = request.args.get('customer_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Interaction.query

    if customer_id:
        query = query.filter_by(customer_id=customer_id)

    interactions = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'interactions': [{
            'id': i.id,
            'customer_id': i.customer_id,
            'notes': i.notes,
            'created_at': i.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for i in interactions.items],
        'total': interactions.total,
        'pages': interactions.pages,
        'current_page': interactions.page
    })


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_interaction(id):
    """
    Retrieve a single interaction by ID.

    Args:
        id (int): The ID of the interaction to retrieve.

    Returns:
        A JSON response containing the details of the requested interaction.
    """
    interaction = Interaction.query.get_or_404(id)
    return jsonify({
        'id': interaction.id,
        'customer_id': interaction.customer_id,
        'notes': interaction.notes,
        'created_at': interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@bp.route('/', methods=['POST'])
@jwt_required()
def create_interaction():
    """
    Create a new interaction for a specific customer.

    Request body:
        A JSON object containing the customer_id and notes for the interaction.

    Returns:
        A JSON response indicating the success of the operation and the ID of the newly created interaction.
    """
    data = request.get_json()

    if not data.get('customer_id') or not data.get('notes'):
        return jsonify({'message': 'Missing required fields: customer_id, notes'}), 400

    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    interaction = Interaction(
        customer_id=data['customer_id'],
        notes=data['notes'],
        created_at=datetime.utcnow()
    )

    try:
        db.session.add(interaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating interaction', 'error': str(e)}), 500

    return jsonify({
        'id': interaction.id,
        'message': 'Interaction created successfully'
    }), 201


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_interaction(id):
    """
    Update an existing interaction by ID.

    Args:
        id (int): The ID of the interaction to update.

    Request body:
        A JSON object containing the updated notes for the interaction.

    Returns:
        A JSON response indicating the success of the update operation.
    """
    interaction = Interaction.query.get_or_404(id)
    data = request.get_json()

    if 'notes' in data:
        interaction.notes = data['notes']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating interaction', 'error': str(e)}), 500

    return jsonify({'message': 'Interaction updated successfully'})


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_interaction(id):
    """
    Delete an interaction by ID.

    Args:
        id (int): The ID of the interaction to delete.

    Returns:
        A JSON response indicating the success of the delete operation.
    """
    interaction = Interaction.query.get_or_404(id)

    try:
        db.session.delete(interaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting interaction', 'error': str(e)}), 500

    return jsonify({'message': 'Interaction deleted successfully'})


def register_routes(app):
    """
    Register the interactions blueprint routes with the Flask application.

    Args:
        app (Flask): The Flask application instance.
    """
    app.register_blueprint(bp)
