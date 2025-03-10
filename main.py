import os
import base64
import uuid
import time
import json
import subprocess
from threading import Thread
from flask import Flask, render_template, request, jsonify, send_file, url_for
from yt_dlp import YoutubeDL
from PIL import Image

app = Flask(__name__, static_folder='static', template_folder='templates')

# Katalogi do przechowywania plików
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
TEMP_FOLDER = 'temp'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER, TEMP_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Funkcja czyszcząca stare pliki (starsze niż 1 godzina)
def cleanup_old_files():
    current_time = time.time()
    for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER, TEMP_FOLDER]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) and os.path.getmtime(file_path) < current_time - 3600:
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")

def cleanup_thread():
    while True:
        cleanup_old_files()
        time.sleep(3600)

Thread(target=cleanup_thread, daemon=True).start()

# -----------------------------------------------
# Funkcja konwersji obrazów (przykładowa)
# -----------------------------------------------
def handle_image_conversion(image_data, target_format):
    try:
        temp_filename = f"{uuid.uuid4()}_temp.png"
        output_filename = f"{uuid.uuid4()}.{target_format.lower()}"
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        output_path = os.path.join(CONVERTED_FOLDER, output_filename)
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            header, encoded = image_data.split(",", 1)
            image_binary = base64.b64decode(encoded)
            with open(temp_path, 'wb') as f:
                f.write(image_binary)
            image = Image.open(temp_path)
        else:
            return False, "Nieprawidłowy format danych wejściowych"
        if image.mode in ('RGBA', 'LA'):
            if target_format.lower() == 'jpg':
                image = image.convert('RGB')
            else:
                image = image.convert('RGBA')
        pillow_format = 'JPEG' if target_format.lower() == 'jpg' else target_format.upper()
        image.save(output_path, pillow_format)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return True, output_filename
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False, str(e)

# -----------------------------------------------
# Funkcja pobierania wideo/audio (przykładowa)
# -----------------------------------------------
def download_video(url, format_code, platform):
    try:
        output_filename = f"{uuid.uuid4()}"
        ydl_opts = {
            'format': format_code,
            'outtmpl': os.path.join(CONVERTED_FOLDER, f'{output_filename}.%(ext)s'),
            'merge_output_format': 'mp4' if 'video' in format_code else 'mp3',
            'quiet': True,
            'no_warnings': True,
        }
        if platform == 'tiktok':
            ydl_opts['cookies'] = 'cookies.txt'
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return True, {'message': 'Pobieranie zakończone pomyślnie!',
                      'filename': os.path.basename(filename)}
    except Exception as e:
        return False, f"Błąd podczas pobierania: {str(e)}"

# -----------------------------------------------
# Endpoint obfuskacji JS przy użyciu javascript-obfuscator
# -----------------------------------------------
def obfuscate_js(js_code: str, config: dict) -> str:
    """
    Obfuskacja kodu JS przy użyciu narzędzia javascript-obfuscator.
    Wymaga, aby Node.js oraz javascript-obfuscator były zainstalowane.
    """
    input_filename = os.path.join(TEMP_FOLDER, f"{uuid.uuid4()}.js")
    output_filename = os.path.join(TEMP_FOLDER, f"{uuid.uuid4()}_obf.js")
    with open(input_filename, "w", encoding="utf-8") as f:
        f.write(js_code)
    config_json = json.dumps(config)
    try:
        subprocess.check_output([
            "javascript-obfuscator",
            input_filename,
            "--output", output_filename,
            "--config", config_json
        ], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode('utf-8')}"
    with open(output_filename, "r", encoding="utf-8") as f:
        obfuscated_code = f.read()
    os.remove(input_filename)
    os.remove(output_filename)
    return obfuscated_code

@app.route('/obfuscate-js', methods=['POST'])
def obfuscate_js_endpoint():
    try:
        data = request.json
        js_code = data.get("code")
        config = data.get("config", {
            "compact": True,
            "controlFlowFlattening": True,
            "controlFlowFlatteningThreshold": 0.75,
            "deadCodeInjection": True,
            "deadCodeInjectionThreshold": 0.4,
            "debugProtection": True,
            "debugProtectionInterval": 2000,
            "disableConsoleOutput": True,
            "renameGlobals": False,
            "renameProperties": False,
            "selfDefending": True,
            "unicodeEscapeSequence": False,
            "target": "browser"
        })
        if not js_code:
            return jsonify(success=False, error="Brak kodu do obfuskacji")
        obfuscated = obfuscate_js(js_code, config)
        return jsonify(success=True, result=obfuscated)
    except Exception as e:
        return jsonify(success=False, error=str(e))

