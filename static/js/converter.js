document.addEventListener('DOMContentLoaded', function() {
    // Obsługa kafelków – przełączanie formularzy
    const converterCards = document.querySelectorAll('.converter-card');
    const conversionForms = document.querySelectorAll('.conversion-form');
    const result = document.getElementById('result');
  
    converterCards.forEach(card => {
      card.addEventListener('click', () => {
        converterCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        conversionForms.forEach(form => form.classList.remove('active'));
        const formId = card.dataset.type + "-form";
        const form = document.getElementById(formId);
        if (form) {
          form.classList.add('active');
          form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        if (result) result.classList.remove('active');
      });
    });
  
    // --- Obsługa formularza obrazów ---
    const imageDropZone = document.querySelector('#image-form .drop-zone');
    const imageFileInput = document.getElementById('file-input');
    imageDropZone.addEventListener('click', () => imageFileInput.click());
    ['dragenter','dragover','dragleave','drop'].forEach(evt => {
      imageDropZone.addEventListener(evt, preventDefaults, false);
      document.body.addEventListener(evt, preventDefaults, false);
    });
    ['dragenter','dragover'].forEach(evt => {
      imageDropZone.addEventListener(evt, () => imageDropZone.classList.add('drag-over'), false);
    });
    ['dragleave','drop'].forEach(evt => {
      imageDropZone.addEventListener(evt, () => imageDropZone.classList.remove('drag-over'), false);
    });
    imageDropZone.addEventListener('drop', handleImageDrop, false);
    imageFileInput.addEventListener('change', function() {
      handleImageFiles(this.files);
    });
    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }
    function handleImageDrop(e) {
      const dt = e.dataTransfer;
      handleImageFiles(dt.files);
    }
    function handleImageFiles(files) {
      if (files.length) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
          const reader = new FileReader();
          reader.onloadend = function() {
            showResult('Plik gotowy do konwersji!');
          };
          reader.readAsDataURL(file);
        } else {
          showResult('Błąd: Wybierz plik obrazu');
        }
      }
    }
    document.querySelector('#image-form .btn-convert').addEventListener('click', function(e) {
      e.preventDefault();
      if (!imageFileInput.files.length) {
        showResult('Proszę najpierw wybrać plik');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = function() {
        const progressInterval = showLoading('Konwertowanie obrazu...');
        fetch('/convert-image', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            image: reader.result,
            format: document.getElementById('img-format').value
          })
        })
        .then(res => res.json())
        .then(data => {
          hideLoading(progressInterval);
          if (data.success) {
            window.open(data.download_url, '_blank');
            showResult('Konwersja zakończona pomyślnie!');
          } else {
            showResult('Błąd: ' + (data.error || 'Wystąpił błąd'));
          }
        })
        .catch(err => {
          hideLoading(progressInterval);
          showResult('Wystąpił błąd: ' + err.message);
        });
      };
      reader.readAsDataURL(imageFileInput.files[0]);
    });
  
    // --- Obsługa formularza linków ---
    document.querySelector('#link-form .btn-convert').addEventListener('click', function(e) {
      e.preventDefault();
      const progressInterval = showLoading('Pobieranie zawartości...');
      fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: document.getElementById('url').value,
          platform: document.getElementById('platform').value,
          'file-type': document.getElementById('format').value === 'mp3' ? 'audio' : 'video',
          format: document.getElementById('format').value,
          quality: document.getElementById('quality').value
        })
      })
      .then(res => res.json())
      .then(data => {
        hideLoading(progressInterval);
        if (data.download_url) {
          window.open(data.download_url, '_blank');
        }
        showResult(data.message || 'Pobrano pomyślnie!');
      })
      .catch(err => {
        hideLoading(progressInterval);
        showResult('Wystąpił błąd: ' + err.message);
      });
    });
  
    // --- Obsługa formularza szyfrowania ---
    const operationType = document.getElementById('operation-type');
    const keyLabel = document.getElementById('key-label');
    const generateKeyBtn = document.getElementById('generate-key');
    const copyKeyBtn = document.getElementById('copy-key');
    const inputMethodSelect = document.getElementById('input-method');
    const fileInputSection = document.getElementById('file-input-section');
    const textInputSection = document.getElementById('text-input-section');
  
    operationType.addEventListener('change', function() {
      if (this.value === 'encrypt') {
        keyLabel.textContent = 'Utwórz klucz szyfrowania';
        generateKeyBtn.style.display = 'inline-block';
      } else {
        keyLabel.textContent = 'Podaj klucz deszyfrujący';
        generateKeyBtn.style.display = 'none';
      }
    });
    generateKeyBtn.addEventListener('click', function() {
      document.getElementById('encryption-key').value = generateRandomKey(32);
    });
    function generateRandomKey(length) {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let res = '';
      for (let i = 0; i < length; i++) {
        res += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return res;
    }
    copyKeyBtn.addEventListener('click', function() {
      const keyValue = document.getElementById('encryption-key').value;
      navigator.clipboard.writeText(keyValue).then(() => {
        copyKeyBtn.classList.add('copied');
        const originalHTML = copyKeyBtn.innerHTML;
        copyKeyBtn.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
          copyKeyBtn.classList.remove('copied');
          copyKeyBtn.innerHTML = originalHTML;
        }, 2000);
      });
    });
    inputMethodSelect.addEventListener('change', function() {
      if (this.value === 'file') {
        fileInputSection.style.display = 'block';
        textInputSection.style.display = 'none';
      } else {
        fileInputSection.style.display = 'none';
        textInputSection.style.display = 'block';
      }
    });
    // Obsługa wyboru pliku z kodem
    const codeFileInput = document.getElementById('code-file-input');
    fileInputSection.addEventListener('click', () => codeFileInput.click());
    fileInputSection.addEventListener('dragover', preventDefaults, false);
    fileInputSection.addEventListener('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
      const file = e.dataTransfer.files[0];
      if (isValidCodeFile(file)) {
        handleCodeFile(file);
      } else {
        showResult('Nieprawidłowy typ pliku. Dozwolone rozszerzenia: .js, .cpp, .h, .hpp');
      }
      this.classList.remove('drag-over');
    });
    function isValidCodeFile(file) {
      const validExts = ['.js', '.cpp', '.h', '.hpp'];
      return validExts.some(ext => file.name.toLowerCase().endsWith(ext));
    }
    function handleCodeFile(file) {
      const reader = new FileReader();
      reader.onload = function(e) {
        document.getElementById('code-text-input').value = e.target.result;
        showResult('Plik wczytany pomyślnie!');
      };
      reader.readAsText(file);
    }
    // Obsługa przycisku szyfrowania/deszyfrowania
    document.querySelector('#encryption-form .btn-convert').addEventListener('click', function(e) {
      e.preventDefault();
      const operation = operationType.value;
      const language = document.getElementById('programming-language').value;
      const key = document.getElementById('encryption-key').value.trim();
      let code = "";
      if (inputMethodSelect.value === 'file') {
        if (!codeFileInput.files.length) {
          showResult('Wybierz plik z kodem');
          return;
        }
        const formData = new FormData();
        formData.append('file', codeFileInput.files[0]);
        formData.append('language', language);
        formData.append('key', key);
        const progressInterval = showLoading(operation === 'encrypt' ? 'Szyfrowanie pliku...' : 'Deszyfrowanie pliku...');
        fetch('/encrypt-file', { method: 'POST', body: formData })
        .then(res => res.json())
        .then(data => {
          hideLoading(progressInterval);
          if (data.download_url) {
            window.open(data.download_url, '_blank');
            showResult('Operacja zakończona pomyślnie!');
          } else {
            showResult('Błąd: ' + (data.error || 'Wystąpił błąd'));
          }
        })
        .catch(err => {
          hideLoading(progressInterval);
          showResult('Wystąpił błąd: ' + err.message);
        });
      } else {
        code = document.getElementById('code-text-input').value.trim();
        if (!code) {
          showResult('Wprowadź kod do przetworzenia');
          return;
        }
        if (!key) {
          showResult('Wprowadź klucz');
          return;
        }
        const progressInterval = showLoading(operation === 'encrypt' ? 'Szyfrowanie kodu...' : 'Deszyfrowanie kodu...');
        fetch('/process-code', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ operation, language, key, code })
        })
        .then(res => res.json())
        .then(data => {
          hideLoading(progressInterval);
          if (data.success) {
            document.getElementById('code-text-input').value = data.result;
            showResult('Operacja zakończona pomyślnie!');
          } else {
            showResult('Błąd: ' + data.error);
          }
        })
        .catch(err => {
          hideLoading(progressInterval);
          showResult('Wystąpił błąd: ' + err.message);
        });
      }
    });
    
    // Funkcje ładowania/ukrywania overlay
    function showLoading(message = 'Przetwarzanie pliku...') {
      const overlay = document.querySelector('.loading-overlay');
      const progressBar = document.querySelector('.progress');
      const loadingText = document.querySelector('.loading-text');
      if (!overlay || !progressBar || !loadingText) {
        console.error('Brak elementów loadingu');
        return null;
      }
      loadingText.textContent = message;
      overlay.classList.add('active');
      progressBar.style.width = '0%';
      let progress = 0;
      const interval = setInterval(() => {
        progress += 0.5;
        if (progress >= 90) clearInterval(interval);
        progressBar.style.width = Math.min(progress, 90) + '%';
      }, 50);
      return interval;
    }
    function hideLoading(interval) {
      const overlay = document.querySelector('.loading-overlay');
      const progressBar = document.querySelector('.progress');
      if (!overlay || !progressBar) {
        console.error('Brak elementów loadingu');
        return;
      }
      if (interval) clearInterval(interval);
      progressBar.style.width = '100%';
      setTimeout(() => {
        overlay.classList.remove('active');
        progressBar.style.width = '0%';
      }, 500);
    }
    function showResult(message) {
      const res = document.getElementById('result');
      res.textContent = message;
      res.classList.add('active');
    }
  });
  