from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Worker
from flask_jwt_extended import create_access_token, jwt_required

bp = Blueprint('workers', __name__, url_prefix='/workers')

# Register Worker
@bp.route('/register', methods=['POST'])
def register_worker():
    data = request.get_json()
    print(f"Registering worker with data: {data}")  # Debug print
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if Worker.query.filter_by(username=username).first():
        print(f"Username '{username}' already exists.")  # Debug print
        return jsonify({'message': 'Username already exists'}), 400

    worker = Worker(username=username, role=role)
    worker.set_password(password)

    try:
        db.session.add(worker)
        db.session.commit()
        print(f"Worker '{username}' registered successfully.")  # Debug print
    except Exception as e:
        db.session.rollback()
        print(f"Error registering worker: {e}")  # Debug print
        return jsonify({'message': 'Error registering worker', 'error': str(e)}), 500

    return jsonify({'message': 'Worker registered successfully'}), 201

# Login Worker
@bp.route('/login', methods=['POST'])
def login_worker():
    data = request.get_json()
    print(f"Logging in worker with data: {data}")  # Debug print
    username = data.get('username')
    password = data.get('password')

    worker = Worker.query.filter_by(username=username).first()
    if worker and worker.check_password(password):
        access_token = create_access_token(identity=worker.id)
        print(f"Worker '{username}' logged in successfully.")  # Debug print
        return jsonify({'access_token': access_token}), 200

    print(f"Invalid credentials for username '{username}'.")  # Debug print
    return jsonify({'message': 'Invalid credentials'}), 401

# Logout Worker
@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_worker():
    print("Worker logged out.")  # Debug print
    return jsonify({'message': 'Logged out'}), 200

# Get all workers with optional filters (position) and pagination
@bp.route('/', methods=['GET'])
@jwt_required()
def get_workers():
    position = request.args.get('position')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    print(f"Fetching workers with position: {position}, page: {page}, per_page: {per_page}")  # Debug print
    query = Worker.query

    # Optionally filter by position
    if position:
        query = query.filter_by(position=position)

    # Paginate the query result
    workers = query.paginate(page=page, per_page=per_page, error_out=False)

    print(f"Total workers found: {workers.total}")  # Debug print
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
    print(f"Fetching worker with ID: {id}")  # Debug print
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
    print(f"Creating worker with data: {data}")  # Debug print

    # Validate the required fields
    if not data.get('name') or not data.get('email') or not data.get('position'):
        print("Missing required fields: name, email, position")  # Debug print
        return jsonify({'message': 'Missing required fields: name, email, position'}), 400

    # Check if the email already exists
    existing_worker = Worker.query.filter_by(email=data['email']).first()
    if existing_worker:
        print(f"Worker with email '{data['email']}' already exists.")  # Debug print
        return jsonify({'message': 'Worker with this email already exists'}), 409

    worker = Worker(
        name=data['name'],
        email=data['email'],
        position=data['position']
    )

    try:
        db.session.add(worker)
        db.session.commit()
        print(f"Worker created successfully with ID: {worker.id}")  # Debug print
    except Exception as e:
        db.session.rollback()
        print(f"Error creating worker: {e}")  # Debug print
        return jsonify({'message': 'Error creating worker', 'error': str(e)}), 500

    return jsonify({'id': worker.id, 'message': 'Worker created successfully'}), 201

# Update an existing worker by ID
@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_worker(id):
    print(f"Updating worker with ID: {id}")  # Debug print
    worker = Worker.query.get_or_404(id)
    data = request.get_json()

    # Update fields only if provided
    if 'name' in data:
        worker.name = data['name']
        print(f"Updated name to: {worker.name}")  # Debug print
    if 'email' in data:
        worker.email = data['email']
        print(f"Updated email to: {worker.email}")  # Debug print
    if 'position' in data:
        worker.position = data['position']
        print(f"Updated position to: {worker.position}")  # Debug print

    # Check if the email is already taken by another worker
    existing_worker = Worker.query.filter(Worker.email == worker.email, Worker.id != worker.id).first()
    if existing_worker:
        print(f"Worker with email '{worker.email}' already exists.")  # Debug print
        return jsonify({'message': 'Worker with this email already exists'}), 409

    try:
        db.session.commit()
        print("Worker updated successfully.")  # Debug print
    except Exception as e:
        db.session.rollback()
        print(f"Error updating worker: {e}")  # Debug print
        return jsonify({'message': 'Error updating worker', 'error': str(e)}), 500

    return jsonify({'message': 'Worker updated successfully'})

# Delete a worker by ID
@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_worker(id):
    print(f"Deleting worker with ID: {id}")  # Debug print
    worker = Worker.query.get_or_404(id)

    try:
        db.session.delete(worker)
        db.session.commit()
        print("Worker deleted successfully.")  # Debug print
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting worker: {e}")  # Debug print
        return jsonify({'message': 'Error deleting worker', 'error': str(e)}), 500

    return jsonify({'message': 'Worker deleted successfully'})

# Register the Blueprint
def register_routes(app):
    app.register_blueprint(bp)
