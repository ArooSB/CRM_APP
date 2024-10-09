from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Analytics
from flask_jwt_extended import jwt_required
from sqlalchemy import func

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

# Get all analytics entries
@bp.route('/', methods=['GET'])
@jwt_required()
def get_analytics():
    analytics = Analytics.query.all()
    return jsonify([{'id': a.id, 'data': a.data} for a in analytics])

# Get a single analytics entry by ID
@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_analytic(id):
    analytic = Analytics.query.get_or_404(id)
    return jsonify({'id': analytic.id, 'data': analytic.data})

# Create a new analytics entry
@bp.route('/', methods=['POST'])
@jwt_required()
def create_analytic():
    data = request.get_json()
    analytic = Analytics(data=data['data'])
    db.session.add(analytic)
    db.session.commit()
    return jsonify({'id': analytic.id, 'message': 'Analytics entry created successfully'}), 201

# Update an existing analytics entry
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_analytic(id):
    analytic = Analytics.query.get_or_404(id)
    data = request.get_json()
    analytic.data = data.get('data', analytic.data)
    db.session.commit()
    return jsonify({'message': 'Analytics entry updated successfully'})

# Delete an analytics entry
@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_analytic(id):
    analytic = Analytics.query.get_or_404(id)
    db.session.delete(analytic)
    db.session.commit()
    return jsonify({'message': 'Analytics entry deleted successfully'})

# General analytics endpoint: filter by date and aggregate
@bp.route('/filter_aggregate', methods=['GET'])
@jwt_required()
def filter_and_aggregate_analytics():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Filter by date range if provided
    query = Analytics.query
    if start_date:
        query = query.filter(Analytics.timestamp >= start_date)
    if end_date:
        query = query.filter(Analytics.timestamp <= end_date)

    # Retrieve filtered analytics data
    analytics = query.all()

    # Aggregate on the filtered data
    total_count = db.session.query(func.count(Analytics.id)).filter(Analytics.timestamp >= start_date, Analytics.timestamp <= end_date).scalar()

    # Example aggregation based on a 'value' field in the 'data' (assuming JSON structure with numeric data)
    # You can replace 'value' with whatever key you need from the 'data' field
    total_value = db.session.query(func.sum(func.cast(Analytics.data['value'], db.Float))).filter(Analytics.timestamp >= start_date, Analytics.timestamp <= end_date).scalar()

    return jsonify({
        'total_count': total_count,
        'total_value': total_value,
        'analytics': [{'id': a.id, 'data': a.data, 'timestamp': a.timestamp} for a in analytics]
    })

# Extended functionality: Get the most recent analytics entries (for dashboard insights)
@bp.route('/recent', methods=['GET'])
@jwt_required()
def recent_analytics():
    recent_entries = Analytics.query.order_by(Analytics.timestamp.desc()).limit(5).all()

    return jsonify([{'id': a.id, 'data': a.data, 'timestamp': a.timestamp} for a in recent_entries])
