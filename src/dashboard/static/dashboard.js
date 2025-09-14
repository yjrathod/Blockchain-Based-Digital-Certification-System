// Simple JS for dashboard interactivity
function showAlert(msg, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerText = msg;
    document.body.prepend(alertDiv);
    setTimeout(() => alertDiv.remove(), 3000);
}

function previewCSV(input) {
    if (input.files && input.files[0]) {
        showAlert('CSV file selected: ' + input.files[0].name, 'success');
    }
}
