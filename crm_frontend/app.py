from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Set a secret key for the application (could be loaded from environment variables)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Dummy user data with hashed passwords for demonstration
users = {
    'testuser': generate_password_hash('password123'),
    'Aroosha': generate_password_hash('123')
}

# Routes to render HTML pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/workers')
def workers():
    return render_template('workers.html')

@app.route('/sales_leads')
def sales_leads():
    return render_template('sales_leads.html')

@app.route('/interactions')
def interactions():
    return render_template('interactions.html')

@app.route('/support_tickets')
def support_tickets():
    return render_template('support_tickets.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

# Login route for authentication
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Simple authentication logic
    if username in users and check_password_hash(users[username], password):
        # Generate a token here using JWT if applicable
        return jsonify({'token': 'dummy_token', 'username': username}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5001)
