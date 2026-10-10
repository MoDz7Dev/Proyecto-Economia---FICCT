import flet as ft
from flet import Icons
import json
import requests

from src import config as cfg
from src.ui.components.product_card import ProductCard
from src.ui.components.category_bar import CategoryBar
from src.ui.components.shopping_cart import ShoppingCart
from src.ui.components import chart_style

def build_equilibrium_chart() -> ft.LineChart:
    """Grafica de equilibrio de mercado (Oferta / Demanda).

    Usa el estilo de "curvas luminosas" y rotula el final de cada curva con
    "Demanda" y "Oferta".
    """
    # Oferta: Qs = -20 + Px      Demanda: Qd = 100 - 2Px
    # Equilibrio: Pe = 40, Qe = 20
    supply_points = []
    demand_points = []

    for px in range(0, 70, 5):
        # Línea de Oferta (verde): Qs = -20 + Px
        qs = -20 + px
        if qs >= 0:
            supply_points.append(
                ft.LineChartDataPoint(px, qs, tooltip=f"Oferta - Px: {px} / Qx: {qs}")
            )

        # Línea de Demanda (cyan): Qd = 100 - 2Px
        qd = 100 - 2 * px
        if qd >= 0:
            demand_points.append(
                ft.LineChartDataPoint(px, qd, tooltip=f"Demanda - Px: {px} / Qx: {qd}")
            )

    def axis_labels():
        return [
            ft.ChartAxisLabel(value=v, label=ft.Text(str(v), color="white", size=10))
            for v in range(0, 71, 10)
        ]

    return ft.LineChart(
        interactive=True,
        bgcolor=chart_style.CHART_BG,
        tooltip_bgcolor=ft.Colors.with_opacity(0.92, chart_style.CHART_BG),
        tooltip_rounded_radius=8,
        tooltip_padding=8,
        point_line_start=0,
        point_line_end=70,
        data_series=[
            # Línea de Demanda (Dx) - Cyan con degradado
            ft.LineChartData(
                data_points=demand_points,
                color=chart_style.CYAN,
                stroke_width=3,
                stroke_cap_round=True,
                curved=True,
                shadow=chart_style.line_glow(chart_style.CYAN),
                point=chart_style.dot(chart_style.CYAN),
                selected_point=chart_style.glow_dot(chart_style.CYAN),
                below_line_gradient=chart_style.fill_gradient(chart_style.CYAN, 0.28),
            ),
            # Línea de Oferta (Sx) - Verde con degradado
            ft.LineChartData(
                data_points=supply_points,
                color=chart_style.GREEN,
                stroke_width=3,
                stroke_cap_round=True,
                curved=True,
                shadow=chart_style.line_glow(chart_style.GREEN),
                point=chart_style.dot(chart_style.GREEN),
                selected_point=chart_style.glow_dot(chart_style.GREEN),
                below_line_gradient=chart_style.fill_gradient(chart_style.GREEN, 0.28),
            ),
            # Punto de Equilibrio (luminoso)
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(40, 20, tooltip="Equilibrio - Pe: 40 / Qe: 20")
                ],
                color=chart_style.RED,
                stroke_width=0,
                point=chart_style.glow_dot(chart_style.RED, radius=4.5, halo=8),
                selected_point=chart_style.glow_dot(chart_style.RED, radius=4.5, halo=8),
            ),
        ],
        min_x=0, max_x=70,
        min_y=0, max_y=70,
        border=chart_style.border_axes(),
        horizontal_grid_lines=chart_style.grid_lines(interval=10),
        vertical_grid_lines=chart_style.grid_lines(interval=10),
        left_axis=ft.ChartAxis(
            title=ft.Text("Cantidad (Qx)", color="white", size=11, weight="bold"),
            title_size=30,
            labels_size=25,
            labels=axis_labels(),
        ),
        bottom_axis=ft.ChartAxis(
            title=ft.Text("Precio (Px)", color="white", size=11, weight="bold"),
            title_size=30,
            labels_size=25,
            labels=axis_labels(),
        ),
        # Etiquetas al final de cada curva
        right_axis=ft.ChartAxis(
            show_labels=True,
            labels_size=58,
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Text("Demanda", color=chart_style.CYAN, size=10, weight="bold"),
                ),
                ft.ChartAxisLabel(
                    value=45,
                    label=ft.Text("Oferta", color=chart_style.GREEN, size=10, weight="bold"),
                ),
            ],
        ),
    )


