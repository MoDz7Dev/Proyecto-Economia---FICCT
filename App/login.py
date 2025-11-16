import flet as ft
from flet import Icons
import json
import requests

class UILogin(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        print("Window type:", page.platform) #? Imprime en que plataforma esta corriendo la ventana
        self.page = page
        self.page.padding = 0
        self.page.window_icon = "Hipermaxi_logo.ico" #! No funciona (Aun no encuentro solucion)
        self.page.title = "Hipermaxi - Gestor Administrativo"
        
        

        #Definimos paleta de colores
        self.color_blue = "#73bf16"
        self.color_purple = "#cf672b"
        self.bg_color = "#3d355f"
        self.container_color = "#362e57"
        self.color_navegation_bt = "#2a2949"
        self.color1_card = "#e3501b"
        self.color2_card = "#d6820c"

        self.page.bgcolor = self.bg_color

        self.page.update()

        #Estilo de animacion para transiciones y efectos
        self.animation_style = ft.Animation(500, ft.AnimationCurve.EASE_IN_TO_LINEAR)
        
ft.app(target=lambda page: UILogin(page), assets_dir="assets")
