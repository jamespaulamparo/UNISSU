// Client-side form validation with real-time feedback
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.novalidate && !validateForm(form)) {
                e.preventDefault();
                return;
            }
        });
        
        // Real-time validation on input
        const inputs = form.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(input);
            });
            
            input.addEventListener('focus', function() {
                clearFieldError(input);
            });
        });
    });
});

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });
    
    return isValid;
}

function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    
    // Check if field is required and empty
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, 'This field is required');
        return false;
    }
    
    // Email validation
    if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, 'Please enter a valid email');
            return false;
        }
    }
    
    // Password strength check (min 8 chars, mix of cases and numbers)
    if (field.name === 'password1' || field.name === 'new_password1') {
        if (value && value.length < 8) {
            showFieldError(field, 'Password must be at least 8 characters');
            return false;
        }
        if (value && !/[a-z]/.test(value) || !/[A-Z]/.test(value) || !/[0-9]/.test(value)) {
            showFieldError(field, 'Password must contain uppercase, lowercase, and numbers');
            return false;
        }
    }
    
    // Password match check
    if (field.name === 'password2' || field.name === 'new_password2') {
        const form = field.closest('form');
        const pwd1Field = form.querySelector('input[name="password1"], input[name="new_password1"]');
        if (pwd1Field && value !== pwd1Field.value) {
            showFieldError(field, 'Passwords do not match');
            return false;
        }
    }
    
    // Clear errors if valid
    clearFieldError(field);
    return true;
}

function showFieldError(field, message) {
    clearFieldError(field);
    field.classList.add('input-error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message field-error';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('input-error');
    const errorDiv = field.parentNode.querySelector('.field-error');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Auto-hide alert messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert, .error-message, .success-message');
    alerts.forEach(alert => {
        if (!alert.classList.contains('field-error')) {
            setTimeout(() => {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 0.3s ease';
                setTimeout(() => alert.remove(), 300);
            }, 5000);
        }
    });
});
