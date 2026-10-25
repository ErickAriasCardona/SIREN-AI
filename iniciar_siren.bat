@echo off
title SIREN AI - Servidor y Tunel Remoto para el Estudio
echo ========================================================================
echo                  INICIANDO SIREN AI (Sam Barton Command)
echo ========================================================================
echo.
echo 1. Verificando motor de IA y servidor local...
echo 2. Generando Tunel Seguro HTTPS para conectar el Estudio con tu Casa...
echo.
python src\server\start_tunnel.py
pause
