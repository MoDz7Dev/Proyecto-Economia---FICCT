import flet as ft
import config as cfg
import diccionario as db

# Mapeo de roles a nombres en español para los filtros
ROLE_NAMES = {
    "admin": "Gerente",
    "supervisor": "Subgerente",
    "warehouse_manager": "Jefe de Almacén",
    "accountant": "Contador",
    "inventory_staff": "Encargado de Inventario",
    "cashier": "Cajero",
    "stock_clerk": "Personal de Reposición"
}

class EmployeeCard(ft.Container):
    """
    Tarjeta que muestra información básica de un empleado.
    Al hacer click en "Ver Detalles", muestra la información completa en el panel derecho.
    """
    def __init__(self, employee: dict, on_detail_click=None):
        """
        Args:
            employee (dict): Diccionario con los datos del empleado
            on_detail_click (callable): Función que se ejecuta al hacer click en "Ver Detalles"
        """
        self.employee = employee
        self.on_detail_click = on_detail_click
        super().__init__()

        # Construcción del contenedor
        self.content = self.build_content()

        # Estilos generales de la tarjeta
        self.width = 250
        self.bgcolor = cfg.CONTAINER_COLOR
        self.padding = 12  # Padding reducido para dar más espacio al contenido
        self.border_radius = 10
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))
        self.ink = True  # Efecto de onda al hacer click
        # No establecemos altura fija, dejamos que se ajuste al contenido

    def build_content(self):
        """
        Construye el contenido de la tarjeta del empleado
        """
        # Avatar del empleado (usamos las iniciales si no hay imagen)
        # Avatar un poco más pequeño para ahorrar espacio
        avatar = ft.CircleAvatar(
            content=ft.Text(
                self.employee['name'][0].upper(),
                color=ft.Colors.WHITE,
                size=22,
                weight=ft.FontWeight.BOLD
            ),
            radius=35,  # Radio reducido de 40 a 35
            bgcolor=cfg.COLOR_PURPLE,
        )

        # Nombre y CI del empleado
        name_text = ft.Text(
            value=self.employee['name'],
            color="white",
            weight=ft.FontWeight.BOLD,
            size=15,  # Tamaño ligeramente reducido
            text_align=ft.TextAlign.CENTER,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        ci_text = ft.Text(
            value=f"CI: {self.employee['ci']}",
            color=ft.Colors.GREY_400,
            size=11,  # Tamaño ligeramente reducido
            text_align=ft.TextAlign.CENTER,
        )

        # Rol del empleado
        role_name = ROLE_NAMES.get(self.employee['role'], self.employee['role'])
        role_text = ft.Container(
            content=ft.Text(
                value=role_name,
                color="white",
                size=12,
                weight=ft.FontWeight.W_500,
            ),
            bgcolor=cfg.COLOR_BLUE,
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=5,
        )

        # Departamento - más compacto
        dept_text = ft.Text(
            value=f"📁 {self.employee['department']}",
            color=ft.Colors.GREY_300,
            size=10,  # Tamaño reducido
            text_align=ft.TextAlign.CENTER,
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        # Estado (activo/inactivo)
        status_color = ft.Colors.GREEN if self.employee['status'] == "active" else ft.Colors.RED
        status_text = ft.Row(
            controls=[
                ft.Container(
                    width=8,
                    height=8,
                    bgcolor=status_color,
                    border_radius=4,
                ),
                ft.Text(
                    value=self.employee['status'].capitalize(),
                    color=status_color,
                    size=11,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

        # Botón "Ver Detalles" - optimizado para siempre ser visible
        detail_button = ft.ElevatedButton(
            text="Ver Detalles",
            icon=ft.Icons.INFO_OUTLINE,
            bgcolor=cfg.COLOR_PURPLE,
            color="white",
            width=200,
            height=36,
            on_click=lambda e: self.handle_detail_click(),
        )

        # Construir la estructura de la tarjeta
        return ft.Column(
            controls=[
                # Avatar centrado
                ft.Container(
                    content=avatar,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=8),  # Espaciado reducido
                # Nombre
                name_text,
                # CI
                ci_text,
                ft.Container(height=6),  # Espaciado reducido
                # Rol
                ft.Container(
                    content=role_text,
                    alignment=ft.alignment.center,
                ),
                ft.Container(height=6),  # Espaciado reducido
                # Departamento
                dept_text,
                ft.Container(height=4),  # Espaciado reducido
                # Estado
                status_text,
                ft.Container(height=8),  # Espaciado antes del botón
                # Botón Ver Detalles - siempre visible en la parte inferior
                # Usamos un Container con padding mínimo para asegurar visibilidad
                ft.Container(
                    content=detail_button,
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=4, bottom=2),  # Padding mínimo
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            expand=False,  # No expandir para que el contenido determine la altura
            tight=True,  # Compactar el contenido
        )

    def handle_detail_click(self):
        """
        Maneja el evento de click en el botón "Ver Detalles"
        """
        if self.on_detail_click:
            self.on_detail_click(self.employee)


class EmployeeSectionLeft(ft.Container):
    """
    Panel izquierdo: Contiene la barra de filtros y las tarjetas de empleados.
    """
    def __init__(self, on_employee_select=None):
        """
        Args:
            on_employee_select (callable): Función que se ejecuta cuando se selecciona un empleado
        """
        self.on_employee_select = on_employee_select
        self.all_employees = db.staff_users.copy()  # Lista completa de empleados
        self.filtered_employees = self.all_employees.copy()  # Empleados filtrados
        self.current_filter = "all"  # Filtro actual
        
        # Referencias para actualizar la UI
        self.employee_grid_ref = ft.Ref[ft.GridView]()
        self.count_text_ref = ft.Ref[ft.Text]()
        self.filter_buttons = {}  # Diccionario para almacenar referencias a los botones de filtro
        
        super().__init__()

        # Construcción del contenedor
        self.content = self.build_content()

        # Estilos generales del contenedor
        self.expand = True
        self.bgcolor = cfg.CONTAINER_COLOR
        self.padding = 15
        self.border_radius = 10
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))

    def filters_bar(self):
        """
        Construye la barra de filtros horizontal con botones para cada rol
        """
        # Botón "Añadir Usuario"
        add_button = ft.ElevatedButton(
            text="Añadir Usuario",
            icon=ft.Icons.ADD,
            bgcolor=cfg.COLOR_BLUE,
            color="white",
            height=40,
            on_click=lambda e: print("Añadir nuevo usuario"),
        )

        # Lista de filtros: Todos + cada rol
        filter_options = [("all", "Todos")] + list(ROLE_NAMES.items())
        
        # Crear botones de filtro
        filter_buttons_row = []
        for role_key, role_name in filter_options:
            btn_ref = ft.Ref[ft.ElevatedButton]()
            is_selected = (role_key == "all")
            
            btn = ft.ElevatedButton(
                text=role_name,
                bgcolor=cfg.COLOR_PURPLE if is_selected else cfg.BG_COLOR,
                color="white",
                height=35,
                on_click=lambda e, rk=role_key: self.filter_by_role(rk),
            )
            
            filter_buttons_row.append(btn)
            self.filter_buttons[role_key] = btn_ref
            btn_ref.current = btn

        # Texto con contador de empleados
        count_text = ft.Text(
            ref=self.count_text_ref,
            value=f"Cantidad de empleados: {len(self.filtered_employees)}",
            color="white",
            size=14,
            weight=ft.FontWeight.W_500,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    # Botón Añadir Usuario
                    add_button,
                    ft.Container(height=10),
                    # Botones de filtro en una fila horizontal con scroll
                    ft.Container(
                        content=ft.Row(
                            controls=filter_buttons_row,
                            scroll=ft.ScrollMode.ADAPTIVE,
                            spacing=8,
                        ),
                        height=45,
                    ),
                    ft.Container(height=8),
                    # Contador de empleados
                    count_text,
                    ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                ],
                spacing=0,
            ),
            padding=10,
        )

    def filter_by_role(self, role_key: str):
        """
        Filtra los empleados según el rol seleccionado
        
        Args:
            role_key (str): Clave del rol para filtrar ('all' para todos)
        """
        self.current_filter = role_key
        
        # Filtrar empleados
        if role_key == "all":
            self.filtered_employees = self.all_employees.copy()
        else:
            self.filtered_employees = [
                emp for emp in self.all_employees 
                if emp['role'] == role_key
            ]
        
        # Actualizar colores de los botones
        for key, btn_ref in self.filter_buttons.items():
            if btn_ref.current:
                btn_ref.current.bgcolor = cfg.COLOR_PURPLE if key == role_key else cfg.BG_COLOR
        
        # Actualizar la UI
        self.update_employee_grid()
        self.update_count()

    def update_employee_grid(self):
        """
        Actualiza el grid de tarjetas de empleados
        """
        if self.employee_grid_ref.current:
            # Limpiar tarjetas existentes
            self.employee_grid_ref.current.controls.clear()
            
            # Crear nuevas tarjetas con los empleados filtrados
            for employee in self.filtered_employees:
                card = EmployeeCard(
                    employee=employee,
                    on_detail_click=self.handle_employee_select
                )
                self.employee_grid_ref.current.controls.append(card)
            
            # Actualizar la página
            self.employee_grid_ref.current.update()

    def update_count(self):
        """
        Actualiza el contador de empleados
        """
        if self.count_text_ref.current:
            self.count_text_ref.current.value = f"Cantidad de empleados: {len(self.filtered_employees)}"
            self.count_text_ref.current.update()

    def handle_employee_select(self, employee: dict):
        """
        Maneja la selección de un empleado (click en "Ver Detalles")
        
        Args:
            employee (dict): Datos del empleado seleccionado
        """
        if self.on_employee_select:
            self.on_employee_select(employee)

    def build_content(self):
        """
        Construye el contenido completo del panel izquierdo
        """
        # Crear tarjetas de empleados
        employee_cards = []
        for employee in self.filtered_employees:
            card = EmployeeCard(
                employee=employee,
                on_detail_click=self.handle_employee_select
            )
            employee_cards.append(card)

        # GridView para mostrar las tarjetas (4 por fila)
        employee_grid = ft.GridView(
            ref=self.employee_grid_ref,
            controls=employee_cards,
            runs_count=4,  # 4 columnas (4 tarjetas por fila)
            max_extent=250,  # Ancho máximo de cada tarjeta
            child_aspect_ratio=0.75,  # Relación alto/ancho ajustada (más altura para que quepa el botón)
            spacing=15,  # Espaciado entre tarjetas
            run_spacing=15,  # Espaciado entre filas
            expand=True,
        )

        return ft.Column(
            controls=[
                # Barra de filtros
                self.filters_bar(),
                ft.Container(height=10),
                # Grid de tarjetas de empleados
                ft.Container(
                    content=employee_grid,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )


class EmployeeSectionRight(ft.Container):
    """
    Panel derecho: Muestra los detalles completos del empleado seleccionado.
    """
    def __init__(self):
        super().__init__()

        # Empleado seleccionado (inicialmente None)
        self.selected_employee = None

        # Construcción del contenedor inicial (vacíos)
        self.content = self.build_empty_content()

        # Estilos generales del contenedor
        self.width = 350
        self.expand = False
        self.bgcolor = cfg.CONTAINER_COLOR
        self.padding = 20
        self.border_radius = 10
        self.border = ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE))

    def build_empty_content(self):
        """
        Construye el contenido cuando no hay empleado seleccionado
        """
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(
                                ft.Icons.PERSON_OUTLINE,
                                size=80,
                                color=ft.Colors.GREY_600,
                            ),
                            ft.Text(
                                "Selecciona un empleado",
                                size=18,
                                color=ft.Colors.GREY_400,
                                weight=ft.FontWeight.W_500,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Haz click en 'Ver Detalles' en una tarjeta para ver la información completa",
                                size=12,
                                color=ft.Colors.GREY_500,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )

    def build_employee_detail(self, employee: dict):
        """
        Construye el contenido con los detalles del empleado seleccionado
        
        Args:
            employee (dict): Datos del empleado
        """
        # Avatar grande del empleado
        avatar = ft.CircleAvatar(
            content=ft.Text(
                employee['name'][0].upper(),
                color=ft.Colors.WHITE,
                size=50,
                weight=ft.FontWeight.BOLD
            ),
            radius=60,
            bgcolor=cfg.COLOR_PURPLE,
        )

        # Nombre completo
        name_text = ft.Text(
            value=employee['name'],
            color="white",
            size=22,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        # CI
        ci_text = ft.Text(
            value=f"CI: {employee['ci']}",
            color=ft.Colors.GREY_300,
            size=14,
            text_align=ft.TextAlign.CENTER,
        )

        # Función auxiliar para crear una fila de información
        def create_info_row(icon, label, value, color=None):
            """Crea una fila con icono, etiqueta y valor"""
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icon, color=color or cfg.COLOR_BLUE, size=20),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    label,
                                    size=11,
                                    color=ft.Colors.GREY_400,
                                ),
                                ft.Text(
                                    str(value),
                                    size=14,
                                    color="white",
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(vertical=8),
            )

        # Información detallada del empleado
        role_name = ROLE_NAMES.get(employee['role'], employee['role'])
        
        info_section = ft.Column(
            controls=[
                ft.Container(height=20),
                # Rol
                create_info_row(
                    ft.Icons.WORK,
                    "Rol",
                    role_name,
                    cfg.COLOR_PURPLE
                ),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                # Departamento
                create_info_row(
                    ft.Icons.BUSINESS,
                    "Departamento",
                    employee['department']
                ),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                # Email
                create_info_row(
                    ft.Icons.EMAIL,
                    "Email",
                    employee['email']
                ),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                # Contacto
                create_info_row(
                    ft.Icons.PHONE,
                    "Teléfono",
                    employee['contact']
                ),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                # Fecha de nacimiento
                create_info_row(
                    ft.Icons.CALENDAR_TODAY,
                    "Fecha de Nacimiento",
                    employee.get('date of birth', 'N/A')
                ),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                # Domicilio
                create_info_row(
                    ft.Icons.HOME,
                    "Domicilio",
                    employee.get('domicile', 'N/A')
                ),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                # Estado
                create_info_row(
                    ft.Icons.CHECK_CIRCLE if employee['status'] == "active" else ft.Icons.CANCEL,
                    "Estado",
                    employee['status'].capitalize(),
                    ft.Colors.GREEN if employee['status'] == "active" else ft.Colors.RED
                ),
            ],
            spacing=0,
        )

        # Botones de acción (opcionales)
        action_buttons = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="Editar",
                    icon=ft.Icons.EDIT,
                    bgcolor=cfg.COLOR_BLUE,
                    color="white",
                    expand=True,
                    on_click=lambda e: print(f"Editar empleado: {employee['name']}"),
                ),
                ft.ElevatedButton(
                    text="Eliminar",
                    icon=ft.Icons.DELETE,
                    bgcolor=ft.Colors.RED_700,
                    color="white",
                    expand=True,
                    on_click=lambda e: print(f"Eliminar empleado: {employee['name']}"),
                ),
            ],
            spacing=10,
        )

        return ft.Column(
            controls=[
                # Avatar y nombre
                ft.Container(
                    content=ft.Column(
                        controls=[
                            avatar,
                            ft.Container(height=15),
                            name_text,
                            ci_text,
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    alignment=ft.alignment.center,
                ),
                # Información detallada
                info_section,
                ft.Container(height=20),
                # Botones de acción
                action_buttons,
            ],
            spacing=0,
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True,
        )

    def show_employee(self, employee: dict):
        """
        Muestra los detalles de un empleado en el panel derecho
        
        Args:
            employee (dict): Datos del empleado a mostrar
        """
        self.selected_employee = employee
        self.content = self.build_employee_detail(employee)
        self.update()
