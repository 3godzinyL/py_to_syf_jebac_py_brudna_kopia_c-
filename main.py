import os
import sys
import time
from yt_dlp import YoutubeDL

# Kolory ANSI
RESET = "\033[0m"
WHITE = "\033[37m"
GREEN = "\033[32m"

# Długość paska postępu
BAR_LENGTH = 20

def baner():
    """Prosty baner tekstowy."""
    print("=" * 50)
    print("   K O N W E R T E R   L I N K Ó W  (YouTube)  ")
    print("=" * 50)

def print_progress_bar(progress):
    """Wyświetla pasek postępu z animacją."""
    green_blocks = int(BAR_LENGTH * progress)
    white_blocks = BAR_LENGTH - green_blocks
    bar = GREEN + "#" * green_blocks + WHITE + "#" * white_blocks + RESET
    percent_display = int(progress * 100)
    print(f"[{bar}] {percent_display}%\r", end='', flush=True)

def clear_console():
    """Czyści konsolę."""
    os.system('cls' if os.name == 'nt' else 'clear')

def progress_hook(d):
    """Funkcja wywoływana przez yt_dlp podczas postępu pobierania."""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        if total_bytes:
            progress = downloaded / total_bytes
            print_progress_bar(progress)
    elif d['status'] == 'finished':
        print_progress_bar(1)
        print()  # przejście do nowej linii po ukończeniu

def pobierz_mp4(url, wybor_jakosci):
    if wybor_jakosci == "1":
        format_code = 'bestvideo[height<=720]+bestaudio/best'
    elif wybor_jakosci == "2":
        format_code = 'bestvideo[height<=1080]+bestaudio/best'
    else:
        format_code = 'bestvideo+bestaudio/best'
    
    ydl_opts = {
        'format': format_code,
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'ffmpeg_location': r'C:\Users\huber\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            channel_name = info.get('uploader', 'Nieznany kanał')
            
            print(f"Kanał: {channel_name}")
            print("Pobieranie w toku, proszę czekać...")
            
            ydl.download([url])
        print("Film (MP4) pobrany pomyślnie!")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def pobierz_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'C:\Users\huber\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            channel_name = info.get('uploader', 'Nieznany kanał')
            
            print(f"Kanał: {channel_name}")
            print("Pobieranie w toku, proszę czekać...")
            
            ydl.download([url])
        print("Audio (MP3) pobrane pomyślnie!")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def pobierz_tiktok(url, wybor_formatu):
    """Pobiera film z TikToka w wybranym formacie."""
    format_code = 'bestvideo+bestaudio/best' if wybor_formatu == "1" else 'bestaudio/best'
    
    ydl_opts = {
        'format': format_code,
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4' if wybor_formatu == "1" else None,
        'ffmpeg_location': r'C:\Users\huber\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-7.1-full_build\bin\ffmpeg.exe',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            channel_name = info.get('uploader', 'Nieznany kanał')
            
            print(f"Kanał: {channel_name}")
            print("Pobieranie w toku, proszę czekać...")
            
            ydl.download([url])
        print("Film (MP4) lub audio (MP3) pobrane pomyślnie!")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

def menu():
    """Wyświetla menu główne i obsługuje wybory użytkownika."""
    baner()
    print("1. YouTube (konwertuj link)")
    print("2. TikTok (pobierz film)")
    print("3. Wyjście")
    wybor_zrodla = input("Wybierz opcję: ").strip()
    return wybor_zrodla

def main():
    while True:
        clear_console()
        wybor_zrodla = menu()
        
        if wybor_zrodla == "1":
            url = input("Podaj link do filmu YouTube: ").strip()
            if not url:
                print("Nie podano linku. Powrót do menu...")
                time.sleep(2)
                continue
            
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
            
            input("Naciśnij ENTER, aby powrócić do menu...")
        
        elif wybor_zrodla == "2":
            url = input("Podaj link do filmu TikTok: ").strip()
            if not url:
                print("Nie podano linku. Powrót do menu...")
                time.sleep(2)
                continue
            
            print("Wybierz format:")
            print("1. MP4")
            print("2. MP3")
            wybor_formatu = input("Twój wybór: ").strip()
            
            if wybor_formatu == "1" or wybor_formatu == "2":
                pobierz_tiktok(url, wybor_formatu)
            else:
                print("Nieprawidłowy wybór formatu.")
        
        elif wybor_zrodla == "3":
            print("Zakończono działanie programu.")
            break
        
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            time.sleep(2)

if __name__ == "__main__":
    main()
