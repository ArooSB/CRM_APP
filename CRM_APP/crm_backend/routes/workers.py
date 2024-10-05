from flask import Blueprint, request, jsonify
from crm_backend import db
from crm_backend.models import Worker
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('workers', __name__, url_prefix='/workers')

# Register Worker
@bp.route('/register', methods=['POST'])
def register_worker():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if Worker.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    worker = Worker(username=username, role=role)
    worker.set_password(password)
    db.session.add(worker)
    db.session.commit()

    return jsonify({'message': 'Worker registered successfully'}), 201

# Login Worker
@bp.route('/login', methods=['POST'])
def login_worker():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    worker = Worker.query.filter_by(username=username).first()
    if worker and worker.check_password(password):
        access_token = create_access_token(identity=worker.id)
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# Logout Worker (JWT token is handled in frontend by removing token)
@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_worker():
    return jsonify({'message': 'Logged out'}), 200

# CRUD for Workers
@bp.route('/', methods=['GET'])
@jwt_required()
def get_workers():
    workers = Worker.query.all()
    return jsonify([worker.username for worker in workers])

@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_worker(id):
    worker = Worker.query.get_or_404(id)
    db.session.delete(worker)
    db.session.commit()
    return jsonify({'message': 'Worker deleted successfully'})
