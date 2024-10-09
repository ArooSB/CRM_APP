document.addEventListener('DOMContentLoaded', function () {
    // Search functionality for customers
    const searchButton = document.getElementById('search-button');
    const searchInput = document.getElementById('search');
    if (searchButton) {
        searchButton.addEventListener('click', function () {
            const query = searchInput.value;
            // API call placeholder for searching customers
            alert(`Searching for customers with name or email containing "${query}"`);
            // Add your search logic here...
        });
    }

    // Create customer
    const createCustomerButton = document.getElementById('create-customer');
    if (createCustomerButton) {
        createCustomerButton.addEventListener('click', function () {
            const customer = {
                firstName: document.getElementById('first-name').value,
                lastName: document.getElementById('last-name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                company: document.getElementById('company').value,
                address: document.getElementById('address').value
            };
            // Placeholder for API call to create a customer
            alert('Customer created: ' + JSON.stringify(customer));
            // Add your API call here...
        });
    }

    // Create sales lead
    const createLeadButton = document.getElementById('create-lead');
    if (createLeadButton) {
        createLeadButton.addEventListener('click', function () {
            const lead = {
                customerId: document.getElementById('customer-id').value,
                status: document.getElementById('lead-status').value
            };
            // Placeholder for API call to create a sales lead
            alert('Sales Lead created: ' + JSON.stringify(lead));
            // Add your API call here...
        });
    }

    // Log interaction
    const logInteractionButton = document.getElementById('log-interaction');
    if (logInteractionButton) {
        logInteractionButton.addEventListener('click', function () {
            const interaction = {
                customerId: document.getElementById('customer-id').value,
                notes: document.getElementById('interaction-notes').value
            };
            // Placeholder for API call to log interaction
            alert('Interaction logged: ' + JSON.stringify(interaction));
            // Add your API call here...
        });
    }

    // Create support ticket
    const createTicketButton = document.getElementById('create-ticket');
    if (createTicketButton) {
        createTicketButton.addEventListener('click', function () {
            const ticket = {
                customerId: document.getElementById('customer-id').value,
                description: document.getElementById('ticket-description').value,
                status: document.getElementById('ticket-status').value
            };
            // Placeholder for API call to create support ticket
            alert('Support ticket created: ' + JSON.stringify(ticket));
            // Add your API call here...
        });
    }

    // Create worker
    const createWorkerButton = document.getElementById('create-worker');
    if (createWorkerButton) {
        createWorkerButton.addEventListener('click', function () {
            const worker = {
                name: document.getElementById('worker-name').value,
                email: document.getElementById('worker-email').value,
                position: document.getElementById('worker-position').value
            };
            // Placeholder for API call to add worker
            alert('Worker added: ' + JSON.stringify(worker));
            // Add your API call here...
        });
    }
});
