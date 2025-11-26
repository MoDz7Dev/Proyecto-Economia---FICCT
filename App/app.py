import flet as ft
from login import UILogin
from main import UIApp

def main(page: ft.Page):

    def route_change(route):
        page.views.clear()

        if page.route == "/login":   # Página login
            page.views.append(
                ft.View(
                    route="/login",
                    controls=[UILogin(page)],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        elif page.route == "/main":  # Página principal
            page.views.append(
                ft.View(
                    route="/main",
                    controls=[UIApp(page)],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go("/login")   # Abrir en la vista login

ft.app(target=main, assets_dir="assets")
