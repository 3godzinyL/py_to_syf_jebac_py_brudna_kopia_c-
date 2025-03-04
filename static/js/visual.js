let vantaEffect = null;

function initVanta() {
    if (vantaEffect) {
        vantaEffect.destroy();
    }

    vantaEffect = VANTA.CLOUDS({
        el: "#vanta",
        THREE: window.THREE,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        skyColor: 0x131f3a,
        cloudColor: 0x303b51,
        cloudShadowColor: 0x9141f,
        sunColor: 0x859743,
        sunGlareColor: 0x4d515d,
        sunlightColor: 0xd0b09,
        speed: 0.6,
        pixelRatio: 1,
        quality: 'low',
        spacing: 40.00,
        showLines: false,
        maxClouds: 8,
        mouseEase: true,
        amplitudeFactor: 0.5,
        mouseFactor: 0.3
    });
}

// Inicjalizacja tylko gdy strona jest w pełni załadowana
window.addEventListener('load', initVanta);

// Automatyczne czyszczenie przy zamknięciu
window.addEventListener('beforeunload', () => {
    if (vantaEffect) {
        vantaEffect.destroy();
    }
});

// Dodaj obsługę pauzy gdy strona jest nieaktywna
document.addEventListener('visibilitychange', () => {
    if (document.hidden && vantaEffect) {
        vantaEffect.pause();
    } else if (vantaEffect) {
        vantaEffect.resume();
    }
});

// Obsługa animacji ładowania
const loadingOverlay = document.querySelector('.loading-overlay');
const progressBar = document.querySelector('.progress');
const loadingText = document.querySelector('.loading-text');

function showLoading(message = 'Przetwarzanie pliku...') {
    loadingText.textContent = message;
    loadingOverlay.classList.add('active');
    progressBar.style.width = '0%';
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += 0.5;
        if (progress >= 90) {
            clearInterval(interval);
        }
        progressBar.style.width = Math.min(progress, 90) + '%';
    }, 50);

    return interval;
}

function hideLoading(interval) {
    if (interval) clearInterval(interval);
    progressBar.style.width = '100%';
    
    setTimeout(() => {
        loadingOverlay.classList.remove('active');
        progressBar.style.width = '0%';
    }, 500);
}

function showResult(message) {
    const result = document.getElementById('result');
    result.textContent = message;
    result.classList.add('active');
}

// Dodajemy obsługę customowych selectów
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('select.form-control').forEach(select => {
        select.addEventListener('mousedown', function(e) {
            if (this.options.length > 4) {
                this.size = 4; // Zmniejszona maksymalna liczba widocznych opcji
            } else {
                this.size = this.options.length;
            }
        });

        select.addEventListener('blur', function() {
            this.size = 0;
        });

        select.addEventListener('change', function() {
            this.size = 0;
            this.blur();
        });

        document.addEventListener('click', function(e) {
            if (!select.contains(e.target)) {
                select.size = 0;
            }
        });
    });
}); 