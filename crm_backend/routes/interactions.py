from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Interaction, Customer
from flask_jwt_extended import jwt_required

bp = Blueprint('interactions', __name__, url_prefix='/interactions')

# Get all interactions with optional search by customer ID and pagination
@bp.route('/', methods=['GET'])
@jwt_required()
def get_interactions():
    customer_id = request.args.get('customer_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Interaction.query

    # Optionally filter by customer ID
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

# Get a single interaction by ID
@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_interaction(id):
    interaction = Interaction.query.get_or_404(id)
    return jsonify({
        'id': interaction.id,
        'customer_id': interaction.customer_id,
        'notes': interaction.notes,
        'created_at': interaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

# Create a new interaction
@bp.route('/', methods=['POST'])
@jwt_required()
def create_interaction():
    data = request.get_json()

    # Validate the required fields
    if not data.get('customer_id') or not data.get('notes'):
        return jsonify({'message': 'Missing required fields: customer_id, notes'}), 400

    # Check if the customer exists before creating the interaction
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    interaction = Interaction(
        customer_id=data['customer_id'],
        notes=data['notes']
    )
    db.session.add(interaction)
    db.session.commit()

    return jsonify({
        'id': interaction.id,
        'message': 'Interaction created successfully'
    }), 201

# Update an existing interaction by ID
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_interaction(id):
    interaction = Interaction.query.get_or_404(id)
    data = request.get_json()

    # Update notes field only if provided
    interaction.notes = data.get('notes', interaction.notes)
    db.session.commit()

    return jsonify({'message': 'Interaction updated successfully'})

# Delete an interaction by ID
@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_interaction(id):
    interaction = Interaction.query.get_or_404(id)
    db.session.delete(interaction)
    db.session.commit()

    return jsonify({'message': 'Interaction deleted successfully'})
