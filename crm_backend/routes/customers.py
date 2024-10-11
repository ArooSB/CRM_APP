from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Customer
from flask_jwt_extended import jwt_required
import re

bp = Blueprint('customers', __name__, url_prefix='/customers')


def is_valid_email(email):
    """
    Validate the format of an email address.

    Args:
        email (str): The email address to validate.

    Returns:
        bool: True if the email is valid, False otherwise.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


@bp.route('/', methods=['GET'])
@jwt_required()
def get_customers():
    """
    Retrieve all customers, with optional search and pagination.

    Query parameters:
        search (str): Optional search term to filter customers by first name, last name, or email.
        page (int): The page number for pagination (default is 1).
        per_page (int): The number of results per page (default is 10).

    Returns:
        A JSON response containing a paginated list of customers and pagination details.
    """
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Customer.query

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


@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    """
    Retrieve a single customer by ID.

    Args:
        id (int): The ID of the customer to retrieve.

    Returns:
        A JSON response containing the details of the requested customer.
    """
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


@bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    """
    Create a new customer.

    Request body:
        A JSON object containing customer details (first_name, last_name, email, phone, company, address).

    Returns:
        A JSON response indicating the success of the operation and the ID of the newly created customer.
    """
    data = request.get_json()

    if not data.get('first_name') or not data.get('last_name') or not data.get('email'):
        return jsonify({'message': 'Missing required fields: first_name, last_name, email'}), 400

    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400

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

    try:
        db.session.add(customer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating customer', 'error': str(e)}), 500

    return jsonify({'id': customer.id, 'message': 'Customer created successfully'}), 201


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    """
    Update an existing customer by ID.

    Args:
        id (int): The ID of the customer to update.

    Request body:
        A JSON object containing the updated customer details.

    Returns:
        A JSON response indicating the success of the update operation.
    """
    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    customer.first_name = data.get('first_name', customer.first_name)
    customer.last_name = data.get('last_name', customer.last_name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.company = data.get('company', customer.company)
    customer.address = data.get('address', customer.address)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating customer', 'error': str(e)}), 500

    return jsonify({'message': 'Customer updated successfully'})


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    """
    Delete a customer by ID.

    Args:
        id (int): The ID of the customer to delete.

    Returns:
        A JSON response indicating the success of the delete operation.
    """
    customer = Customer.query.get_or_404(id)

    try:
        db.session.delete(customer)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting customer', 'error': str(e)}), 500

    return jsonify({'message': 'Customer deleted successfully'})
