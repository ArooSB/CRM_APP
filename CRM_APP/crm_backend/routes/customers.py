from flask import Blueprint, request, jsonify
from crm_backend import db
from crm_backend.models import Customer
from flask_jwt_extended import jwt_required

bp = Blueprint('customers', __name__, url_prefix='/customers')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.first_name} for c in customers])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({'id': customer.id, 'first_name': customer.first_name})

@bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    data = request.get_json()
    customer = Customer(first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id, 'message': 'Customer created'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    customer.first_name = data['first_name']
    db.session.commit()
    return jsonify({'message': 'Customer updated'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'})
