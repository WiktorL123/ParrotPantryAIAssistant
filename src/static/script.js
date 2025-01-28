const modeSelector = document.getElementById('mode-selector');
const textForm = document.getElementById('textForm');
const photoForm = document.getElementById('photoForm');
const responseDiv = document.getElementById('response');
const loadingDiv = document.getElementById('loading');

// Przełączanie między trybami
modeSelector.addEventListener('change', (e) => {
    const mode = document.querySelector('input[name="mode"]:checked').value;
    if (mode === 'text') {
        textForm.style.display = 'block';
        photoForm.style.display = 'none';
    } else {
        textForm.style.display = 'none';
        photoForm.style.display = 'block';
    }
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
