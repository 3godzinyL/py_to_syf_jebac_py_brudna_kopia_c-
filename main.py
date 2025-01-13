from pytube import YouTube

def pobierz_film(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if stream:
            stream.download()
            print("Film pobrany pomyślnie!")
        else:
            print("Nie znaleziono strumienia do pobrania.")
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

url = 'https://youtu.be/2lAe1cqCOXo'
pobierz_film(url)