@echo off
chcp 65001 >nul
title SIREN AI - Command & Intelligence Center
cls

echo ========================================================
echo        ⚡ SIREN AI — Multi-Platform Command Center ⚡
echo             Sam Barton • Executive Dashboard
echo ========================================================
echo.
echo [1/3] Verificando entorno Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en el PATH. Instala Python 3.10+.
    pause
    exit /b 1
)

echo [2/3] Abriendo SIREN AI Command en tu navegador...
start http://localhost:8888

echo [3/3] Iniciando Servidor SIREN AI y Copiloto ROXANNE en el puerto 8888...
echo Presiona Ctrl + C en esta ventana para detener el servidor.
echo --------------------------------------------------------
python src/server/siren_app_server.py

pause
