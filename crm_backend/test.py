import os
import pytest
from flask import Flask
from crm_backend.backend_app import create_app, db
from crm_backend.models import Worker

# Configure test environment
os.environ['FLASK_ENV'] = 'testing'
os.environ[
    'DATABASE_URL'] = 'sqlite:///:memory:'  # Use an in-memory database for testing


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()

    # Create the database and the database tables
    with app.app_context():
        db.create_all()

    yield app  # This will return the app to the test

    # Clean up the database after each test
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def auth_token(client):
    """Authenticate and get a JWT token."""
    # Register a worker to authenticate
    client.post('/workers/register', json={
        'username': 'test_user',
        'password': 'password123',
        'role': 'Sales'
    })

    # Login to get the token
    response = client.post('/workers/login', json={
        'username': 'test_user',
        'password': 'password123'
    })
    return response.json['access_token']


def test_create_worker(client, auth_token):
    """Test creating a new worker."""
    response = client.post('/workers/', json={
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'position': 'Sales Manager'
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 201
    assert response.json['message'] == 'Worker created successfully'


def test_create_customer(client, auth_token):
    """Test creating a new customer."""
    # Adjust the route and expected payload as needed
    response = client.post('/customers/', json={
        'first_name': 'James',
        'last_name': 'Bond',
        'email': 'james@example.com',
        'phone': '1234567890',
        'company': 'James Inc.',
        'address': '123 Main St.'
    }, headers={"Authorization": f"Bearer {auth_token}"})

    assert response.status_code == 201
    assert response.json['first_name'] == 'James'


def test_get_workers(client, auth_token):
    """Test getting the list of workers."""
    response = client.get('/workers/',
                          headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    assert isinstance(response.json['workers'], list)  # Ensure it's a list


if __name__ == '__main__':
    pytest.main()
