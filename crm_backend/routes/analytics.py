from flask import Blueprint, request, jsonify
from crm_backend import db
from crm_backend.models import Analytics
from flask_jwt_extended import jwt_required

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_analytics():
    analytics = Analytics.query.all()
    return jsonify([{'id': a.id, 'data': a.data} for a in analytics])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_analytic(id):
    analytic = Analytics.query.get_or_404(id)
    return jsonify({'id': analytic.id, 'data': analytic.data})

@bp.route('/', methods=['POST'])
@jwt_required()
def create_analytic():
    data = request.get_json()
    analytic = Analytics(data=data['data'])
    db.session.add(analytic)
    db.session.commit()
    return jsonify({'id': analytic.id, 'message': 'Analytics entry created'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_analytic(id):
    analytic = Analytics.query.get_or_404(id)
    data = request.get_json()
    analytic.data = data['data']
    db.session.commit()
    return jsonify({'message': 'Analytics entry updated'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_analytic(id):
    analytic = Analytics.query.get_or_404(id)
    db.session.delete(analytic)
    db.session.commit()
    return jsonify({'message': 'Analytics entry deleted'})
