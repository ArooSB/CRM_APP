from flask import Blueprint, request, jsonify
from crm_backend import db
from crm_backend.models import SalesLead
from flask_jwt_extended import jwt_required

bp = Blueprint('sales_leads', __name__, url_prefix='/sales_leads')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_sales_leads():
    sales_leads = SalesLead.query.all()
    return jsonify([{'id': lead.id, 'customer_id': lead.customer_id, 'status': lead.status} for lead in sales_leads])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_sales_lead(id):
    sales_lead = SalesLead.query.get_or_404(id)
    return jsonify({'id': sales_lead.id, 'customer_id': sales_lead.customer_id, 'status': sales_lead.status})

@bp.route('/', methods=['POST'])
@jwt_required()
def create_sales_lead():
    data = request.get_json()
    sales_lead = SalesLead(customer_id=data['customer_id'], status=data['status'])
    db.session.add(sales_lead)
    db.session.commit()
    return jsonify({'id': sales_lead.id, 'message': 'Sales Lead created'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_sales_lead(id):
    sales_lead = SalesLead.query.get_or_404(id)
    data = request.get_json()
    sales_lead.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Sales Lead updated'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_sales_lead(id):
    sales_lead = SalesLead.query.get_or_404(id)
    db.session.delete(sales_lead)
    db.session.commit()
    return jsonify({'message': 'Sales Lead deleted'})
