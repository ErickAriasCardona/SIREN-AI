@echo off
title SIREN AI - Servidor y Consola Local
echo ========================================================
echo        INICIANDO SIREN AI (Sam Barton Command)
echo ========================================================
echo.
echo Abriendo navegador en http://localhost:8888/ ...
start http://localhost:8888/
python src/server/siren_app_server.py
pause
