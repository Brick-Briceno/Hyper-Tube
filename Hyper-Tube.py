"""
Hyper Tube v1.1
@Brick_briceno 2024
"""

from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
QTableWidgetItem, QShortcut, QApplication, QMainWindow)
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube, Playlist, exceptions
from PyQt5.QtGui import QKeySequence, QColor
from it_ui import Ui_MainWindow
from threading import Thread
import Api_hyper as ht
from config import cf
import requests
import random
import time
import os
import re


class hp:
    #variables
    celda_selecionada = None
    "administrar widgets"
    def cambiar_color_texto_celda(
            tabla, fila,
            columna, texto="",
            color=QColor.fromHslF(0, 0, 0, 0)):
        item = QTableWidgetItem()
        tabla.setItem(fila, columna, item)
        item.setText(texto)
        item.setBackground(QColor(color))

    def cantidad_celdas(tabla, filas=1, columnas=1):
        tabla.setRowCount(filas)
        tabla.setColumnCount(columnas)

    def actualizar_lista():
        hp.cantidad_celdas(ventana.lista, len(cf["video list"]["Name"]))
        for i, name in enumerate(cf["video list"]["Name"]):
            hp.cambiar_color_texto_celda(ventana.lista, i, 0, name)
    
    "control de sistema"
    
    def inicio():
        hp.actualizar_lista()

    def set_calidad(v):
        cf["resolution"] = ht.calidades[::-1][v]
        ventana.reso.setText(f"Resolución: {cf["resolution"]}")
        cf.guardar()

    def eliminar():
        if hp.celda_selecionada == None:
            ventana.statusbar.showMessage("Selecione un video para Eliminarlo!")
        else:
            name = cf["video list"]["Name"][hp.celda_selecionada]
            cf["video list"]["Name"].pop(hp.celda_selecionada)
            cf["video list"]["ID"].pop(hp.celda_selecionada)
            cf["video list"]["Data"].pop(hp.celda_selecionada)
            cf.guardar()
            hp.celda_selecionada = None
            hp.actualizar_lista()
            ventana.statusbar.showMessage(f"Se ha eliminado {name}")

    def anadir():
        link = ventana.buscador.displayText()
        try: _id = link
        except ht.exceptions.RegexMatchError:
            ventana.statusbar.showMessage(f"Enlace no valido {link}")
        cf["video list"]["Name"].append(f"Cargando datos de video: {_id}")
        cf["video list"]["ID"].append(_id)
        cf["video list"]["Data"].append(False)
        hp.actualizar_lista()

    def indices():
        cf["list count"] = not ventana.indices.isChecked()
        cf.guardar()
    
    def seleccionar(l, c): hp.celda_selecionada = l

    "motor de descargas"

    motor_vivo = True
    def motor_descargas():
        while hp.motor_vivo:
            for _id in cf["video list"]["ID"]:
                try:
                    #iniciar descarga
                    video = ht.video_yt(_id)
                    #verificar si es lista de reproducción
                    video.descargar()
                    #descarga completada
                except: time.sleep(random.randint(1, 50**4)/1000)

    def nombres_listas():
        while hp.motor_vivo:
            #obtener nombres de videos
            for _id, is_data in zip(
                cf["video list"]["ID"],
                cf["video list"]["Data"]):
                if not is_data:
                    try: cf["video list"]["Name"] = YouTube(
                        f"https://www.youtube.com/watch?v={_id})").title
                    except: ...
                time.sleep(1)


class MiVentana(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.97)
        self.showMaximized()
        self.valor = False

        def pantalla_completa():
            if self.valor: self.showMaximized()
            else: self.showFullScreen()
            self.valor = not ventana.valor

        "Botones"
        #self.descargar.clicked.connect()
        #self.play_pause.clicked.connect()

        "Sliders"
        self.ajustar_resol.valueChanged.connect(hp.set_calidad)
        "Radio button"
        self.indices.pressed.connect(hp.indices)

        "Line Edits"
        self.buscador.returnPressed.connect(hp.anadir)
        #self.buscador.setPlaceholderText("")

        "Tablas"
        self.lista.cellClicked.connect(hp.seleccionar)

        "Atajos"
        QShortcut(QKeySequence("F11"), self, pantalla_completa)
        QShortcut(QKeySequence("Ctrl+D"), self, hp.eliminar)


app = QApplication([])
ventana = MiVentana()
ventana.show()

"Funciones de inicio"
hp.inicio()
Thread(target=hp.motor_descargas).start()

app.exec_()#iniciar
hp.motor_vivo = False

"Funciones de salida"