# -----------------------------------------------
# Endpointy dodatkowe
# -----------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert-image', methods=['POST'])
def convert_image():
    try:
        data = request.json
        image_data = data['image']
        target_format = data['format']
        success, result = handle_image_conversion(image_data, target_format)
        if success:
            return jsonify({'success': True,
                            'download_url': url_for('download_file', filename=result)})
        else:
            return jsonify({'success': False, 'error': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(CONVERTED_FOLDER, filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'Plik nie istnieje'}), 404
        # Używamy download_name (Flask 2.x); jeśli masz starszą wersję, użyj attachment_filename
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({'error': f"Błąd: {str(e)}"}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        file_type = data.get('file-type')
        if file_type == 'image':
            image_data = data.get('url')
            target_format = data.get('format', 'png').lower()
            success, result = handle_image_conversion(image_data, target_format)
            if not success:
                return jsonify({'error': result}), 400
            return jsonify({'message': 'Konwersja zakończona pomyślnie!',
                            'download_url': url_for('download_file', filename=result)})
        elif file_type in ['video', 'audio']:
            url_input = data.get('url')
            format_code = 'bestaudio/best' if file_type == 'audio' else 'bestvideo+bestaudio/best'
            platform = data.get('platform', 'youtube')
            if data.get('quality'):
                if data['quality'] == '1':
                    format_code = 'bestvideo[height<=720]+bestaudio/best'
                elif data['quality'] == '2':
                    format_code = 'bestvideo[height<=1080]+bestaudio/best'
            success, result = download_video(url_input, format_code, platform)
            if not success:
                return jsonify({'error': result}), 400
            return jsonify({'message': result['message'],
                            'download_url': url_for('download_file', filename=result['filename'])})
        return jsonify({'error': 'Nieprawidłowy typ pliku'}), 400
    except Exception as e:
        return jsonify({'error': f"Wystąpił błąd: {str(e)}"}), 500

@app.route('/process-code', methods=['POST'])
def process_code():
    try:
        data = request.json
        operation = data.get('operation')
        language = data.get('language')
        key = data.get('key')
        code = data.get('code')
        if not code:
            return jsonify({'success': False, 'error': "Brak kodu do przetworzenia"})
        if not key:
            return jsonify({'success': False, 'error': "Brak klucza"})
        if language == 'javascript':
            if operation == 'encrypt':
                result_code = new_js_encrypt(code, key)
                return jsonify({'success': True, 'result': result_code})
            elif operation == 'decrypt':
                result_code = "Funkcja deszyfrowania nie jest zaimplementowana."
                return jsonify({'success': True, 'result': result_code})
            else:
                return jsonify({'success': False, 'error': "Nieobsługiwana operacja"})
        elif language == 'cpp':
            result_code = new_cpp_encrypt(code, key)
            return jsonify({'success': True, 'result': result_code})
        else:
            return jsonify({'success': False, 'error': f"Nieznany język: {language}"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/encrypt-file', methods=['POST'])
def encrypt_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nie przesłano pliku'}), 400
        uploaded_file = request.files['file']
        language = request.form.get('language', 'javascript')
        key = request.form.get('key', '')
        if not key:
            return jsonify({'error': 'Brak klucza szyfrującego'}), 400
        original_content = uploaded_file.read().decode('utf-8', errors='replace')
        if language.lower() == 'javascript':
            encrypted_content = new_js_encrypt(original_content, key)
            ext = 'js'
        elif language.lower() == 'cpp':
            encrypted_content = new_cpp_encrypt(original_content, key)
            ext = 'cpp'
        else:
            return jsonify({'error': 'Nieobsługiwany język'}), 400
        output_filename = f"{uuid.uuid4()}.{ext}"
        output_path = os.path.join(CONVERTED_FOLDER, output_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_content)
        return jsonify({'message': 'Plik zaszyfrowany pomyślnie!',
                        'download_url': url_for('download_file', filename=output_filename)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

if __name__ == '__main__':
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(debug=True)
