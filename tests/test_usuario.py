"""Pruebas del resumen de usuario y del cierre de sesión.

Ejecutar desde la raiz:   python -m tests.test_usuario
"""
import os

import flet as ft

from src.core import session as sess
from src.ui.main_view import UIApp

SES_FILE = "storage/temp/session.json"


class _Dummy:
    color_purple = "#cf672b"
    color1_card = "#e3501b"


def _backup():
    if os.path.exists(SES_FILE):
        with open(SES_FILE, encoding="utf-8") as f:
            return f.read()
    return None


def _restore(content):
    if content is not None:
        os.makedirs(os.path.dirname(SES_FILE), exist_ok=True)
        with open(SES_FILE, "w", encoding="utf-8") as f:
            f.write(content)
    elif os.path.exists(SES_FILE):
        os.remove(SES_FILE)


def test_resumen_usuario():
    original = _backup()
    try:
        sess.session_manager.save_session({
            "ci": 1001, "user": "admin", "name": "Carlos Rodríguez",
            "email": "carlos.rodriguez@hipermaxi.com", "contact": "78899111",
            "status": "active", "role": "admin", "department": "Gerencia",
            "hire_date": "2020-01-15",
        })

        d = _Dummy()
        d._get_current_user = sess.session_manager.get_user_data
        d.logout = UIApp.logout.__get__(d)

        col = UIApp._build_user_popup_content(d)
        assert isinstance(col, ft.Column)

        buttons = [c for c in col.controls if isinstance(c, ft.ElevatedButton)]
        assert buttons, "debe existir el boton de cerrar sesion"
        assert buttons[0].text == "Cerrar sesión"
        assert buttons[0].on_click is not None
        print("test_resumen_usuario OK")
    finally:
        _restore(original)


def test_logout():
    original = _backup()
    try:
        sess.session_manager.save_session(
            {"user": "admin", "name": "Admin", "role": "admin"})

        class _Page:
            def __init__(self):
                self.routes = []

            def go(self, route):
                self.routes.append(route)

        d = _Dummy()
        d.page = _Page()
        d.user_popup = ft.Container(visible=True)

        UIApp.logout(d, None)

        assert d.page.routes == ["/login"], d.page.routes
        assert d.user_popup.visible is False
        assert sess.session_manager.get_user_data() is None
        print("test_logout OK")
    finally:
        _restore(original)


if __name__ == "__main__":
    test_resumen_usuario()
    test_logout()
    print("TODOS LOS TESTS OK")
