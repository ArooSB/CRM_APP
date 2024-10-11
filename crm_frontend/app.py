from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')

# Dummy user data with hashed passwords
users = {
    'testuser': generate_password_hash('password123'),
    'Aroosha': generate_password_hash('123')
}

# Routes to render HTML pages
@app.route('/')
def index():
    # Redirect to welcome page if logged in
    if 'username' in session:
        return redirect(url_for('welcome'))
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('welcome.html', username=session['username'])

@app.route('/customers')
def customers():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('customers.html')

@app.route('/workers')
def workers():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('workers.html')

@app.route('/sales_leads')
def sales_leads():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('sales_leads.html')

@app.route('/interactions')
def interactions():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('interactions.html')

@app.route('/support_tickets')
def support_tickets():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('support_tickets.html')

@app.route('/analytics')
def analytics():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('analytics.html')

# Login route for authentication
@app.route('/login', methods=['POST'])
def login():
    # Handle JSON request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Simple authentication logic
    if username in users and check_password_hash(users[username], password):
        # Store user information in the session
        session['username'] = username
        print(f"User {username} logged in.")  # Debugging point
        return jsonify({'message': 'Login successful', 'redirect': '/welcome'}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove user from session
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
