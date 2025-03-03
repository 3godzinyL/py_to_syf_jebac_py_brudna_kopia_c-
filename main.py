from flask import Flask, render_template, request, jsonify
from yt_dlp import YoutubeDL
import os
from PIL import Image
import io

app = Flask(__name__)

def pobierz_wideo(url, format_code):
    ydl_opts = {
        'format': format_code,
        'outtmpl': '%(title)s.%(ext)s',  # Zmieniono aby zapisywało plik w formacie tytułu
        'merge_output_format': 'mp4' if 'video' in format_code else None,
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, "Pobieranie wideo zakończone pomyślnie!"
    except Exception as e:
        return False, str(e)

def konwertuj_obraz(plik_wejsciowy, format):
    try:
        # Otwórz obraz
        img = Image.open(plik_wejsciowy)
        plik_sciezki = os.path.splitext(plik_wejsciowy)[0] + '.' + format
        img.save(plik_sciezki)
        
        return True, f"Konwersja zakończona! Zapisano jako {plik_sciezki}"
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    format = data['format']
    quality = data.get('quality', None)
    
    if data['file-type'] == 'video':
        if format == 'mp4':
            if quality == "1":
                format_code = 'bestvideo[height<=720]+bestaudio/best'
            elif quality == "2":
                format_code = 'bestvideo[height<=1080]+bestaudio/best'
            else:
                format_code = 'bestvideo+bestaudio/best'
        elif format == 'mp3':
            format_code = 'bestaudio/best'
        else:
            return jsonify({'message': 'Nieprawidłowy format video'}), 400

        success, message = pobierz_wideo(url, format_code)

    elif data['file-type'] == 'image':
        if "data:image" in url:
            format = format.lower()  # Upewniamy się, że format jest małymi literami
            # Zapisać obraz jako plik
            image_data = url.split(",")[1]
            image_binary = io.BytesIO(base64.b64decode(image_data))
            success, message = konwertuj_obraz(image_binary, format)
        else:
            return jsonify({'message': 'Nieprawidłowy URL dla obrazu'}), 400
            
    else:
        return jsonify({'message': 'Nieprawidłowy typ pliku'}), 400

    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)
