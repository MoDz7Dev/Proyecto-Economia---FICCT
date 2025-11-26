import flet as ft
from flet import Icons
import json
import requests

class UILogin(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.page = page
        self.page.padding = 0
        self.page.window_icon = "Hipermaxi_logo.ico" #! No funciona (Aun no encuentro solucion)
        self.page.title = "Hipermaxi - Inicio de sesión"

        # Configuración de la ventana
        self.page.window_width = 1000
        self.page.window_height = 600
        self.page.window_resizable = False

        #Paletas de colores
        self.color_blue = "#73bf16"
        self.color_purple = "#cf672b"
        # Color usado para mensajes de error
        self.error_color = "#e74c3c"
        self.bg_color = "#21324e"
        self.container_color = "#1c2b45"
        self.color_navegation_bt = "#21324e"
        self.color1_card = "#e3501b"
        self.color2_card = "#d6820c"
        # Color principal para textos informativos
        self.color_primary = self.color_blue

        self.page.bgcolor = self.bg_color

        self.api_url = "http://127.0.0.1:8000" # URL de la API

        self.animation_style = ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT) # Animación

        #Estilo de animacion para transiciones y efectos
        self.animation_style = ft.Animation(500, ft.AnimationCurve.EASE_IN_TO_LINEAR)

        # ENTRADA DE USUARIO
        self.username_field = ft.TextField(
            label="Usuario",
            prefix_icon=Icons.PERSON,
            width=350,
            height=60,
            border_color=self.color_blue,
            focused_border_color=self.color_purple,
            cursor_color=self.color_blue,
            text_size=16,
            on_submit=lambda e: self.handle_login(e) #Enter para login
        )

        # ENTRADA DE CONTRASEÑA
        self.password_field = ft.TextField(
            label="Contraseña",
            prefix_icon=Icons.LOCK,
            password=True,
            can_reveal_password=True,
            width=350,
            height=60,
            border_color=self.color_blue,
            focused_border_color=self.color_purple,
            color="white",
            label_style=ft.TextStyle(color="white"),
            cursor_color=self.color_blue,
            text_size=16,
            on_submit=lambda e: self.handle_login(e) #Enter para login
        )

        # MENSAJE DE ERROR AL COLOCAR MAL EL USUARIO - SOLO ES UN CONTENEDOR
        self.error_message = ft.Container(
            visible=False,
            bgcolor=ft.Colors.with_opacity(0.9, self.error_color),
            border_radius=10,
            padding=15,
            width=350,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Icon(Icons.ERROR_OUTLINE, color="white", size=24),
                    ft.Text(
                        "",
                        color="white",
                        size=14,
                        weight="bold"
                    )
                ]
            )            
        )

        # INDICADOR DE CARGA
        self.loading_indicator = ft.Container(
            visible=False,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.ProgressRing(color=self.color_blue, width=20, height=20),
                    ft.Text(value="Verificando cuenta de usuario...", color="white", size=14)
                ]
            )
        )

        self.login_button = ft.ElevatedButton(
            text="INICIAR SESIÓN",
            on_click=self.handle_login,
            width=350,
            height=50,
            style=ft.ButtonStyle(
                bgcolor=self.color_purple,
                color="white",
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            icon=Icons.LOGIN
        )
    
        # AHORA ESTE ES EL PANEL IZQUIERO (EL BRANDING-LOGO)
        self.left_panel = ft.Container(
            expand=2,
            bgcolor=self.container_color, # color del contenedor
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        src="Hipermaxi_logo.png",
                        width=250,
                        height=150,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    ft.Text(
                        value="SISTEMA DE GESTIÓN",
                        size=28,
                        weight="bold",
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        value="ADMINISTRATIVA",
                        size=28,
                        weight="bold",
                        color="white",
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Container(height=20),
                    ft.Text(
                        value="Hipermaxi Las Brisas S.A.", # Esto es solo un ejemplo
                        size=16,
                        color=ft.Colors.GREY_400,
                        text_align=ft.TextAlign.CENTER
                    )
                ]
            )
        )

        # ESTE ES EL PANEL DERECHO - LOGIN
        self.right_panel = ft.Container(
            expand=3,
            bgcolor=self.bg_color,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value="Bienvenido",
                        size=32,
                        weight="bold",
                        color="white"
                    ),
                    ft.Text(
                        value="Ingresa tu credenciales para continuar",
                        size=14,
                        color=ft.Colors.GREY_400
                    ),
                    ft.Container(height=30), # Es para dar espacio de 30 xD

                    # Campo de usuario
                    self.username_field,
                    # Campo de contraseña
                    self.password_field,
                    ft.Container(height=10),
                    self.error_message,
                    ft.Container(height=10),
                    # Indicador de carga
                    self.loading_indicator,
                    # Boton de login
                    self.login_button,
                    ft.Container(height=30),
                    # Información de ayuda
                    ft.Container(
                        width=350,
                        padding=15,
                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                        border_radius=10,
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    "👤 Usuarios de prueba:",
                                    size=12,
                                    weight="bold",
                                    color=self.color_primary
                                ),
                                ft.Text("• admin / admin123 (Gerente)", size=11, color=ft.Colors.GREY_400),
                                ft.Text("• supervisor / super123 (Supervisor)", size=11, color=ft.Colors.GREY_400),
                                ft.Text("• cajero1 / caj123 (Cajero)", size=11, color=ft.Colors.GREY_400),
                            ]
                        )
                    )
                ]
            )
        )

        # AHORA ESTE ES EL CONTENEDOR PRINCIPAL
        self.content = ft.Row(
            expand=True,
            spacing=0,
            controls=[
                self.left_panel,
                self.right_panel
            ]                             
        )

        #self.page.add(self) # Añadir a la pagina principal
        #self.page.update()

    # ESTAS SON LAS FUNCIONES DEL OBJETO LOGIN
    def show_error(self, message: str): # Muestra un mensaje de error al iniciar sesión
        error_text = self.error_message.content.controls[1] # El contenedor de mensaje de error
        error_text.value = message
        self.error_message.visible = True
        self.page.update()

    def hide_error(self): # Oculta el mensaje de error
        self.error_message.visible = False
        self.page.update()

    def show_loading(self, show: bool): # Muestra/oculta el indicador de carga
        self.loading_indicator.visible = show # mostrar/ocultar
        self.login_button.disabled = show # habilitar/desabilitar
        self.page.update()

    def handle_login(self, e): # Maneja el evento de login
        # Limpiar errores previos
        self.hide_error()

        # Obtener valores
        username = self.username_field.value
        password = self.password_field.value

        # Validar campos vacios
        if not username or not password:
            self.show_error("Por favor, completa todos los campos")
            return
        
        # Mostrar indicador de carga
        self.show_loading(True)

        try:
            # Hacer petición a la API
            response = requests.post(
                url=f"{self.api_url}/login",
                json={
                    "user":username,
                    "password":password
                },
                timeout=5
            )

            # Pasear respuesta
            data = response.json()

            if data.get("success"):
                user_data = data.get("user_data") # Login exitoso
                self.save_session(user_data) # Guardar sesión
                self.show_success_and_redirect(user_data) # Mostrar mensaje exitoso
            else:
                self.show_loading(False) # Login fallido
                self.show_error(data.get("message", "Error desconocido"))
        
        except requests.exceptions.ConnectionError:
            self.show_loading(False)
            self.show_error("No se pudo conectar al servidor. Asegúrate de que esté ejecutándose.")
        
        except requests.exceptions.Timeout:
            self.show_loading(False)
            self.show_error(f"Tiempo de espera agotado. Intenta nuevamente")
        
        except Exception as ex:
            self.show_loading(False)
            self.show_error(f"Error inesperado: {str(ex)}")

    def save_session(self, user_data: dict):
        try:
            import session
            session.save_session(user_data)
        except Exception as e:
            print(f"Error al guardar sesión: {e}")

    def show_success_and_redirect(self, user_data: dict):  # Redirige a la app principal
        # Ocultar indicador de carga
        self.show_loading(False)
        success_message = ft.Container(
            bgcolor=ft.Colors.with_opacity(0.9, ft.Colors.GREEN),
            border_radius=10,
            padding=15,
            width=350,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Icon(Icons.CHECK_CIRCLE, color="white", size=24),
                    ft.Text(
                        f"!Bienvenido, {user_data['name']}!",
                        color="white",
                        size=14,
                        weight="bold"
                    )
                ]
            )
        )

        # Reemplazar el mensaje de error por el mensaje de éxito en el panel derecho
        right_panel = self.content.controls[1]
        form_column = right_panel.content

        # Buscar y reemplazar el mensaje de error
        for i, control in enumerate(form_column.controls):
            if control == self.error_message:
                form_column.controls[i] = success_message
                break

        # Actualizar la página y navegar a la vista principal
        self.page.update()
        self.page.go("/main")

#ft.app(target=lambda page: UILogin(page), assets_dir="assets")
