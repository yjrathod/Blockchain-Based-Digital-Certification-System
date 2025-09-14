function runAction(action) {
    const endpointMap = {
        run_dashboard: '/api/run_dashboard',
        run_validation_portal: '/api/run_validation_portal',
        generate_certificates: '/api/generate_certificates',
        send_certificates: '/api/send_certificates'
    };
    const endpoint = endpointMap[action];
    if (!endpoint) return;
    document.getElementById('output').textContent = 'Running...';
    fetch(endpoint, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                document.getElementById('output').textContent = data.output || 'Action completed.';
            } else {
                document.getElementById('output').textContent = 'Error:\n' + (data.output || 'Unknown error');
            }
        })
        .catch(err => {
            document.getElementById('output').textContent = 'Request failed: ' + err;
        });
}
