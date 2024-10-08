from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Customer
from flask_jwt_extended import jwt_required

bp = Blueprint('customers', __name__, url_prefix='/customers')

# Get all customers with optional search and pagination
@bp.route('/', methods=['GET'])
@jwt_required()
def get_customers():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Customer.query

    # Optional search by name or email
    if search:
        query = query.filter(
            (Customer.first_name.ilike(f'%{search}%')) |
            (Customer.last_name.ilike(f'%{search}%')) |
            (Customer.email.ilike(f'%{search}%'))
        )

    customers = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'customers': [{
            'id': c.id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email': c.email,
            'phone': c.phone,
            'company': c.company,
            'address': c.address
        } for c in customers.items],
        'total': customers.total,
        'pages': customers.pages,
        'current_page': customers.page
    })

# Get a single customer by ID
@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({
        'id': customer.id,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'email': customer.email,
        'phone': customer.phone,
        'company': customer.company,
        'address': customer.address
    })

# Create a new customer
@bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()

    # Validate required fields
    if not data.get('first_name') or not data.get('last_name') or not data.get('email'):
        return jsonify({'message': 'Missing required fields: first_name, last_name, email'}), 400

    # Check for existing customer with the same email
    if Customer.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Customer with this email already exists'}), 400

    customer = Customer(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone=data.get('phone'),
        company=data.get('company'),
        address=data.get('address')
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id, 'message': 'Customer created successfully'}), 201

# Update an existing customer
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    # Update customer fields if provided in the request
    customer.first_name = data.get('first_name', customer.first_name)
    customer.last_name = data.get('last_name', customer.last_name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.company = data.get('company', customer.company)
    customer.address = data.get('address', customer.address)

    db.session.commit()
    return jsonify({'message': 'Customer updated successfully'})

# Delete a customer by ID
@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})
