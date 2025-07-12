// Main JavaScript file for Employee Management System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Auto-hide alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Confirm form submission for delete actions
    const deleteButtons = document.querySelectorAll('.btn-danger[type="submit"]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this employee? This action cannot be undone.')) {
                event.preventDefault();
            }
        });
    });
    
    // Search form auto-submit on filter change
    const searchForm = document.querySelector('form[method="GET"]');
    if (searchForm) {
        const filterInputs = searchForm.querySelectorAll('select, input[type="number"]');
        filterInputs.forEach(function(input) {
            input.addEventListener('change', function() {
                searchForm.submit();
            });
        });
    }
    
    // Loading states for forms
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const form = button.closest('form');
            if (form && form.checkValidity()) {
                button.disabled = true;
                button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processing...';
                
                // Re-enable after 5 seconds as fallback
                setTimeout(function() {
                    button.disabled = false;
                    button.innerHTML = button.getAttribute('data-original-text') || 'Submit';
                }, 5000);
            }
        });
    });
    
    // Store original button text
    submitButtons.forEach(function(button) {
        button.setAttribute('data-original-text', button.innerHTML);
    });
    
    // Salary input formatting
    const salaryInputs = document.querySelectorAll('input[name="salary"]');
    salaryInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            const value = parseFloat(this.value);
            if (!isNaN(value)) {
                this.value = value.toFixed(2);
            }
        });
    });
    
    // Department input autocomplete
    const departmentInputs = document.querySelectorAll('input[name="department"]');
    departmentInputs.forEach(function(input) {
        const commonDepartments = ['IT', 'HR', 'Sales', 'Marketing', 'Finance', 'Operations', 'Support'];
        
        input.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            const suggestions = commonDepartments.filter(dept => 
                dept.toLowerCase().startsWith(value)
            );
            
            // Simple autocomplete implementation
            if (suggestions.length > 0 && value.length > 0) {
                this.setAttribute('placeholder', suggestions[0]);
            }
        });
    });
    
    // Role input autocomplete
    const roleInputs = document.querySelectorAll('input[name="role"]');
    roleInputs.forEach(function(input) {
        const commonRoles = ['Manager', 'Developer', 'Analyst', 'Designer', 'Coordinator', 'Specialist', 'Executive'];
        
        input.addEventListener('input', function() {
            const value = this.value.toLowerCase();
            const suggestions = commonRoles.filter(role => 
                role.toLowerCase().startsWith(value)
            );
            
            if (suggestions.length > 0 && value.length > 0) {
                this.setAttribute('placeholder', suggestions[0]);
            }
        });
    });
    
    // Table row click to view details
    const tableRows = document.querySelectorAll('tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function(event) {
            // Don't trigger on button clicks
            if (event.target.tagName === 'BUTTON' || event.target.closest('button')) {
                return;
            }
            
            const editButton = row.querySelector('.btn-outline-primary');
            if (editButton) {
                window.location.href = editButton.getAttribute('href');
            }
        });
        
        // Add hover cursor
        row.style.cursor = 'pointer';
    });
    
    // Export functionality feedback
    const exportButtons = document.querySelectorAll('a[href*="export"]');
    exportButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Exporting...';
            
            setTimeout(() => {
                this.innerHTML = originalText;
                
                // Show success message
                const alert = document.createElement('div');
                alert.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 end-0 m-3';
                alert.style.zIndex = '1055';
                alert.innerHTML = `
                    <i class="fas fa-check-circle me-2"></i>Export completed successfully!
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                document.body.appendChild(alert);
                
                // Auto-remove after 3 seconds
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 3000);
            }, 1000);
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // Ctrl+N for new employee
        if (event.ctrlKey && event.key === 'n') {
            event.preventDefault();
            const addButton = document.querySelector('a[href*="add_employee"]');
            if (addButton) {
                window.location.href = addButton.getAttribute('href');
            }
        }
        
        // Ctrl+S for save (on forms)
        if (event.ctrlKey && event.key === 's') {
            event.preventDefault();
            const submitButton = document.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.click();
            }
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(function(modal) {
                bootstrap.Modal.getInstance(modal).hide();
            });
        }
    });
    
    // Print functionality
    const printButton = document.querySelector('.btn-print');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Dashboard charts (if Chart.js is available)
    if (typeof Chart !== 'undefined') {
        initializeDashboardCharts();
    }
});

// Dashboard charts initialization
function initializeDashboardCharts() {
    // Department distribution chart
    const deptChartCanvas = document.getElementById('departmentChart');
    if (deptChartCanvas) {
        const ctx = deptChartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: window.chartData.departments.map(d => d.name),
                datasets: [{
                    data: window.chartData.departments.map(d => d.count),
                    backgroundColor: [
                        '#0d6efd',
                        '#198754',
                        '#ffc107',
                        '#dc3545',
                        '#6f42c1',
                        '#fd7e14'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Salary distribution chart
    const salaryChartCanvas = document.getElementById('salaryChart');
    if (salaryChartCanvas) {
        const ctx = salaryChartCanvas.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: window.chartData.salaryRanges.map(r => r.range),
                datasets: [{
                    label: 'Number of Employees',
                    data: window.chartData.salaryRanges.map(r => r.count),
                    backgroundColor: '#0d6efd'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

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

// Global error handler
window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    
    // Show user-friendly error message
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show position-fixed top-0 end-0 m-3';
    alert.style.zIndex = '1055';
    alert.innerHTML = `
        <i class="fas fa-exclamation-triangle me-2"></i>An error occurred. Please try again.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alert);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.parentNode.removeChild(alert);
        }
    }, 5000);
});
