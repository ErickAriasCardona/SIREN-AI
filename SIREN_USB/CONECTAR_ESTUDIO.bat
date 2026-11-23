@echo off
title SIREN AI - Conector Satelite de Estudio (USB Plug & Play)
color 0b
echo ========================================================================
echo        SIREN AI - CONECTOR SATELITE DE TRANSMISION (USB)
echo ========================================================================
echo.
echo [1/3] Detectando motor de ejecucion en la memoria USB...

set SCRIPT_DIR=%~dp0
set PY_PORTABLE=%SCRIPT_DIR%python\python.exe

if exist "%PY_PORTABLE%" (
    echo [OK] Usando Python Portable de la USB (Sin instalacion requerida).
    set RUNNER="%PY_PORTABLE%"
) else (
    where python >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        echo [OK] Usando Python del sistema.
        set RUNNER=python
    ) else (
        echo [!] Python no detectado. Lanzando conector nativo PowerShell...
        powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%siren_satellite.ps1"
        goto fin
    )
)

echo [2/3] Localizando StreamMonitor en este ordenador...
echo [3/3] Estableciendo enlace seguro con el PC Central de SIREN...
echo.

%RUNNER% "%SCRIPT_DIR%siren_satellite.py"

:fin
echo.
echo Presione cualquier tecla para cerrar esta ventana...
pause >nul
