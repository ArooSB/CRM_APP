import pytest
from crm_backend.backend_app import create_app, db
from crm_backend.models import *


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()  # Create database tables
        yield app.test_client()  # Provide the test client

        db.session.remove()
        db.drop_all()  # Clean up after tests


# Worker Tests
def test_register_worker(client):
    response = client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Worker registered successfully'


def test_login_worker(client):
    client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    response = client.post('/workers/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json


# Customer Tests
def test_create_customer(client):
    client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    access_token = client.post('/workers/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    }).json['access_token']

    response = client.post('/customers/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'company': 'Example Inc.',
        'address': '123 Example St.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 201
    assert response.json['message'] == 'Customer created successfully'


def test_get_customers(client):
    client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    access_token = client.post('/workers/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    }).json['access_token']

    client.post('/customers/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'company': 'Example Inc.',
        'address': '123 Example St.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    response = client.get('/customers/',
                          headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json['customers']) == 1


# Support Ticket Tests
def test_create_support_ticket(client):
    client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    access_token = client.post('/workers/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    }).json['access_token']

    # Create a customer first
    customer_response = client.post('/customers/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'company': 'Example Inc.',
        'address': '123 Example St.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    customer_id = customer_response.json['id']

    response = client.post('/support_tickets/', json={
        'customer_id': customer_id,
        'description': 'Need help with my order.',
        'status': 'open'
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 201
    assert response.json['message'] == 'Support ticket created successfully'


def test_get_support_tickets(client):
    client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    access_token = client.post('/workers/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    }).json['access_token']

    # Create a customer and a ticket
    customer_response = client.post('/customers/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'company': 'Example Inc.',
        'address': '123 Example St.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    customer_id = customer_response.json['id']

    client.post('/support_tickets/', json={
        'customer_id': customer_id,
        'description': 'Need help with my order.',
        'status': 'open'
    }, headers={'Authorization': f'Bearer {access_token}'})

    response = client.get('/support_tickets/',
                          headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json['tickets']) == 1


# Interaction Tests
def test_create_interaction(client):
    client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    access_token = client.post('/workers/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    }).json['access_token']

    # Create a customer first
    customer_response = client.post('/customers/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'company': 'Example Inc.',
        'address': '123 Example St.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    customer_id = customer_response.json['id']

    response = client.post('/interactions/', json={
        'customer_id': customer_id,
        'notes': 'Discussed the order details.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 201
    assert response.json['message'] == 'Interaction created successfully'


def test_get_interactions(client):
    client.post('/workers/register', json={
        'username': 'testuser',
        'password': 'testpassword',
        'role': 'admin'
    })
    access_token = client.post('/workers/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    }).json['access_token']

    # Create a customer and an interaction
    customer_response = client.post('/customers/', json={
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'phone': '1234567890',
        'company': 'Example Inc.',
        'address': '123 Example St.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    customer_id = customer_response.json['id']

    client.post('/interactions/', json={
        'customer_id': customer_id,
        'notes': 'Discussed the order details.'
    }, headers={'Authorization': f'Bearer {access_token}'})

    response = client.get('/interactions/',
                          headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert len(response.json['interactions']) == 1

