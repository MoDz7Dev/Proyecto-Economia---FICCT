@echo off
REM ============================================================
REM  Hipermaxi - Lanzador del proyecto
REM  Ejecuta run.py: levanta la API (FastAPI, puerto 8000) y
REM  abre la aplicacion Flet en el navegador (puerto 8080).
REM ============================================================
setlocal

REM Carpeta raiz del proyecto (donde esta este archivo)
set "ROOT=%~dp0"
set "PY=%ROOT%venv\Scripts\python.exe"

REM Verificar que exista el entorno virtual
if not exist "%PY%" (
    echo [ERROR] No se encontro el entorno virtual en:
    echo         "%PY%"
    echo.
    echo Crealo con:
    echo    python -m venv venv
    echo    venv\Scripts\python -m pip install -r requirements.txt
    pause
    exit /b 1
)

cd /d "%ROOT%"
echo Iniciando Hipermaxi (API en http://127.0.0.1:8000 y app en http://127.0.0.1:8080)...
"%PY%" run.py

endlocal
