// Amazon Task Manager JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Task form validation
    const taskForm = document.querySelector('form');
    if (taskForm) {
        taskForm.addEventListener('submit', function(event) {
            const titleInput = document.getElementById('title');
            if (titleInput && titleInput.value.trim() === '') {
                event.preventDefault();
                titleInput.classList.add('is-invalid');
                
                // Create error message
                const errorDiv = document.createElement('div');
                errorDiv.className = 'text-danger';
                errorDiv.textContent = 'Title is required';
                
                // Insert error message after the input
                titleInput.parentNode.appendChild(errorDiv);
            }
        });
    }

    // Task status update
    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        select.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const newStatus = this.value;
            
            // Show loading spinner
            const loadingSpinner = document.getElementById(`loading-${taskId}`);
            if (loadingSpinner) {
                loadingSpinner.classList.remove('d-none');
            }
            
            // In a real app, you would send an AJAX request to update the task status
            // For demo purposes, we'll just reload the page after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 500);
        });
    });

    // Task filter
    const filterSelect = document.getElementById('filter-status');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            const status = this.value;
            const taskRows = document.querySelectorAll('tr[data-status]');
            
            taskRows.forEach(row => {
                if (status === 'all' || row.dataset.status === status) {
                    row.classList.remove('d-none');
                } else {
                    row.classList.add('d-none');
                }
            });
        });
    }

    // Error handling for API requests
    function handleApiError(error) {
        console.error('API Error:', error);
        const errorContainer = document.getElementById('error-container');
        if (errorContainer) {
            errorContainer.textContent = 'An error occurred. Please try again later.';
            errorContainer.classList.remove('d-none');
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                errorContainer.classList.add('d-none');
            }, 5000);
        }
    }
});