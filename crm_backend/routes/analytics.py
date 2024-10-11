from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Analytics
from flask_jwt_extended import jwt_required
from sqlalchemy import func

bp = Blueprint('analytics', __name__, url_prefix='/analytics')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_analytics():
    """
    Retrieve all analytics entries from the database.

    Returns:
        A JSON response containing all analytics entries in the database.
    """
    analytics = Analytics.query.all()
    return jsonify([{'id': a.id, 'data': a.data} for a in analytics])

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_analytic(id):
    """
    Retrieve a specific analytics entry by its ID.

    Args:
        id (int): The ID of the analytics entry to retrieve.

    Returns:
        A JSON response containing the details of the requested analytics entry.
    """
    analytic = Analytics.query.get_or_404(id)
    return jsonify({'id': analytic.id, 'data': analytic.data})

@bp.route('/', methods=['POST'])
@jwt_required()
def create_analytic():
    """
    Create a new analytics entry.

    Request body:
        data (JSON): A JSON object containing the data for the new analytics entry.

    Returns:
        A JSON response indicating the success of the operation and the ID of the newly created entry.
    """
    data = request.get_json()
    analytic = Analytics(data=data['data'])
    db.session.add(analytic)
    db.session.commit()
    return jsonify({'id': analytic.id, 'message': 'Analytics entry created successfully'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_analytic(id):
    """
    Update an existing analytics entry by its ID.

    Args:
        id (int): The ID of the analytics entry to update.

    Request body:
        data (JSON): A JSON object containing the updated data for the analytics entry.

    Returns:
        A JSON response indicating the success of the update operation.
    """
    analytic = Analytics.query.get_or_404(id)
    data = request.get_json()
    analytic.data = data.get('data', analytic.data)
    db.session.commit()
    return jsonify({'message': 'Analytics entry updated successfully'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_analytic(id):
    """
    Delete an existing analytics entry by its ID.

    Args:
        id (int): The ID of the analytics entry to delete.

    Returns:
        A JSON response indicating the success of the delete operation.
    """
    analytic = Analytics.query.get_or_404(id)
    db.session.delete(analytic)
    db.session.commit()
    return jsonify({'message': 'Analytics entry deleted successfully'})

@bp.route('/filter_aggregate', methods=['GET'])
@jwt_required()
def filter_and_aggregate_analytics():
    """
    Filter analytics entries by a date range and aggregate the data.

    Query parameters:
        start_date (str): The start date for filtering analytics entries.
        end_date (str): The end date for filtering analytics entries.

    Returns:
        A JSON response containing the filtered analytics data, total count of entries, and the sum of the 'value' field.
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Analytics.query
    if start_date:
        query = query.filter(Analytics.timestamp >= start_date)
    if end_date:
        query = query.filter(Analytics.timestamp <= end_date)

    analytics = query.all()
    total_count = db.session.query(func.count(Analytics.id)).filter(Analytics.timestamp >= start_date, Analytics.timestamp <= end_date).scalar()
    total_value = db.session.query(func.sum(func.cast(Analytics.data['value'], db.Float))).filter(Analytics.timestamp >= start_date, Analytics.timestamp <= end_date).scalar()

    return jsonify({
        'total_count': total_count,
        'total_value': total_value,
        'analytics': [{'id': a.id, 'data': a.data, 'timestamp': a.timestamp} for a in analytics]
    })

@bp.route('/recent', methods=['GET'])
@jwt_required()
def recent_analytics():
    """
    Retrieve the most recent analytics entries, ordered by their timestamp.

    Returns:
        A JSON response containing the five most recent analytics entries.
    """
    recent_entries = Analytics.query.order_by(Analytics.timestamp.desc()).limit(5).all()
    return jsonify([{'id': a.id, 'data': a.data, 'timestamp': a.timestamp} for a in recent_entries])
