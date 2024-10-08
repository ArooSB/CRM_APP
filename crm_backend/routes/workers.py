from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Worker
from flask_jwt_extended import jwt_required

bp = Blueprint('workers', __name__, url_prefix='/workers')


# Get all workers with optional filters (position) and pagination
@bp.route('/', methods=['GET'])
@jwt_required()
def get_workers():
    position = request.args.get('position')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Worker.query

    # Optionally filter by position
    if position:
        query = query.filter_by(position=position)

    # Paginate the query result
    workers = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'workers': [{
            'id': w.id,
            'name': w.name,
            'email': w.email,
            'position': w.position
        } for w in workers.items],
        'total': workers.total,
        'pages': workers.pages,
        'current_page': workers.page
    })


# Get a single worker by ID
@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_worker(id):
    worker = Worker.query.get_or_404(id)
    return jsonify({
        'id': worker.id,
        'name': worker.name,
        'email': worker.email,
        'position': worker.position
    })


# Create a new worker
@bp.route('/', methods=['POST'])
@jwt_required()
def create_worker():
    data = request.get_json()

    # Validate the required fields
    if not data.get('name') or not data.get('email') or not data.get(
            'position'):
        return jsonify(
            {'message': 'Missing required fields: name, email, position'}), 400

    # Check if the email already exists
    existing_worker = Worker.query.filter_by(email=data['email']).first()
    if existing_worker:
        return jsonify(
            {'message': 'Worker with this email already exists'}), 409

    worker = Worker(
        name=data['name'],
        email=data['email'],
        position=data['position']
    )
    db.session.add(worker)
    db.session.commit()
    return jsonify(
        {'id': worker.id, 'message': 'Worker created successfully'}), 201


# Update an existing worker by ID
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_worker(id):
    worker = Worker.query.get_or_404(id)
    data = request.get_json()

    # Update fields only if provided
    worker.name = data.get('name', worker.name)
    worker.email = data.get('email', worker.email)
    worker.position = data.get('position', worker.position)

    # Check if the email is already taken by another worker
    existing_worker = Worker.query.filter(Worker.email == worker.email,
                                          Worker.id != worker.id).first()
    if existing_worker:
        return jsonify(
            {'message': 'Worker with this email already exists'}), 409

    db.session.commit()
    return jsonify({'message': 'Worker updated successfully'})


# Delete a worker by ID
@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_worker(id):
    worker = Worker.query.get_or_404(id)
    db.session.delete(worker)
    db.session.commit()
    return jsonify({'message': 'Worker deleted successfully'})
