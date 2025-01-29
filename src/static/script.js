const modeButtons = document.querySelectorAll('.mode-btn');
const textForm = document.getElementById('textForm');
const photoForm = document.getElementById('photoForm');
const vetForm = document.getElementById('vetForm');
const responseDiv = document.getElementById('response');
const loadingDiv = document.getElementById('loading');


responseDiv.style.display = 'none';

modeButtons.forEach(button => {
    button.addEventListener('click', () => {
        modeButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        const mode = button.getAttribute('data-mode');


        switch (mode){
            case 'text': {
                textForm.style.display='block'
                vetForm.style.display='none'
                photoForm.style.display='none'
                break
            }
            case 'photos': {
                photoForm.style.display='flex'
                photoForm.style.flexDirection='column'
                photoForm.style.alignItems='center'
                textForm.style.display='none'
                vetForm.style.display='none'
                break
            }
            case 'vet': {
                vetForm.style.display='block'
                photoForm.style.display='none'
                textForm.style.display='none'
                break
            }
            default: {
                alert('nie dziala')
            }
        }


        responseDiv.style.display = 'none';
        responseDiv.innerHTML = '';
    });
});

async function fetchData(url, requestData) {
    loadingDiv.style.display = 'block';
    responseDiv.style.display = 'none';
    responseDiv.innerHTML = '';

    try {
        const response = await fetch(url, requestData);
        const data = await response.json();
        loadingDiv.style.display = 'none';

        if (data.image_url) {
            responseDiv.innerHTML = `<img src="${data.image_url}" alt="Generated Image" class="generated-image">`;
        } else if (data.advice) {
            responseDiv.innerHTML = `<h2>Advice:</h2><p>${data.advice}</p>`;
        } else {
            responseDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }

        responseDiv.style.display = 'block';

    } catch (error) {
        loadingDiv.style.display = 'none';
        responseDiv.innerHTML = `<p class="error">An error occurred. Please try again.</p>`;
        responseDiv.style.display = 'block';
    }
}

textForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('prompt').value;

    await fetchData('/generate-image-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    });
});

photoForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const photo1 = document.getElementById('photo1').files[0];
    const photo2 = document.getElementById('photo2').files[0];

    if (!photo1 || !photo2) {
        responseDiv.innerHTML = `<p class="error">Both photos are required!</p>`;
        responseDiv.style.display = 'block';
        return;
    }

    formData.append("photo1", photo1);
    formData.append("photo2", photo2);

    await fetchData('/generate-image-photos', {
        method: 'POST',
        body: formData
    });
});


vetForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const problem = document.getElementById('problem').value;

    await fetchData('/vet-assistant', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem })
    });
});
