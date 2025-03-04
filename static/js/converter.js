document.addEventListener('DOMContentLoaded', function() {
    // Obsługa kart konwertera
    const converterCards = document.querySelectorAll('.converter-card');
    const imageForms = document.getElementById('image-form');
    const linkForm = document.getElementById('link-form');
    const result = document.getElementById('result');

    converterCards.forEach(card => {
        card.addEventListener('click', () => {
            converterCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');

            if (card.dataset.type === 'image') {
                imageForms.classList.add('active');
                linkForm.classList.remove('active');
            } else {
                linkForm.classList.add('active');
                imageForms.classList.remove('active');
            }
            result.classList.remove('active');
        });
    });

    // Obsługa przeciągania i upuszczania
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.getElementById('file-input');

    dropZone.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight(e) {
        dropZone.classList.add('drag-over');
    }

    function unhighlight(e) {
        dropZone.classList.remove('drag-over');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    fileInput.addEventListener('change', function(e) {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length) {
            const file = files[0];
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onloadend = function() {
                    showResult('Plik gotowy do konwersji!');
                };
            } else {
                showResult('Błąd: Wybierz plik obrazu');
            }
        }
    }

    // Funkcja konwersji obrazu
    function convertImage(imageData) {
        const format = document.getElementById('img-format').value;
        const progressInterval = showLoading('Konwertowanie obrazu...');
        
        fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: imageData,
                'file-type': 'image',
                format: format
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.download_url) {
                showLoading('Pobieranie pliku...');
                setTimeout(() => {
                    hideLoading(progressInterval);
                    window.location.href = data.download_url;
                    showResult('Konwersja zakończona pomyślnie!');
                }, 1000);
            } else {
                hideLoading(progressInterval);
                showResult(data.error || 'Wystąpił błąd podczas konwersji');
            }
        })
        .catch(error => {
            hideLoading(progressInterval);
            showResult('Wystąpił błąd: ' + error.message);
        });
    }

    // Obsługa formularza linków
    document.getElementById('link-form').querySelector('.btn-convert').addEventListener('click', function(e) {
        e.preventDefault();
        const url = document.getElementById('url').value;
        const platform = document.getElementById('platform').value;
        const format = document.getElementById('format').value;
        const quality = document.getElementById('quality').value;

        showLoading('Pobieranie zawartości...');

        fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: url,
                platform: platform,
                'file-type': format === 'mp3' ? 'audio' : 'video',
                format: format,
                quality: quality
            })
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            if (data.download_url) {
                window.location.href = data.download_url;
            }
            showResult(data.message);
        })
        .catch(error => {
            hideLoading();
            showResult('Wystąpił błąd: ' + error.message);
        });
    });

    // Dynamiczna zmiana opcji formatu
    document.getElementById('platform').addEventListener('change', function() {
        const format = document.getElementById('format');
        const qualityGroup = document.getElementById('quality-group');
        
        if (this.value === 'youtube') {
            format.innerHTML = `
                <option value="mp4">MP4</option>
                <option value="mp3">MP3</option>
            `;
            qualityGroup.style.display = 'block';
        } else {
            format.innerHTML = `
                <option value="mp4">MP4</option>
            `;
            qualityGroup.style.display = 'none';
        }
    });

    // Obsługa przycisku konwertuj dla obrazów
    document.getElementById('image-form').querySelector('.btn-convert').addEventListener('click', function(e) {
        e.preventDefault();
        const fileInput = document.getElementById('file-input');
        if (fileInput.files.length > 0) {
            const reader = new FileReader();
            reader.readAsDataURL(fileInput.files[0]);
            reader.onloadend = function() {
                convertImage(reader.result);
            };
        } else {
            showResult('Proszę najpierw wybrać plik');
        }
    });
}); 