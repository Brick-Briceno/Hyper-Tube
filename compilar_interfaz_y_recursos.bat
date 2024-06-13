@echo off
title Compilando :D
echo Compilando Interfaz y recursos
echo espere...

pyuic5 it.ui -o it_ui.py
pyrcc5 it.qrc -o it_rc.py
