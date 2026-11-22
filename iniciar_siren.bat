@echo off
title SIREN AI - Server & Control Center (by ALMA TECH)
cd /d "%~dp0"
echo ========================================================
echo   SIREN AI - Centro de Inteligencia y Co-Piloto Táctico
echo   Powered by ALMA TECH Ecosistema
echo ========================================================
echo.
echo Iniciando servidor backend en http://localhost:8888 ...
start "" http://localhost:8888
python src/server/start_tunnel.py
pause
