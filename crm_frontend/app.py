from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
