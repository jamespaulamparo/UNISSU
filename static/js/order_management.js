
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Basic form validation could go here
            const customerName = this.querySelector('[name="customer_name"]').value;
            if (!customerName) {
                event.preventDefault();
                alert('Customer Name is required!');
            }
            // Optional: Add more validations as needed
            alert('Order submitted successfully!');
        });
    });
});
