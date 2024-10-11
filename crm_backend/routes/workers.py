from flask import Blueprint, request, jsonify
from crm_backend.backend_app import db
from crm_backend.models import Worker
from flask_jwt_extended import create_access_token, jwt_required

bp = Blueprint('workers', __name__, url_prefix='/workers')

@bp.route('/register', methods=['POST'])
def register_worker():
    """
    Registers a new worker.
    Expects a JSON body with 'username', 'password', and 'role'.
    Returns a 201 status on successful registration,
    or a 400 if the username already exists.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if Worker.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    worker = Worker(username=username, role=role)
    worker.set_password(password)

    try:
        db.session.add(worker)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error registering worker', 'error': str(e)}), 500

    return jsonify({'message': 'Worker registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login_worker():
    """
    Logs in a worker.
    Expects a JSON body with 'username' and 'password'.
    Returns a JWT access token on successful login, or a 401 on invalid credentials.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    worker = Worker.query.filter_by(username=username).first()
    if worker and worker.check_password(password):
        access_token = create_access_token(identity=worker.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_worker():
    """
    Logs out a worker.
    This endpoint requires a valid JWT token.
    """
    return jsonify({'message': 'Logged out'}), 200

@bp.route('/', methods=['GET'])
@jwt_required()
def get_workers():
    """
    Fetches all workers, with optional filters for 'position' and pagination.
    This endpoint requires a valid JWT token.
    """
    position = request.args.get('position')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Worker.query

    if position:
        query = query.filter_by(position=position)

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

@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_worker(id):
    """
    Fetches a worker by their ID.
    This endpoint requires a valid JWT token.
    """
    worker = Worker.query.get_or_404(id)
    return jsonify({
        'id': worker.id,
        'name': worker.name,
        'email': worker.email,
        'position': worker.position
    })

@bp.route('/', methods=['POST'])
@jwt_required()
def create_worker():
    """
    Creates a new worker.
    Expects a JSON body with 'name', 'email', and 'position'.
    Returns a 201 status on successful creation,
    or a 400 if required fields are missing, or a 409 if the email already exists.
    """
    data = request.get_json()

    if not data.get('name') or not data.get('email') or not data.get('position'):
        return jsonify({'message': 'Missing required fields: name, email, position'}), 400

    existing_worker = Worker.query.filter_by(email=data['email']).first()
    if existing_worker:
        return jsonify({'message': 'Worker with this email already exists'}), 409

    worker = Worker(
        name=data['name'],
        email=data['email'],
        position=data['position']
    )

    try:
        db.session.add(worker)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error creating worker', 'error': str(e)}), 500

    return jsonify({'id': worker.id, 'message': 'Worker created successfully'}), 201

@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_worker(id):
    """
    Updates an existing worker by their ID.
    Expects a JSON body with fields to update ('name', 'email', 'position').
    This endpoint requires a valid JWT token.
    """
    worker = Worker.query.get_or_404(id)
    data = request.get_json()

    if 'name' in data:
        worker.name = data['name']
    if 'email' in data:
        worker.email = data['email']
    if 'position' in data:
        worker.position = data['position']

    existing_worker = Worker.query.filter(Worker.email == worker.email, Worker.id != worker.id).first()
    if existing_worker:
        return jsonify({'message': 'Worker with this email already exists'}), 409

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error updating worker', 'error': str(e)}), 500

    return jsonify({'message': 'Worker updated successfully'})

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_worker(id):
    """
    Deletes a worker by their ID.
    This endpoint requires a valid JWT token.
    """
    worker = Worker.query.get_or_404(id)

    try:
        db.session.delete(worker)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error deleting worker', 'error': str(e)}), 500

    return jsonify({'message': 'Worker deleted successfully'})

def register_routes(app):
    """
    Registers the 'workers' Blueprint to the Flask app.
    """
    app.register_blueprint(bp)
