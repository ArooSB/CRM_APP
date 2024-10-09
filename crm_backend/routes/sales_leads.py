from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import SalesLead, Customer
from flask_jwt_extended import jwt_required
from datetime import datetime

bp = Blueprint('sales_leads', __name__, url_prefix='/sales_leads')

# Get all sales leads with optional filters (customer ID, status) and pagination
@bp.route('/', methods=['GET'])
@jwt_required()
def get_sales_leads():
    customer_id = request.args.get('customer_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = SalesLead.query

    # Optionally filter by customer ID
    if customer_id:
        query = query.filter_by(customer_id=customer_id)

    # Optionally filter by status
    if status:
        query = query.filter_by(status=status)

    # Paginate the query result
    sales_leads = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'sales_leads': [{
            'id': sl.id,
            'customer_id': sl.customer_id,
            'status': sl.status,
            'created_at': sl.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for sl in sales_leads.items],
        'total': sales_leads.total,
        'pages': sales_leads.pages,
        'current_page': sales_leads.page
    })

# Get a single sales lead by ID
@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_sales_lead(id):
    sales_lead = SalesLead.query.get_or_404(id)
    return jsonify({
        'id': sales_lead.id,
        'customer_id': sales_lead.customer_id,
        'status': sales_lead.status,
        'created_at': sales_lead.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

# Create a new sales lead
@bp.route('/', methods=['POST'])
@jwt_required()
def create_sales_lead():
    data = request.get_json()

    # Validate the required fields
    if not data.get('customer_id') or not data.get('status'):
        return jsonify({'message': 'Missing required fields: customer_id, status'}), 400

    # Ensure that the customer exists before creating a sales lead
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    sales_lead = SalesLead(
        customer_id=data['customer_id'],
        status=data['status']
    )

    try:
        db.session.add(sales_lead)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating sales lead', 'error': str(e)}), 500

    return jsonify({'id': sales_lead.id, 'message': 'Sales lead created successfully'}), 201

# Update an existing sales lead by ID
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_sales_lead(id):
    sales_lead = SalesLead.query.get_or_404(id)
    data = request.get_json()

    # Update fields only if provided
    if 'status' in data:
        sales_lead.status = data['status']

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating sales lead', 'error': str(e)}), 500

    return jsonify({'message': 'Sales lead updated successfully'})

# Delete a sales lead by ID
@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_sales_lead(id):
    sales_lead = SalesLead.query.get_or_404(id)

    try:
        db.session.delete(sales_lead)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting sales lead', 'error': str(e)}), 500

    return jsonify({'message': 'Sales lead deleted successfully'})

# Register the Blueprint
def register_routes(app):
    app.register_blueprint(bp)
s