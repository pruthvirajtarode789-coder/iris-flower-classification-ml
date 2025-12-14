document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('iris-form');
    const resultDiv = document.getElementById('result');
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        resultDiv.textContent = 'Predicting...';
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        const response = await fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const res = await response.json();
        resultDiv.textContent = res.result || 'Error occurred.';
    });
});
