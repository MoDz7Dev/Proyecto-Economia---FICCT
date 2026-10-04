import flet as ft


class BuscarSection(ft.Container):
    """
    Módulo de búsqueda simple con filtros y resultados simulados.
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

        # Datos simulados para mostrar en el buscador
        self.items = [
            {"sku": "A-1001", "nombre": "Leche Entera 1L", "categoria": "Lácteos", "stock": 120, "estado": "Activo"},
            {"sku": "A-1020", "nombre": "Yogurt Durazno 1L", "categoria": "Lácteos", "stock": 45, "estado": "Activo"},
            {"sku": "B-2005", "nombre": "Arroz Premium 5kg", "categoria": "Granos", "stock": 80, "estado": "Activo"},
            {"sku": "B-2010", "nombre": "Quinua Orgánica 1kg", "categoria": "Granos", "stock": 18, "estado": "Bajo stock"},
            {"sku": "C-3010", "nombre": "Detergente Líquido 2L", "categoria": "Limpieza", "stock": 60, "estado": "Activo"},
            {"sku": "C-3020", "nombre": "Cloro Concentrado 1L", "categoria": "Limpieza", "stock": 25, "estado": "Bajo stock"},
            {"sku": "D-4001", "nombre": "Manzana Roja Kg", "categoria": "Frutas", "stock": 15, "estado": "Bajo stock"},
            {"sku": "D-4010", "nombre": "Banana Plátano Kg", "categoria": "Frutas", "stock": 95, "estado": "Activo"},
            {"sku": "E-5010", "nombre": "Filete de Pollo Kg", "categoria": "Carnes", "stock": 32, "estado": "Activo"},
            {"sku": "E-5020", "nombre": "Carne Molida Kg", "categoria": "Carnes", "stock": 10, "estado": "Bajo stock"},
        ]

        # Controles de filtro
        self.search_field = ft.TextField(
            hint_text="Buscar por nombre, SKU o categoría",
            prefix_icon=ft.Icons.SEARCH,
            border_radius=12,
            border_color="transparent",
            bgcolor=self.bg_color,
            color="white",
            hint_style=ft.TextStyle(color=ft.Colors.GREY),
            on_change=self._on_filter_change,
        )
        self.category_filter = ft.Dropdown(
            hint_text="Categoría",
            options=[ft.dropdown.Option("Todas")] + [
                ft.dropdown.Option(cat) for cat in sorted({item["categoria"] for item in self.items})
            ],
            value="Todas",
            bgcolor=self.bg_color,
            color="white",
            border_radius=8,
            border_color="transparent",
            on_change=self._on_filter_change,
        )
        self.status_filter = ft.Dropdown(
            hint_text="Estado",
            options=[ft.dropdown.Option("Todos"), ft.dropdown.Option("Activo"), ft.dropdown.Option("Bajo stock")],
            value="Todos",
            bgcolor=self.bg_color,
            color="white",
            border_radius=8,
            border_color="transparent",
            on_change=self._on_filter_change,
        )

        # Tabla de resultados
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("SKU", color="white")),
                ft.DataColumn(ft.Text("Nombre", color="white")),
                ft.DataColumn(ft.Text("Categoría", color="white")),
                ft.DataColumn(ft.Text("Stock", color="white")),
                ft.DataColumn(ft.Text("Estado", color="white")),
            ],
            rows=[],
            heading_row_color=ft.Colors.with_opacity(0.08, "white"),
            divider_thickness=0,
            data_row_color={"hovered": ft.Colors.with_opacity(0.05, "white")},
        )

        # Construimos la interfaz principal
        self.content = ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Buscador de productos", size=22, weight="bold", color="white"),
                self._build_filters(),
                ft.Container(
                    bgcolor=self.card_color,
                    padding=12,
                    border_radius=12,
                    content=self.table,
                ),
            ],
        )

        # Primera carga de datos (sin llamar update, solo construimos las filas)
        self._build_initial_rows()

    # --- UI helpers ---
    def _build_filters(self) -> ft.Container:
        """Construye la fila de filtros con buscador y combos."""
        return ft.Container(
            bgcolor=self.card_color,
            border_radius=12,
            padding=12,
            content=ft.Row(
                controls=[
                    ft.Container(expand=True, content=self.search_field),
                    ft.Container(width=160, content=self.category_filter),
                    ft.Container(width=140, content=self.status_filter),
                ],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _on_filter_change(self, e):
        """Se dispara cuando cambia el texto o los combos para filtrar la tabla."""
        self._refresh_table()

    def _build_initial_rows(self):
        """Construye las filas iniciales sin llamar a update (para usar en __init__)."""
        query = (self.search_field.value or "").lower().strip()
        category = self.category_filter.value or "Todas"
        status = self.status_filter.value or "Todos"

        filtered = []
        for item in self.items:
            # Filtro de texto contra varias columnas
            text_match = (
                query in item["sku"].lower()
                or query in item["nombre"].lower()
                or query in item["categoria"].lower()
            )
            # Filtro de categoría
            category_match = category == "Todas" or item["categoria"] == category
            # Filtro de estado
            status_match = status == "Todos" or item["estado"] == status

            if text_match and category_match and status_match:
                filtered.append(item)

        # Reconstruimos filas sin llamar a update
        self.table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["sku"], color="white")),
                    ft.DataCell(ft.Text(item["nombre"], color="white")),
                    ft.DataCell(ft.Text(item["categoria"], color="white")),
                    ft.DataCell(ft.Text(str(item["stock"]), color=self.accent_alt if item["stock"] > 30 else self.card_accent_2)),
                    ft.DataCell(self._status_chip(item["estado"])),
                ]
            )
            for item in filtered
        ]

    def _refresh_table(self):
        """Filtra los datos y reconstruye las filas de la tabla."""
        query = (self.search_field.value or "").lower().strip()
        category = self.category_filter.value or "Todas"
        status = self.status_filter.value or "Todos"

        filtered = []
        for item in self.items:
            # Filtro de texto contra varias columnas
            text_match = (
                query in item["sku"].lower()
                or query in item["nombre"].lower()
                or query in item["categoria"].lower()
            )
            # Filtro de categoría
            category_match = category == "Todas" or item["categoria"] == category
            # Filtro de estado
            status_match = status == "Todos" or item["estado"] == status

            if text_match and category_match and status_match:
                filtered.append(item)

        # Reconstruimos filas
        self.table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["sku"], color="white")),
                    ft.DataCell(ft.Text(item["nombre"], color="white")),
                    ft.DataCell(ft.Text(item["categoria"], color="white")),
                    ft.DataCell(ft.Text(str(item["stock"]), color=self.accent_alt if item["stock"] > 30 else self.card_accent_2)),
                    ft.DataCell(self._status_chip(item["estado"])),
                ]
            )
            for item in filtered
        ]
        # Solo actualizamos si el control ya está en la página
        if self.table.page is not None:
            self.table.update()
            self.page.update()

    def _status_chip(self, status: str) -> ft.Container:
        """Etiqueta coloreada para el estado del producto."""
        color_map = {
            "Activo": self.card_accent_1,
            "Bajo stock": self.card_accent_2,
        }
        return ft.Container(
            bgcolor=ft.Colors.with_opacity(0.15, color_map.get(status, "white")),
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            border_radius=20,
            content=ft.Text(status, color=color_map.get(status, "white"), size=12, weight="bold"),
        )

