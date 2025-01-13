import os
from yt_dlp import YoutubeDL

def baner():
    """Prosty baner tekstowy."""
    print("=" * 50)
    print("   K O N W E R T E R   L I N K Ó W  (YouTube)  ")
    print("=" * 50)

def pobierz_mp4(url, wybor_jakosci):
    """
    Pobiera film z YouTube w formacie MP4, z wybraną jakością:
    - '1': 720p
    - '2': 1080p
    - '3': najwyższa dostępna
    """
    # Określamy formaty wg wyboru
    if wybor_jakosci == "1":
        # max 720p
        format_code = 'bestvideo[height<=720]+bestaudio/best'
    elif wybor_jakosci == "2":
        # max 1080p
        format_code = 'bestvideo[height<=1080]+bestaudio/best'
    else:
        # najwyższa dostępna (może być np. 4K)
        format_code = 'bestvideo+bestaudio/best'
    
    # Opcje pobierania
    ydl_opts = {
        'format': format_code,
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        
        # KONIECZNE, aby yt-dlp wiedziało, gdzie jest ffmpeg (jeśli PATH nie działa).
        'ffmpeg_location': r'C:\Users\huber\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe',
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Najpierw pobieramy informacje o filmie (aby wyświetlić nazwę kanału)
            info = ydl.extract_info(url, download=False)
            channel_name = info.get('uploader', 'Nieznany kanał')
            
            print(f"Kanał: {channel_name}")
            print("Pobieranie w toku, proszę czekać...")
            
            # Teraz właściwe pobieranie:
            ydl.download([url])
        print("Film (MP4) pobrany pomyślnie!")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def pobierz_mp3(url):
    """
    Pobiera audio z YouTube w formacie MP3 (192 kbps).
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }
        ],
        
        # Również wskażemy lokalizację ffmpeg
        'ffmpeg_location': r'C:\Users\huber\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe',
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Najpierw tylko informacja (nazwa kanału)
            info = ydl.extract_info(url, download=False)
            channel_name = info.get('uploader', 'Nieznany kanał')
            
            print(f"Kanał: {channel_name}")
            print("Pobieranie w toku, proszę czekać...")
            
            # Pobieranie i konwersja do MP3
            ydl.download([url])
        print("Audio (MP3) pobrane pomyślnie!")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def main():
    baner()
    print("1. YouTube (konwertuj link)")
    wybor_zrodla = input("Wybierz [1] lub wyjdź [ENTER]: ").strip()
    
    if wybor_zrodla == "1":
        url = input("Podaj link do filmu YouTube: ").strip()
        if not url:
            print("Nie podano linku. Zamykanie programu.")
            return
        
        print("Wybierz format:")
        print("1. MP4")
        print("2. MP3")
        wybor_formatu = input("Twój wybór: ").strip()
        
        if wybor_formatu == "1":
            print("Wybierz jakość wideo:")
            print("1. 720p")
            print("2. 1080p")
            print("3. Najwyższa dostępna")
            wybor_jakosci = input("Twój wybór: ").strip()
            pobierz_mp4(url, wybor_jakosci)
        
        elif wybor_formatu == "2":
            pobierz_mp3(url)
        
        else:
            print("Nieprawidłowy wybór formatu.")
    else:
        print("Zakończono działanie programu.")

if __name__ == "__main__":
    main()
