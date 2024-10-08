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

# Extended functionality: Filter analytics data by date range
@bp.route('/filter', methods=['GET'])
@jwt_required()
def filter_analytics():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Assuming your 'data' field contains structured data including a 'timestamp' field
    analytics = Analytics.query.filter(Analytics.timestamp >= start_date, Analytics.timestamp <= end_date).all()

    return jsonify([{'id': a.id, 'data': a.data} for a in analytics])

# Extended functionality: Aggregate analytics data (e.g., count, average, etc.)
@bp.route('/aggregate', methods=['GET'])
@jwt_required()
def aggregate_analytics():
    # Example: Count the total number of analytics entries
    total_count = db.session.query(func.count(Analytics.id)).scalar()

    # Example: Aggregate data based on some criteria (e.g., sales figures, interaction data, etc.)
    # Modify this depending on the structure of your 'data' field
    total_value = db.session.query(func.sum(func.cast(Analytics.data['value'], db.Float))).scalar()

    return jsonify({
        'total_count': total_count,
        'total_value': total_value
    })

# Extended functionality: Get the most recent analytics entries (for dashboard insights)
@bp.route('/recent', methods=['GET'])
@jwt_required()
def recent_analytics():
    recent_entries = Analytics.query.order_by(Analytics.timestamp.desc()).limit(5).all()

    return jsonify([{'id': a.id, 'data': a.data, 'timestamp': a.timestamp} for a in recent_entries])
