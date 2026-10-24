@echo off
title VELVET AI - Server & Control Center
cd /d "%~dp0"
echo ========================================================
echo   VELVET AI - Sistema de Control y Asistente ROXANNE
echo ========================================================
echo.
echo Iniciando servidor backend en http://localhost:8888 ...
start "" http://localhost:8888
python src/server/velvet_app_server.py
pause
