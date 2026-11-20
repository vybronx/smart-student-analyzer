// Smart Student Analyzer - Main JavaScript Helper

document.addEventListener('DOMContentLoaded', function () {
    // Enable Bootstrap tooltips if any
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

function confirmDelete(name) {
    return confirm(`Are you sure you want to delete "${name}"? This action cannot be undone.`);
}

function printReport() {
    window.print();
}
