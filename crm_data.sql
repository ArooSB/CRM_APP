-- Create Workers Table for Login
CREATE TABLE workers (
    worker_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,  -- Worker username
    password_hash VARCHAR(255) NOT NULL,   -- Hashed password for security
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(50),  -- Role of the worker (e.g., 'admin', 'support', 'sales')
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Customers Table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    company VARCHAR(100),
    address VARCHAR(225),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Sales Leads Table
CREATE TABLE sales_leads (
    lead_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,  -- Link to customers table
    worker_id INT REFERENCES workers(worker_id) ON DELETE SET NULL,       -- Worker responsible for this lead
    lead_status VARCHAR(50) NOT NULL,
    lead_source VARCHAR(50),
    potential_value DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Unified Interactions Table
CREATE TABLE interactions (
    interaction_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,  -- Link to customers table
    worker_id INT REFERENCES workers(worker_id) ON DELETE SET NULL,       -- Worker involved in the interaction
    interaction_type VARCHAR(50),
    interaction_date TIMESTAMP NOT NULL,
    interaction_notes TEXT,
    communication_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Customer Support Tickets Table
CREATE TABLE support_tickets (
    ticket_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,  -- Link to customers table
    created_by INT REFERENCES workers(worker_id) ON DELETE SET NULL,      -- Worker who created the ticket (i.e., who reported the issue)
    assigned_to INT REFERENCES workers(worker_id) ON DELETE SET NULL,     -- Worker currently assigned to handle the ticket
    ticket_subject VARCHAR(255) NOT NULL,
    ticket_description TEXT,
    ticket_status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Analytics Table
CREATE TABLE analytics (
    analytics_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE CASCADE,  -- Link to customers table
    worker_id INT REFERENCES workers(worker_id) ON DELETE SET NULL,       -- Worker responsible for tracking/handling the analytics
    metric_name VARCHAR(50),
    metric_value DECIMAL(10, 2),
    period_start_date DATE,
    period_end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
