"""Hipermaxi - Punto de entrada.

Levanta el servidor de la API (FastAPI/uvicorn) y abre la aplicacion Flet
en el navegador.  Ejecutar SIEMPRE desde la raiz del proyecto:

    python run.py
"""
import subprocess
import sys

import flet as ft

from src.ui.app import main

# Evita errores de codificacion (emojis) cuando la salida se redirige a un archivo
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass



def start_api() -> subprocess.Popen:
    """Inicia el servidor FastAPI en un proceso aparte (puerto 8000)."""
    return subprocess.Popen(
        [
            sys.executable, "-m", "uvicorn", "src.api.server:app",
            "--host", "127.0.0.1", "--port", "8000",
        ]
    )


def run() -> None:
    api = start_api()
    try:
        ft.app(
            target=main,
            assets_dir="assets",
            view=ft.WEB_BROWSER,
            port=8080,
        )
    finally:
        api.terminate()
        try:
            api.wait(timeout=5)
        except Exception:
            api.kill()


if __name__ == "__main__":
    run()
