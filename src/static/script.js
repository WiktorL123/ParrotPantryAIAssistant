const modeSelector = document.getElementById('mode-selector');
const textForm = document.getElementById('textForm');
const photoForm = document.getElementById('photoForm');
const vetForm = document.getElementById('vetForm');
const responseDiv = document.getElementById('response');
const loadingDiv = document.getElementById('loading');

// Przełączanie między trybami
modeSelector.addEventListener('change', () => {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    textForm.style.display = mode === 'text' ? 'block' : 'none';
    photoForm.style.display = mode === 'photos' ? 'block' : 'none';
    vetForm.style.display = mode === 'vet' ? 'block' : 'none';
});

// Obsługa formularza tekstowego
textForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('prompt').value;

    loadingDiv.style.display = 'block';
    responseDiv.innerHTML = '';

    const response = await fetch('/generate-image-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });

    const data = await response.json();
    loadingDiv.style.display = 'none';
    responseDiv.innerHTML = data.image_url
        ? `<img src="${data.image_url}" alt="Generated Parrot">`
        : `<p>Error: ${data.error}</p>`;
});

// Obsługa formularza przesyłania zdjęć
photoForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(photoForm);
    loadingDiv.style.display = 'block';
    responseDiv.innerHTML = '';

    const response = await fetch('/generate-image-photos', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    loadingDiv.style.display = 'none';
    responseDiv.innerHTML = data.image_url
        ? `<img src="${data.image_url}" alt="Generated Parrot">`
        : `<p>Error: ${data.error}</p>`;
});

// Obsługa formularza Vet Assistant
vetForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const problem = document.getElementById('problem').value;

    loadingDiv.style.display = 'block';
    responseDiv.innerHTML = '';

    const response = await fetch('/vet-assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem })
    });

    const data = await response.json();
    loadingDiv.style.display = 'none';
    responseDiv.innerHTML = data.advice
        ? `<h2>Advice:</h2><div>${data.advice}</div>`
        : `<p>Error: ${data.error}</p>`;
});
