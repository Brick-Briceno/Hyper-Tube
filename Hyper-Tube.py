"""
Hyper Tube v1.1
@Brick_briceno 2024
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QShortcut, QMessageBox, QHeaderView
from pytube import YouTube, Playlist
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QUrl, Qt
from it_ui import Ui_MainWindow
import time
import re
import os


class DL:
    def descargar_video(url, nombre, ruta, resolucion):
        video = YouTube(url)

        # Filtra las corrientes por resolución
        if resolucion.lower() == "max":
            chosen_stream = video.streams.get_highest_resolution()
        else:
            filtered_streams = video.streams.filter(res=resolucion, file_extension="mp4")
            chosen_stream = filtered_streams.first()

        # Descarga el video en la ubicación especificada
        chosen_stream.download(output_path=ruta, filename=nombre)

    def es_url_lista_reproduccion(url):
        try:
            playlist = Playlist(url)
            playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            return playlist.title, playlist
        except: return ["", [url]]

    def limpiar(txt):
        final = ""
        for x in txt:
            if x.upper() in " 0123456789ABCDEFGHIJKLMNÑOPQRSTUVWXYZ": final += x
        return final

    on = True
    lista = [
        #aquí estarán listas con indices:
        #[URL, Nombre, nombre_lista]
    ]
    conf = {"resolucion": "max",
            "indices": True,
            "ruta": "%USERPROFILE%/Videos/YT"
            }
    
    def agregar(url):
        DL.conf["indices"] = ventana.indices.isChecked()
        print(DL.conf["indices"])

        nueva_lista = []
        nombre_lista, lista = DL.es_url_lista_reproduccion(url)
        for video in lista:
            nueva_lista.append([video, ])        
        

    def descargar():
        indice = 0
        intentos = 3
        while DL.on:
            url, titulo, nombre_lista = DL.lista[indice]
            try:
                DL.descargar(url, titulo,
                            DL.limpiar(DL.conf["ruta"].strip("\\")+nombre_lista),
                            DL.conf["resolucion"])
                DL.lista.pop(0)
                indice += 1
            except:
                print("ha ocurrido un error")
                if not intentos:
                    intentos -= 1
                    print(f"intentos restantes {intentos}")
                    continue
                else:
                    DL.lista.pop(0)
                    indice += 1


class MiVentana(QMainWindow, Ui_MainWindow):
    valor = False
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.97)
        self.showMaximized()

        def pantalla_completa():
            if ventana.valor: self.showMaximized()
            else: self.showFullScreen()
            ventana.valor = not ventana.valor

        "Botones"
        #self.descargar.clicked.connect()
        #self.play_pause.clicked.connect()

        "Sliders"
        #self.ajustar_reso.valueChanged.connect()
        #radioButton.isChecked()

        "Line Edits"
        #self.buscador.returnPressed.connect()
        #self.buscador.setPlaceholderText("")

        "Tablas"
        #self.tabla_contactos.cellClicked.connect()
        #self.tabla_contactos_2.cellClicked.connect()
        #self.tabla_contactos_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        "Atajos"
        QShortcut(QKeySequence("F11"), self, pantalla_completa)
        QShortcut(QKeySequence("Ctrl+D"), self, pantalla_completa)


app = QApplication([])
ventana = MiVentana()
ventana.show()

"Funciones de inicio"

app.exec_()#iniciar

"Funciones de salida"

DL.on = False
