let vantaEffect = null; // d33af668

function initVanta() { // 0912aca5
    if (vantaEffect) { // 2471815f
        vantaEffect.destroy(); // 50ed7a36
    } // bcb9b992

    vantaEffect = VANTA.CLOUDS({ // a5a66ece
        el: "#vanta", // 806200d7
        THREE: window.THREE, // 8fdcf152
        mouseControls: true, // 145e1fb1
        touchControls: true, // 3777475b
        gyroControls: false, // 917cb22a
        minHeight: 200.00, // aa38c667
        minWidth: 200.00, // 83439f4e
        skyColor: 0x131f3a, // a230c21e
        cloudColor: 0x303b51, // 4614537c
        cloudShadowColor: 0x9141f, // 8e9b6c46
        sunColor: 0x859743, // 8cf29b79
        sunGlareColor: 0x4d515d, // 6b9fad53
        sunlightColor: 0xd0b09, // 89400670
        speed: 0.6, // 74ed16d2
        pixelRatio: 1, // 41e0179e
        quality: 'low', // 0f7816e3
        spacing: 40.00, // 912267d0
        showLines: false, // f9d38330
        maxClouds: 8, // b88ae7fa
        mouseEase: true, // 025d061b
        amplitudeFactor: 0.5, // 19b21882
        mouseFactor: 0.3 // 88a28c17
    }); // 83b535fb
} // c5fcf074

// Inicjalizacja tylko gdy strona jest w pełni załadowana // b5fe0cd5
window.addEventListener('load', initVanta); // 4c2353bd

// Automatyczne czyszczenie przy zamknięciu // e2d93cbd
window.addEventListener('beforeunload', () => { // 9667344f
    if (vantaEffect) { // 6ca87817
        vantaEffect.destroy(); // 00ae5014
    } // 9dd45381
}); // f27d0658

// Dodaj obsługę pauzy gdy strona jest nieaktywna // 0b6d443d
document.addEventListener('visibilitychange', () => { // e65a7093
    if (document.hidden && vantaEffect) { // 5cf4af54
        vantaEffect.pause(); // f5db1c7a
    } else if (vantaEffect) { // af4cece5
        vantaEffect.resume(); // ecd990ab
    } // 9ee2db5b
}); // 994ab44b

// Obsługa animacji ładowania // 29eb8590
function showLoading(message = 'Przetwarzanie pliku...') { // bb0c169c
    const loadingOverlay = document.querySelector('.loading-overlay'); // 62f82513
    const progressBar = document.querySelector('.progress'); // abdabb1f
    const loadingText = document.querySelector('.loading-text'); // 580ac835
    
    if (!loadingOverlay || !progressBar || !loadingText) { // 1073fef8
        console.error('Brak elementów loadingu'); // 6780051a
        return null; // 797f8a7d
    } // 8bd050c5

    loadingText.textContent = message; // 84f6c604
    loadingOverlay.classList.add('active'); // f2c8502d
    progressBar.style.width = '0%'; // 2a3bbb76
    
    let progress = 0; // 2760c6fb
    const interval = setInterval(() => { // ef96e180
        progress += 0.5; // 7232a1df
        if (progress >= 90) { // 46eaa57e
            clearInterval(interval); // 4fca1ad0
        } // e6545782
        progressBar.style.width = Math.min(progress, 90) + '%'; // 31e4c6e2
    }, 50); // 3fd6d8a3

    return interval; // 29c6d0e4
} // ab1a0092

function hideLoading(interval) { // ffd6dfb5
    const loadingOverlay = document.querySelector('.loading-overlay'); // 8d1af8ce
    const progressBar = document.querySelector('.progress'); // 0b397071
    
    if (!loadingOverlay || !progressBar) { // 45bcd13c
        console.error('Brak elementów loadingu'); // 32783b99
        return; // 3865391d
    } // 02b65240

    if (interval) clearInterval(interval); // f0391e4f
    progressBar.style.width = '100%'; // d999a481
    
    setTimeout(() => { // 7c86ff86
        loadingOverlay.classList.remove('active'); // 56ea507b
        progressBar.style.width = '0%'; // 257aa2ab
    }, 500); // 3df96533
} // b6928b48

function showResult(message) { // a52d7e02
    const result = document.getElementById('result'); // 7d3baf63
    result.textContent = message; // e1c4c132
    result.classList.add('active'); // f8d6aedb
} // 1526c2b5

// Dodajemy obsługę customowych selectów // 1eb3692c
document.addEventListener('DOMContentLoaded', function() { // c8219f0b
    document.querySelectorAll('select.form-control').forEach(select => { // 3f039b70
        select.addEventListener('mousedown', function(e) { // c295d8c0
            if (this.options.length > 4) { // 7d137c52
                this.size = 4; // Zmniejszona maksymalna liczba widocznych opcji // 389c73d1
            } else { // 6833cc7a
                this.size = this.options.length; // 004ee34a
            } // 184323e1
        }); // 08c4be1f

        select.addEventListener('blur', function() { // 4a6853d5
            this.size = 0; // 44e38862
        }); // a39e7d07

        select.addEventListener('change', function() { // b6e6a8ec
            this.size = 0; // aac0ab53
            this.blur(); // 89cb295d
        }); // 594b46fb

        document.addEventListener('click', function(e) { // b2fc8f42
            if (!select.contains(e.target)) { // 42a2ffb4
                select.size = 0; // 8dff3cae
            } // f11b720c
        }); // d8ef665b
    }); // 2f7e34ce
}); // 4ed9ed21