// JavaScript for Employee Management System

// Initialize dashboard charts if Chart.js is available
function initializeDashboardCharts() {
    // This would be used if we add Chart.js for data visualization
    console.log('Dashboard charts initialized');
}

// Format currency display
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// Format date display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-dismiss flash messages
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Enhanced search functionality
    const searchInput = document.getElementById('search');
    if (searchInput) {
        const debouncedSearch = debounce(() => {
            // Auto-submit search form after typing stops
            const form = searchInput.closest('form');
            if (form) {
                form.submit();
            }
        }, 1000);
        
        searchInput.addEventListener('input', debouncedSearch);
    }
    
    // Salary range validation
    const minSalary = document.getElementById('min_salary');
    const maxSalary = document.getElementById('max_salary');
    
    if (minSalary && maxSalary) {
        function validateSalaryRange() {
            const min = parseFloat(minSalary.value) || 0;
            const max = parseFloat(maxSalary.value) || Infinity;
            
            if (min > max) {
                maxSalary.setCustomValidity('Maximum salary must be greater than minimum salary');
            } else {
                maxSalary.setCustomValidity('');
            }
        }
        
        minSalary.addEventListener('input', validateSalaryRange);
        maxSalary.addEventListener('input', validateSalaryRange);
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize dashboard charts
    initializeDashboardCharts();
});

// Loading state management
function showLoading(element) {
    element.classList.add('loading');
    element.style.pointerEvents = 'none';
}

function hideLoading(element) {
    element.classList.remove('loading');
    element.style.pointerEvents = 'auto';
}

// Confirmation dialogs
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Print functionality
function printReport() {
    window.print();
}

// Export functionality
function exportData(format) {
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('format', format);
    window.location.href = currentUrl.toString();
}

// Auto-refresh for dashboard (optional)
function autoRefreshDashboard() {
    if (window.location.pathname === '/') {
        setTimeout(() => {
            location.reload();
        }, 300000); // Refresh every 5 minutes
    }
}

// Initialize auto-refresh
// autoRefreshDashboard();

console.log('Employee Management System JavaScript loaded successfully');