class InventorySection(ft.Container):
    """
    Sección completa de inventario con productos y carrito
    """
    def __init__(self, page: ft.Page):
        self.page = page
        super().__init__()
        
        self.category_bar = CategoryBar(on_category_change=self.filter_by_category)
        self.shopping_cart = ShoppingCart()
        self.products_grid_ref = ft.Ref[ft.GridView]()
        self.empty_state_ref = ft.Ref[ft.Container]()
        self.all_products = self.get_products()
        self.filtered_products = self.all_products.copy()
        
        self.content = self.build_content()
        
        self.expand = True
        self.margin = 5

    def get_products(self):
        try:
            response = requests.get("http://127.0.0.1:8000/")
            products = json.loads(response.text)
            print(f"✅ {len(products)} productos cargados")
            return products
        except Exception as e:
            print(f"❌ Error al obtener productos: {e}")
            return []

    def filter_by_category(self, category_id: str):
        if category_id == "all":
            self.filtered_products = self.all_products.copy()
        else:
            self.filtered_products = [
                p for p in self.all_products 
                if p.get('category', '').lower() == category_id.lower()
            ]
        
        print(f"🔍 Categoría: {category_id} - {len(self.filtered_products)} productos")
        self.update_products_grid()

    def update_products_grid(self):
        has_products = len(self.filtered_products) > 0

        if self.products_grid_ref.current:
            grid = self.products_grid_ref.current
            grid.controls.clear()

            for product in self.filtered_products:
                card = ProductCard(
                    product=product,
                    page=self.page,
                    on_add_to_cart=self.shopping_cart.add_product,
                    show_details_callback=self.show_product_details
                )
                grid.controls.append(card)

            grid.visible = has_products
            grid.update()

        if self.empty_state_ref.current:
            self.empty_state_ref.current.visible = not has_products
            self.empty_state_ref.current.update()

    def show_product_details(self, product: dict):
        """
        Muestra un AlertDialog con los detalles del producto
        """
        print(f"💫 Mostrando detalles: {product.get('name', 'Sin nombre')}")
        
        def close_dlg(e):
            dlg.open = False
            self.page.update()
            print("✅ Diálogo cerrado")
        
        def add_and_close(e):
            self.shopping_cart.add_product(product)
            dlg.open = False
            self.page.update()
            print(f"🛒 Producto agregado: {product.get('name')}")
        
        # Grafica de Equilibrio de Mercado (estilo curvas luminosas)
        chart = build_equilibrium_chart()
        
        # Crear el diálogo con nuevo diseño
        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=cfg.CONTAINER_COLOR,
            content=ft.Container(
                width=800,
                height=530,
                padding=5,
                content=ft.Column(
                    spacing=5,
                    controls=[
                        # Header con título y botón cerrar
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("Detalles del Producto", size=20, weight="bold", color="white"),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="white",
                                    icon_size=25,
                                    on_click=close_dlg
                                )
                            ]
                        ),
                        ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                        # Contenedor principal con 2 columnas
                        ft.Row(
                            spacing=15,
                            expand=True,
                            controls=[
                                # Columna izquierda: Imagen y detalles del producto
                                ft.Container(
                                    width=280,
                                    bgcolor=cfg.BG_COLOR,
                                    border_radius=10,
                                    padding=15,
                                    content=ft.Column(
                                        spacing=10,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            # Imagen del producto
                                            ft.Container(
                                                height=220,
                                                width=220,
                                                border=ft.border.all(2, ft.Colors.WHITE),
                                                border_radius=5,
                                                alignment=ft.alignment.center,
                                                content=ft.Image(
                                                    src=product.get('image', ''),
                                                    fit=ft.ImageFit.CONTAIN,
                                                    error_content=ft.Text("Imagen", size=40, color="white")
                                                )
                                            ),
                                            # Nombre del producto
                                            ft.Text(
                                                product.get('name', 'Sin nombre'),
                                                size=16,
                                                weight="bold",
                                                color="white",
                                                text_align=ft.TextAlign.CENTER
                                            ),
                                            ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                            # Precios
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Column(
                                                        spacing=2,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                        controls=[
                                                            ft.Text("Precio de Venta", size=12, color=ft.Colors.GREY_400),
                                                            ft.Text(f"Bs. {product.get('saleprice', '0.00')}", size=18, weight="bold", color="white")
                                                        ]
                                                    ),
                                                    ft.Column(
                                                        spacing=2,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                        controls=[
                                                            ft.Text("Precio de Compra", size=12, color=ft.Colors.GREY_400),
                                                            ft.Text(f"Bs. {product.get('purchaseprice', '0.00')}", size=18, weight="bold", color=cfg.COLOR_PURPLE)
                                                        ]
                                                    )
                                                ]
                                            ),
                                            ft.Divider(height=1, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                            # Detalles adicionales
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.CATEGORY, color=cfg.COLOR_PURPLE, size=20),
                                                    ft.Text(f"Categoría: {product.get('category', 'N/A')}", size=14, color="white")
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.INVENTORY_2, color=cfg.COLOR_PURPLE, size=20),
                                                    ft.Text(f"Stock: {product.get('stock', 'N/A')} unidades", size=14, color="white")
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(ft.Icons.USB, color=cfg.COLOR_PURPLE, size=20),
                                                    ft.Text(f"Código: {product.get('code', 'N/A')}", size=14, color="white")
                                                ]
                                            ),
                                        ]
                                    )
                                ),
                                # Columna derecha: Gráfica y contenedor de análisis
                                ft.Container(
                                    expand=True,
                                    content=ft.Column(
                                        spacing=10,
                                        controls=[
                                            # Gráfica de Equilibrio de Mercado
                                            ft.Container(
                                                height=240,
                                                bgcolor=cfg.BG_COLOR,
                                                border_radius=10,
                                                padding=15,
                                                content=ft.Column(
                                                    spacing=5,
                                                    controls=[
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                            controls=[
                                                                ft.Row(
                                                                    spacing=5,
                                                                    controls=[
                                                                        ft.Text("Equilibrio de Mercado ", size=14, weight="bold", color="white"),
                                                                        ft.Container(
                                                                            padding=5,
                                                                            content=ft.Row(
                                                                                spacing=3,
                                                                                controls=[
                                                                                    ft.Container(width=15, height=3, bgcolor=ft.Colors.CYAN, border_radius=2),
                                                                                    ft.Text("Demanda", size=10, color=ft.Colors.CYAN),
                                                                                ]
                                                                            )
                                                                        ),
                                                                        ft.Container(
                                                                            padding=5,
                                                                            content=ft.Row(
                                                                                spacing=3,
                                                                                controls=[
                                                                                    ft.Container(width=15, height=3, bgcolor=ft.Colors.GREEN, border_radius=2),
                                                                                    ft.Text("Oferta", size=10, color=ft.Colors.GREEN),
                                                                                ]
                                                                            )
                                                                        ),
                                                                    ]
                                                                ),
                                                                ft.IconButton(
                                                                    icon=ft.Icons.MORE_HORIZ,
                                                                    icon_color="white",
                                                                    icon_size=20
                                                                )
                                                            ]
                                                        ),
                                                        ft.Container(
                                                            expand=True,
                                                            content=chart
                                                        )
                                                    ]
                                                )
                                            ),
                                            # Contenedor de Información de Oferta-Demanda
                                            ft.Container(
                                                expand=True,
                                                bgcolor=cfg.BG_COLOR,
                                                border_radius=10,
                                                padding=15,
                                                content=ft.Column(
                                                    spacing=12,
                                                    controls=[
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.START,
                                                            controls=[
                                                                ft.Icon(ft.Icons.INSIGHTS, color=cfg.COLOR_PURPLE, size=24),
                                                                ft.Text("Análisis de Mercado", size=15, weight="bold", color="white")
                                                            ]
                                                        ),
                                                        ft.Divider(height=1, color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                                                        # Punto de Equilibrio
                                                        ft.Row(
                                                            spacing=8,
                                                            controls=[
                                                                ft.Container(
                                                                    width=8,
                                                                    height=8,
                                                                    bgcolor=ft.Colors.RED,
                                                                    border_radius=4
                                                                ),
                                                                ft.Column(
                                                                    spacing=2,
                                                                    controls=[
                                                                        ft.Text("Precio de Equilibrio (Pe)", size=11, color=ft.Colors.GREY_400),
                                                                        ft.Text("Bs. 40.00", size=14, weight="bold", color="white")
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        # Cantidad de Equilibrio
                                                        ft.Row(
                                                            spacing=8,
                                                            controls=[
                                                                ft.Container(
                                                                    width=8,
                                                                    height=8,
                                                                    bgcolor=ft.Colors.ORANGE,
                                                                    border_radius=4
                                                                ),
                                                                ft.Column(
                                                                    spacing=2,
                                                                    controls=[
                                                                        ft.Text("Cantidad de Equilibrio (Qe)", size=11, color=ft.Colors.GREY_400),
                                                                        ft.Text("20 unidades", size=14, weight="bold", color="white")
                                                                    ]
                                                                )
                                                            ]
                                                        ),
                                                        # Condiciones de Mercado
                                                        ft.Container(
                                                            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE),
                                                            border_radius=5,
                                                            padding=8,
                                                            content=ft.Column(
                                                                spacing=4,
                                                                controls=[
                                                                    ft.Row(
                                                                        controls=[
                                                                            ft.Icon(ft.Icons.ARROW_DOWNWARD, color=ft.Colors.CYAN, size=16),
                                                                            ft.Text("Exceso de Demanda: Px < Bs. 40", size=11, color=ft.Colors.CYAN)
                                                                        ]
                                                                    ),
                                                                    ft.Row(
                                                                        controls=[
                                                                            ft.Icon(ft.Icons.ARROW_UPWARD, color=ft.Colors.GREEN, size=16),
                                                                            ft.Text("Exceso de Oferta: Px > Bs. 40", size=11, color=ft.Colors.GREEN)
                                                                        ]
                                                                    ),
                                                                ]
                                                            )
                                                        ),
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        )
        
        # Asignar el diálogo ANTES de abrirlo
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
        print("✅ AlertDialog abierto en overlay")

    def build_content(self):
        product_cards = []
        for product in self.filtered_products:
            card = ProductCard(
                product=product,
                page=self.page,
                on_add_to_cart=self.shopping_cart.add_product,
                show_details_callback=self.show_product_details
            )
            product_cards.append(card)
        
        products_grid = ft.GridView(
            ref=self.products_grid_ref,
            controls=product_cards,
            runs_count=5,
            max_extent=200,
            child_aspect_ratio=0.8,
            spacing=5,
            run_spacing=5,
            expand=1,
        )
        
        empty_state = ft.Container(
            ref=self.empty_state_ref,
            expand=10,
            visible=False,
            alignment=ft.alignment.center,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Icon(ft.Icons.SEARCH_OFF, size=60, color=ft.Colors.with_opacity(0.6, ft.Colors.WHITE)),
                    ft.Text("No hay productos en esta categoría", color="white", size=16),
                ],
            ),
        )

        return ft.Row(
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            self.category_bar,
                            products_grid,
                            empty_state
                        ]
                    )
                ),
                self.shopping_cart,
            ]
        )
