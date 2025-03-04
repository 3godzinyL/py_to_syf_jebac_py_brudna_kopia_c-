from flask import Flask, render_template, request, jsonify, send_file
from yt_dlp import YoutubeDL
import os
import base64
from PIL import Image
import io
import uuid
from werkzeug.utils import secure_filename
import mimetypes

app = Flask(__name__)

# Konfiguracja aplikacji
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Tworzenie katalogów jeśli nie istnieją
for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def handle_image_conversion(image_data, target_format):
    try:
        # Upewnij się, że katalogi istnieją
        for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # Generuj unikalne nazwy plików
        temp_filename = f"{uuid.uuid4()}_temp.png"
        output_filename = f"{uuid.uuid4()}.{target_format.lower()}"
        
        temp_path = os.path.join(UPLOAD_FOLDER, temp_filename)
        output_path = os.path.join(CONVERTED_FOLDER, output_filename)

        # Zapisz oryginalny plik
        if isinstance(image_data, str) and image_data.startswith('data:image'):
            # Wyciągnij właściwe dane base64
            header, encoded = image_data.split(",", 1)
            image_binary = base64.b64decode(encoded)
            with open(temp_path, 'wb') as f:
                f.write(image_binary)
            image = Image.open(temp_path)
        else:
            return False, "Nieprawidłowy format danych wejściowych"

        # Konwertuj i zapisz obraz
        if image.mode in ('RGBA', 'LA'):
            if target_format.lower() == 'jpg':
                # Konwertuj do RGB jeśli zapisujemy jako JPG
                image = image.convert('RGB')
            elif target_format.lower() == 'png':
                # Zachowaj przezroczystość dla PNG
                image = image.convert('RGBA')
            else:
                # Dla innych formatów konwertuj do RGB
                image = image.convert('RGB')
        
        # Zapisz z odpowiednimi parametrami jakości
        if target_format.lower() == 'jpg':
            image.save(output_path, format='JPEG', quality=95, optimize=True)
        elif target_format.lower() == 'png':
            image.save(output_path, format='PNG', optimize=True)
        elif target_format.lower() == 'webp':
            image.save(output_path, format='WEBP', quality=95, method=6)
        else:
            image.save(output_path, format=target_format.upper())

        # Usuń tymczasowy plik
        try:
            os.remove(temp_path)
        except:
            pass
        
        return True, {
            'message': 'Konwersja zakończona pomyślnie!',
            'filename': output_filename,
            'path': output_path
        }
    except Exception as e:
        return False, f"Błąd podczas konwersji obrazu: {str(e)}"

def download_video(url, format_code, platform):
    try:
        # Upewnij się, że katalogi istnieją
        for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # Generuj unikalną nazwę pliku
        output_filename = f"{uuid.uuid4()}"
        
        ydl_opts = {
            'format': format_code,
            'outtmpl': os.path.join(CONVERTED_FOLDER, f'{output_filename}.%(ext)s'),
            'merge_output_format': 'mp4' if 'video' in format_code else 'mp3',
            'quiet': True,
            'no_warnings': True,
        }

        # Dodatkowe opcje dla różnych platform
        if platform == 'tiktok':
            ydl_opts['cookies'] = 'cookies.txt'
        
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        return True, {
            'message': 'Pobieranie zakończone pomyślnie!',
            'filename': os.path.basename(filename),
            'path': filename
        }
    except Exception as e:
        return False, f"Błąd podczas pobierania: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

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
                
            return jsonify({
                'message': result['message'],
                'download_url': f"/download_file/{result['filename']}"
            })

        elif file_type in ['video', 'audio']:
            url = data.get('url')
            format_code = 'bestaudio/best' if file_type == 'audio' else 'bestvideo+bestaudio/best'
            platform = data.get('platform', 'youtube')
            
            if data.get('quality'):
                if data['quality'] == '1':
                    format_code = 'bestvideo[height<=720]+bestaudio/best'
                elif data['quality'] == '2':
                    format_code = 'bestvideo[height<=1080]+bestaudio/best'

            success, result = download_video(url, format_code, platform)
            
            if not success:
                return jsonify({'error': result}), 400
                
            return jsonify({
                'message': result['message'],
                'download_url': f"/download_file/{result['filename']}"
            })

        return jsonify({'error': 'Nieprawidłowy typ pliku'}), 400

    except Exception as e:
        return jsonify({'error': f"Wystąpił błąd: {str(e)}"}), 500

@app.route('/download_file/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(CONVERTED_FOLDER, filename)
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'Plik nie istnieje'}), 404

        # Określ typ MIME
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Dodaj odpowiednie nagłówki dla różnych typów plików
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': mime_type
        }

        return send_file(
            file_path,
            mimetype=mime_type,
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({'error': f"Błąd podczas pobierania pliku: {str(e)}"}), 500

@app.after_request
def add_header(response):
    """Dodaj nagłówki CORS i cache control."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

def cleanup_old_files():
    """Usuń stare pliki (starsze niż 1 godzina)."""
    import time
    current_time = time.time()
    for folder in [UPLOAD_FOLDER, CONVERTED_FOLDER]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.getmtime(file_path) < current_time - 3600:  # 1 godzina
                try:
                    os.remove(file_path)
                except:
                    pass

if __name__ == '__main__':
    # Dodatkowe zależności
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit 16MB dla przesyłanych plików
    
    # Uruchom czyszczenie starych plików w tle
    from threading import Thread
    import time
    
    def cleanup_thread():
        while True:
            cleanup_old_files()
            time.sleep(3600)  # Sprawdzaj co godzinę
    
    Thread(target=cleanup_thread, daemon=True).start()
    
    app.run(debug=True) 
