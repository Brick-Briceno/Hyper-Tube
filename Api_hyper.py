"""
Componente descargador de videos, y añadidor de substitulos
"""

from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube, Playlist, exceptions
import requests
from config import cf
import re

from pprint import pprint

"Area de descargar videos"

calidades = [
    "3840p", "2160p", "1440p",
    "1080p", "720p", "480p",
    "360p", "240p", "144p",
    ]

def limpiar_txt_carpetas(txt):
    final = ""
    for x in txt:
        if x.upper() in " 0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ": final += x
    return final

def descargar_archivo(url, nombre=None, ruta=""):
    response = requests.get(url, stream=True)
    with open(nombre, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk: f.write(chunk)

def descargar_video(url, nombre=None, ruta="", resolucion="1080p"):
    video = YouTube(url)
    # Filtra las corrientes por resolución
    if resolucion.lower() == "max":
        chosen_stream = video.streams.get_highest_resolution()
    else:
        filtered_streams = video.streams.filter(res=resolucion, file_extension="mp4")
        chosen_stream = filtered_streams.first()

    # Descarga el video en la ubicación especificada
    #chosen_stream.download(output_path=ruta, filename=nombre)


def extraer_id_youtube(url):
    #toma en cuenta que aquí no uso links con ajustes de tiempo
    patron = r"^(https?://)?((www.youtube.com/watch\?v=|youtu.be/|www\.youtube\.com/shorts/))([^&]+)"
    match = re.search(patron, url)
    if match: return match.group(4)

def es_url_lista_reproduccion(url):
    try:
        playlist = Playlist(url)
        return playlist.title, playlist.video_urls
    except: ...

class video_yt:
    def __init__(self, link, nombre=None, subs=False):
        self._id = extraer_id_youtube(url)
        self.nombre = nombre
        self.subs = subs
        self.bajado = 0
        self.peso = None

    def descargar(self):
        _link = f"https://www.youtube.com/watch?v={self.id}"
        video = YouTube(url)
        video_url = video.vid_info['streamingData']["formats"][0]["url"]

url = "https://www.youtube.com/watch?v=vMSrAcrH9tg&list=PLTIdiuUvwYCHrjyEIYR8ZOhza5NAFef3Y"
url = "https://www.youtube.com/watch?v=Ch_d076Ju8M"
url = "https://www.youtube.com/watch?v=ELSm-G201Ls"
url = "https://www.youtube.com/watch?v=UG3sfZKtCQI"
url = "https://www.youtube.com/embed/-RDBMu7BreE"


def streams_video_data(url):
    video = YouTube(url)
    data = {"calidad": [], "bitrate": [], "link": []}
    for streams in video.vid_info['streamingData']["adaptiveFormats"]:
        if "audio" in streams["mimeType"]: continue
        data["calidad"].append(streams["qualityLabel"])
        data["bitrate"].append(streams["bitrate"])
        data["link"].append(streams["url"])

def stream_audio(url):
    video = YouTube(url)
    bitrate = 0
    link = None
    for streams in video.vid_info['streamingData']["adaptiveFormats"]:
        if "video" in streams["mimeType"]: continue
        if streams["bitrate"] > bitrate:
            bitrate = streams["bitrate"]
            link = streams["url"]
    return video.title, link

#video.vid_info['streamingData']["adaptiveFormats"]#[0]["url"]
#video.video_id#.vid_info['streamingData']["adaptiveFormats"]#[0]["url"]

#except exceptions.RegexMatchError: print(555)

#video = YouTube(url).vid_info["videoDetails"]["title"]#.keys()#[0]["url"]

#data = stream_audio(url)

#pprint(data, indent=4)
