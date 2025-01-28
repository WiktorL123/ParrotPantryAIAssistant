const form = document.getElementById('promptForm');
const responseDiv = document.getElementById('response');
const loadingDiv = document.getElementById('loading');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('prompt').value;

    // Wyświetl spinner ładowania
    loadingDiv.style.display = 'block';
    responseDiv.innerHTML = '';

    try {
        // Wysłanie żądania POST do backendu
        const response = await fetch('/generate-image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();

        // Ukryj spinner ładowania
        loadingDiv.style.display = 'none';

        if (data.image_url) {
            // Wyświetl obraz
            responseDiv.innerHTML = `<img src="${data.image_url}" alt="Generated Parrot" />`;
        } else {
            // Wyświetl błąd
            responseDiv.innerHTML = `<p><strong>Error:</strong> ${data.error}</p>`;
        }
    } catch (error) {
        // Ukryj spinner i pokaż błąd
        loadingDiv.style.display = 'none';
        responseDiv.innerHTML = `<p><strong>Error:</strong> Something went wrong!</p>`;
    }
});
