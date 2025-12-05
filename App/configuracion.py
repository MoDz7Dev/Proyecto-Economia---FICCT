import flet as ft


class ConfiguracionSection(ft.Container):
    """
    Módulo de configuración con diferentes secciones para personalizar la aplicación.
    Incluye: Perfil de usuario, Preferencias, Empresa, Seguridad y Notificaciones.
    """

    def __init__(
        self,
        page: ft.Page,
        bg_color: str,
        card_color: str,
        accent: str,
        accent_alt: str,
        card_accent_1: str,
        card_accent_2: str,
    ):
        super().__init__(expand=True, padding=15)

        self.page = page
        self.bg_color = bg_color
        self.card_color = card_color
        self.accent = accent
        self.accent_alt = accent_alt
        self.card_accent_1 = card_accent_1
        self.card_accent_2 = card_accent_2

        # Datos simulados de configuración
        self.user_data = {
            "nombre": "Juan Pérez",
            "email": "juan.perez@hipermaxi.com",
            "telefono": "+591 70012345",
            "cargo": "Administrador",
        }

        self.app_preferences = {
            "idioma": "Español",
            "tema": "Oscuro",
            "notificaciones_email": True,
            "notificaciones_push": True,
            "auto_backup": True,
        }

        self.company_data = {
            "nombre": "Hipermaxi Las Brisas S.A.",
            "nit": "1028627025",
            "direccion": "Avenida Banzer, 4to. Anillo",
            "telefono": "+591 3 3456789",
            "email": "info@hipermaxi.com",
        }

        # Controles de formulario
        self.name_field = ft.TextField(
            label="Nombre completo",
            value=self.user_data["nombre"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.email_field = ft.TextField(
            label="Correo electrónico",
            value=self.user_data["email"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.phone_field = ft.TextField(
            label="Teléfono",
            value=self.user_data["telefono"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.position_field = ft.TextField(
            label="Cargo",
            value=self.user_data["cargo"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
            read_only=True,
        )

        # Dropdowns de preferencias
        self.language_dropdown = ft.Dropdown(
            label="Idioma",
            value=self.app_preferences["idioma"],
            options=[
                ft.dropdown.Option("Español"),
                ft.dropdown.Option("English"),
                ft.dropdown.Option("Português"),
            ],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.theme_dropdown = ft.Dropdown(
            label="Tema",
            value=self.app_preferences["tema"],
            options=[
                ft.dropdown.Option("Oscuro"),
                ft.dropdown.Option("Claro"),
                ft.dropdown.Option("Automático"),
            ],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )

        # Switches de preferencias
        self.email_notif_switch = ft.Switch(
            value=self.app_preferences["notificaciones_email"],
            label="Notificaciones por email",
            active_color=self.accent,
        )
        self.push_notif_switch = ft.Switch(
            value=self.app_preferences["notificaciones_push"],
            label="Notificaciones push",
            active_color=self.accent,
        )
        self.backup_switch = ft.Switch(
            value=self.app_preferences["auto_backup"],
            label="Backup automático",
            active_color=self.accent,
        )

        # Campos de empresa
        self.company_name_field = ft.TextField(
            label="Nombre de la empresa",
            value=self.company_data["nombre"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.nit_field = ft.TextField(
            label="NIT",
            value=self.company_data["nit"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.address_field = ft.TextField(
            label="Dirección",
            value=self.company_data["direccion"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
            multiline=True,
            min_lines=2,
        )
        self.company_phone_field = ft.TextField(
            label="Teléfono",
            value=self.company_data["telefono"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.company_email_field = ft.TextField(
            label="Email",
            value=self.company_data["email"],
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )

        # Controles de seguridad
        self.current_password_field = ft.TextField(
            label="Contraseña actual",
            password=True,
            can_reveal_password=True,
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.new_password_field = ft.TextField(
            label="Nueva contraseña",
            password=True,
            can_reveal_password=True,
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )
        self.confirm_password_field = ft.TextField(
            label="Confirmar nueva contraseña",
            password=True,
            can_reveal_password=True,
            bgcolor=self.bg_color,
            color="white",
            border_color="transparent",
            border_radius=8,
        )

        # Construimos la interfaz con tabs
        self.content = ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Configuración", size=22, weight="bold", color="white"),
                ft.Tabs(
                    selected_index=0,
                    indicator_color=self.accent,
                    label_color="white",
                    unselected_label_color=ft.Colors.GREY,
                    tabs=[
                        ft.Tab(
                            text="Perfil",
                            icon=ft.Icons.PERSON,
                            content=self._build_profile_tab(),
                        ),
                        ft.Tab(
                            text="Preferencias",
                            icon=ft.Icons.SETTINGS,
                            content=self._build_preferences_tab(),
                        ),
                        ft.Tab(
                            text="Empresa",
                            icon=ft.Icons.BUSINESS,
                            content=self._build_company_tab(),
                        ),
                        ft.Tab(
                            text="Seguridad",
                            icon=ft.Icons.LOCK,
                            content=self._build_security_tab(),
                        ),
                        ft.Tab(
                            text="Notificaciones",
                            icon=ft.Icons.NOTIFICATIONS,
                            content=self._build_notifications_tab(),
                        ),
                    ],
                    expand=True,
                ),
            ],
        )

    def _build_profile_tab(self) -> ft.Container:
        """Construye la pestaña de perfil de usuario."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Información del perfil", size=18, weight="bold", color="white"),
                    ft.Container(
                        bgcolor=self.card_color,
                        padding=20,
                        border_radius=12,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            width=100,
                                            height=100,
                                            border_radius=50,
                                            bgcolor=self.accent,
                                            content=ft.Icon(
                                                ft.Icons.PERSON,
                                                size=50,
                                                color="white",
                                            ),
                                            alignment=ft.alignment.center,
                                        ),
                                        ft.Column(
                                            expand=True,
                                            spacing=5,
                                            controls=[
                                                ft.Text(
                                                    self.user_data["nombre"],
                                                    size=20,
                                                    weight="bold",
                                                    color="white",
                                                ),
                                                ft.Text(
                                                    self.user_data["cargo"],
                                                    size=14,
                                                    color=ft.Colors.GREY,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                ft.Divider(color=ft.Colors.with_opacity(0.2, "white")),
                                self.name_field,
                                self.email_field,
                                self.phone_field,
                                self.position_field,
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Guardar cambios",
                                            bgcolor=self.accent,
                                            color="white",
                                            on_click=self._save_profile,
                                        ),
                                        ft.OutlinedButton(
                                            "Cancelar",
                                            style=ft.ButtonStyle(color="white"),
                                            on_click=self._cancel_profile,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _build_preferences_tab(self) -> ft.Container:
        """Construye la pestaña de preferencias de la aplicación."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Preferencias de la aplicación", size=18, weight="bold", color="white"),
                    ft.Container(
                        bgcolor=self.card_color,
                        padding=20,
                        border_radius=12,
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Text("Apariencia", size=16, weight="bold", color="white"),
                                self.language_dropdown,
                                self.theme_dropdown,
                                ft.Divider(color=ft.Colors.with_opacity(0.2, "white")),
                                ft.Text("General", size=16, weight="bold", color="white"),
                                self.email_notif_switch,
                                self.push_notif_switch,
                                self.backup_switch,
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Guardar preferencias",
                                            bgcolor=self.accent,
                                            color="white",
                                            on_click=self._save_preferences,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _build_company_tab(self) -> ft.Container:
        """Construye la pestaña de información de la empresa."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Información de la empresa", size=18, weight="bold", color="white"),
                    ft.Container(
                        bgcolor=self.card_color,
                        padding=20,
                        border_radius=12,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                self.company_name_field,
                                self.nit_field,
                                self.address_field,
                                self.company_phone_field,
                                self.company_email_field,
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Guardar información",
                                            bgcolor=self.accent,
                                            color="white",
                                            on_click=self._save_company,
                                        ),
                                        ft.OutlinedButton(
                                            "Restaurar valores",
                                            style=ft.ButtonStyle(color="white"),
                                            on_click=self._reset_company,
                                        ),
                                    ],
                                    spacing=10,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _build_security_tab(self) -> ft.Container:
        """Construye la pestaña de configuración de seguridad."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Seguridad y contraseña", size=18, weight="bold", color="white"),
                    ft.Container(
                        bgcolor=self.card_color,
                        padding=20,
                        border_radius=12,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                ft.Text(
                                    "Cambiar contraseña",
                                    size=16,
                                    weight="bold",
                                    color="white",
                                ),
                                self.current_password_field,
                                self.new_password_field,
                                self.confirm_password_field,
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Cambiar contraseña",
                                            bgcolor=self.card_accent_1,
                                            color="white",
                                            on_click=self._change_password,
                                        ),
                                    ],
                                ),
                                ft.Divider(color=ft.Colors.with_opacity(0.2, "white")),
                                ft.Text(
                                    "Sesiones activas",
                                    size=16,
                                    weight="bold",
                                    color="white",
                                ),
                                ft.Container(
                                    bgcolor=self.bg_color,
                                    padding=15,
                                    border_radius=8,
                                    content=ft.Column(
                                        spacing=10,
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.COMPUTER, color="white"),
                                                    ft.Column(
                                                        expand=True,
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text(
                                                                "Windows - Chrome",
                                                                color="white",
                                                                weight="bold",
                                                            ),
                                                            ft.Text(
                                                                "Última actividad: hace 5 minutos",
                                                                size=12,
                                                                color=ft.Colors.GREY,
                                                            ),
                                                        ],
                                                    ),
                                                    ft.IconButton(
                                                        ft.Icons.LOGOUT,
                                                        tooltip="Cerrar sesión",
                                                        icon_color=self.card_accent_1,
                                                        on_click=self._close_session,
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def _build_notifications_tab(self) -> ft.Container:
        """Construye la pestaña de configuración de notificaciones."""
        return ft.Container(
            padding=20,
            content=ft.Column(
                spacing=15,
                controls=[
                    ft.Text("Configuración de notificaciones", size=18, weight="bold", color="white"),
                    ft.Container(
                        bgcolor=self.card_color,
                        padding=20,
                        border_radius=12,
                        content=ft.Column(
                            spacing=20,
                            controls=[
                                ft.Text("Tipos de notificaciones", size=16, weight="bold", color="white"),
                                ft.Switch(
                                    label="Ventas nuevas",
                                    value=True,
                                    active_color=self.accent,
                                ),
                                ft.Switch(
                                    label="Inventario bajo",
                                    value=True,
                                    active_color=self.accent,
                                ),
                                ft.Switch(
                                    label="Recordatorios de pago",
                                    value=True,
                                    active_color=self.accent,
                                ),
                                ft.Switch(
                                    label="Reportes diarios",
                                    value=False,
                                    active_color=self.accent,
                                ),
                                ft.Switch(
                                    label="Alertas de seguridad",
                                    value=True,
                                    active_color=self.accent,
                                ),
                                ft.Divider(color=ft.Colors.with_opacity(0.2, "white")),
                                ft.Text("Frecuencia", size=16, weight="bold", color="white"),
                                ft.Dropdown(
                                    label="Frecuencia de reportes",
                                    value="Diario",
                                    options=[
                                        ft.dropdown.Option("Diario"),
                                        ft.dropdown.Option("Semanal"),
                                        ft.dropdown.Option("Mensual"),
                                    ],
                                    bgcolor=self.bg_color,
                                    color="white",
                                    border_color="transparent",
                                    border_radius=8,
                                ),
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton(
                                            "Guardar configuración",
                                            bgcolor=self.accent,
                                            color="white",
                                            on_click=self._save_notifications,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    # --- Métodos de eventos ---
    def _save_profile(self, e):
        """Guarda los cambios del perfil."""
        self.user_data["nombre"] = self.name_field.value
        self.user_data["email"] = self.email_field.value
        self.user_data["telefono"] = self.phone_field.value
        self._show_snackbar("Perfil actualizado correctamente", self.accent)

    def _cancel_profile(self, e):
        """Cancela los cambios y restaura los valores originales."""
        self.name_field.value = self.user_data["nombre"]
        self.email_field.value = self.user_data["email"]
        self.phone_field.value = self.user_data["telefono"]
        self.page.update()
        self._show_snackbar("Cambios cancelados", ft.Colors.GREY)

    def _save_preferences(self, e):
        """Guarda las preferencias de la aplicación."""
        self.app_preferences["idioma"] = self.language_dropdown.value
        self.app_preferences["tema"] = self.theme_dropdown.value
        self.app_preferences["notificaciones_email"] = self.email_notif_switch.value
        self.app_preferences["notificaciones_push"] = self.push_notif_switch.value
        self.app_preferences["auto_backup"] = self.backup_switch.value
        self._show_snackbar("Preferencias guardadas correctamente", self.accent)

    def _save_company(self, e):
        """Guarda la información de la empresa."""
        self.company_data["nombre"] = self.company_name_field.value
        self.company_data["nit"] = self.nit_field.value
        self.company_data["direccion"] = self.address_field.value
        self.company_data["telefono"] = self.company_phone_field.value
        self.company_data["email"] = self.company_email_field.value
        self._show_snackbar("Información de empresa guardada", self.accent)

    def _reset_company(self, e):
        """Restaura los valores originales de la empresa."""
        self.company_name_field.value = self.company_data["nombre"]
        self.nit_field.value = self.company_data["nit"]
        self.address_field.value = self.company_data["direccion"]
        self.company_phone_field.value = self.company_data["telefono"]
        self.company_email_field.value = self.company_data["email"]
        self.page.update()
        self._show_snackbar("Valores restaurados", ft.Colors.GREY)

    def _change_password(self, e):
        """Cambia la contraseña del usuario."""
        if not self.current_password_field.value:
            self._show_snackbar("Ingrese su contraseña actual", self.card_accent_1)
            return
        if not self.new_password_field.value:
            self._show_snackbar("Ingrese una nueva contraseña", self.card_accent_1)
            return
        if self.new_password_field.value != self.confirm_password_field.value:
            self._show_snackbar("Las contraseñas no coinciden", self.card_accent_1)
            return
        if len(self.new_password_field.value) < 8:
            self._show_snackbar("La contraseña debe tener al menos 8 caracteres", self.card_accent_1)
            return

        # Simulación de cambio de contraseña
        self.current_password_field.value = ""
        self.new_password_field.value = ""
        self.confirm_password_field.value = ""
        self.page.update()
        self._show_snackbar("Contraseña cambiada exitosamente", self.accent)

    def _close_session(self, e):
        """Cierra una sesión activa."""
        self._show_snackbar("Sesión cerrada", self.card_accent_1)

    def _save_notifications(self, e):
        """Guarda la configuración de notificaciones."""
        self._show_snackbar("Configuración de notificaciones guardada", self.accent)

    def _show_snackbar(self, message: str, color: str):
        """Muestra un mensaje de confirmación."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color="white"),
            bgcolor=color,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()

