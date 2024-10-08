from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Dummy user data for demonstration
users = {'testuser': 'password123','Aroosha': '123'}

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
    print(data)
    username = data.get('username')
    password = data.get('password')

    # Simple authentication logic
    if username in users and users[username] == password:
        return jsonify({'token': 'dummy_token', 'username': username}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5001)
