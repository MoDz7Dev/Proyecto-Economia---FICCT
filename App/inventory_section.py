import flet as ft
from flet import Icons
import json
import requests
import config as cfg

class ProductCard(ft.Container):
    """
    Tarjeta que muestra información básica de un producto.
    Al hacer click en "Detalles", muestra la información completa en un diálogo.
    """
    def __init__(self, product: dict, page: ft.Page, on_add_to_cart=None, show_details_callback=None):
        """
        Args:
            product (dict): Diccionario con los datos del producto
            page (ft.Page): Referencia a la página principal
            on_add_to_cart (callable): Función que se ejecuta al agregar al carrito
            show_details_callback (callable): Callback para mostrar detalles
        """
        self.product = product
        self.page = page
        self.on_add_to_cart = on_add_to_cart
        self.show_details_callback = show_details_callback
        super().__init__()

        # Construcción del contenedor
        self.content = self.build_content()

        # Estilos generales de la tarjeta
        self.aspect_ratio = 1.5
        self.bgcolor = cfg.CONTAINER_COLOR
        self.border_radius = 10

    def build_content(self):
        """
        Construye el contenido de la tarjeta del producto
        """
        return ft.Column(
            controls=[
                ft.Container(
                    content=ft.Image(
                        self.product.get('image', ''), 
                        width=200,
                        fit=ft.ImageFit.COVER,
                        error_content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=100, color="white")
                    ), 
                    expand=1
                ),
                ft.Container(
                    padding=ft.padding.only(left=10, right=10, bottom=10), 
                    content=ft.Column(
                        controls=[
                            # Título del producto
                            ft.Text(
                                self.product.get('name', 'Sin nombre'), 
                                color="white", 
                                weight="bold",
                                size=15,
                                text_align=ft.TextAlign.CENTER,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS, 
                                expand=True, 
                            ),
                            # Precios
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        f"Bs.{self.product.get('saleprice', '0.00')}", 
                                        color="white",
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.Text(
                                        f"Bs.{self.product.get('purchaseprice', '0.00')}", 
                                        color=cfg.COLOR_PURPLE,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                ]
                            ),
                            # Botón
                            ft.FilledButton(
                                "Detalles", 
                                bgcolor=cfg.COLOR_PURPLE, 
                                expand=True,
                                width=130,
                                on_click=self.handle_details_click
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        height=121
                    )   
                )
            ]
        )

    def handle_details_click(self, e):
        """
        Maneja el clic en el botón de detalles
        """
        print(f"🖱️ CLICK DETECTADO en: {self.product.get('name', 'Sin nombre')}")
        if self.show_details_callback:
            print("✅ Ejecutando callback...")
            self.show_details_callback(self.product)
        else:
            print("❌ No hay callback configurado")


class CategoryBar(ft.Container):
    """
    Barra de navegación horizontal con categorías de productos
    """
    def __init__(self, on_category_change=None):
        self.on_category_change = on_category_change
        self.current_scroll_offset = 0
        self.category_list_ref = ft.Ref[ft.ListView]()
        
        super().__init__()
        
        self.content = self.build_content()
        
        self.bgcolor = cfg.CONTAINER_COLOR
        self.height = 50
        self.border_radius = 15
        self.padding = 5

    def build_content(self):
        categories = [
            ("all", Icons.ALL_INBOX, "Todo"),
            ("groceries", Icons.LOCAL_GROCERY_STORE, "Abarrotes"),
            ("beverages", Icons.LOCAL_BAR, "Bebidas"),
            ("meat", Icons.FASTFOOD, "Carnes"),
            ("frozen", Icons.AC_UNIT, "Congelados"),
            ("dairy", Icons.WATER_DROP, "Lácteos y Derivados"),
            ("bakery", Icons.BAKERY_DINING, "Panadería"),
            ("home_care", Icons.CLEANING_SERVICES, "Cuidado del Hogar"),
            ("personal_care", Icons.WASH, "Cuidado Personal"),
            ("toys", Icons.TOYS, "Juguetería"),
            ("pharmacy", Icons.LOCAL_HOSPITAL, "Farmacia"),
        ]
        
        category_buttons = []
        for cat_id, icon, name in categories:
            btn = ft.Container(
                padding=10,
                bgcolor=cfg.COLOR_NAVEGATION_BT,
                border_radius=15,
                on_click=lambda e, c=cat_id: self.handle_category_click(c),
                height=40,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(icon, color="white"),
                        ft.Text(name, color="white")
                    ]
                )
            )
            category_buttons.append(btn)
        
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=0,
            controls=[
                ft.IconButton(
                    Icons.ARROW_BACK_IOS, 
                    icon_color="white", 
                    on_click=lambda e: self.scroll_categories(-100),
                ),
                ft.Container(
                    expand=True,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=ft.ListView(
                        ref=self.category_list_ref,
                        horizontal=True,
                        spacing=5,
                        controls=category_buttons
                    )
                ),
                ft.IconButton(
                    Icons.ARROW_FORWARD_IOS, 
                    icon_color="white", 
                    on_click=lambda e: self.scroll_categories(100),
                ),
            ]
        )

    def scroll_categories(self, delta: int):
        category_list = self.category_list_ref.current
        
        if category_list:
            new_scroll = self.current_scroll_offset + delta
            
            if new_scroll < 0:
                new_scroll = 0
            
            category_list.scroll_to(offset=new_scroll, duration=300)
            self.current_scroll_offset = new_scroll
            self.update()

    def handle_category_click(self, category_id: str):
        if self.on_category_change:
            self.on_category_change(category_id)


class ShoppingCart(ft.Container):
    """
    Panel del carrito de compras en el lado derecho
    """
    def __init__(self):
        super().__init__()
        
        self.cart_items = []
        self.cart_list_ref = ft.Ref[ft.ListView]()
        self.total_text_ref = ft.Ref[ft.Text]()
        
        self.content = self.build_content()
        
        self.bgcolor = cfg.CONTAINER_COLOR
        self.width = 300
        self.border_radius = 15
        self.padding = 10

    def build_content(self):
        return ft.Column(
            controls=[
                ft.Text("Factura N°: 3798247731223", color=ft.Colors.GREY_400),
                ft.Divider(height=1),
                ft.Row(
                    controls=[
                        ft.Image(src="Hipermaxi_logo.png", width=120, height=60, fit=ft.ImageFit.COVER),
                        ft.Column(
                            controls=[
                                ft.Text("Hipermaxi", weight="bold", size=25, color="white"),
                                ft.Text("hipermaxi@gmail.com", color=ft.Colors.GREY_400)
                            ]
                        )
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Sucursal: Las Brisas", weight="bold", color=cfg.COLOR_PURPLE),
                        ft.Text("Orden #23440", weight="bold", color="white")
                    ],
                ),
                ft.Divider(height=1),
                ft.ListView(
                    ref=self.cart_list_ref,
                    expand=True,
                    controls=[
                        ft.Column([
                            ft.Row([
                                ft.Image("products/img16.png", width=50, height=50),
                                ft.Column([
                                    ft.Text("Cartulina Oficio", color="white"),
                                    ft.Text("Precio: Bs.38.00", color=cfg.COLOR_PURPLE)
                                ]),
                                ft.Text("Bs.114.00", color=cfg.COLOR_PURPLE, size=20, weight="bold")
                            ]),
                            ft.Row([
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.REMOVE, icon_color="white"),
                                    ft.Container(
                                        border_radius=3,
                                        width=40,
                                        height=25,
                                        bgcolor=cfg.BG_COLOR,
                                        content=ft.Row([
                                            ft.Text(5, color="white")
                                        ], alignment=ft.MainAxisAlignment.CENTER)
                                    ),
                                    ft.IconButton(icon=ft.Icons.ADD, icon_color="white")
                                ]),
                                ft.IconButton(icon=ft.Icons.DELETE, icon_color="white")
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)                                         
                        ]),
                        ft.Divider(height=1),
                        ft.Column([
                            ft.Row([
                                ft.Image("products/img13.png", width=50, height=50),
                                ft.Column([
                                    ft.Text("Lapices Faber Castell", color="white"),
                                    ft.Text("Precio: Bs.10.00", color=cfg.COLOR_PURPLE)
                                ]),
                                ft.Text("Bs.40.00", color=cfg.COLOR_PURPLE, size=20, weight="bold")
                            ]),
                            ft.Row([
                                ft.Row([
                                    ft.IconButton(icon=ft.Icons.REMOVE, icon_color="white"),
                                    ft.Container(
                                        border_radius=3,
                                        width=40,
                                        height=25,
                                        bgcolor=cfg.BG_COLOR,
                                        content=ft.Row([
                                            ft.Text(5, color="white")
                                        ], alignment=ft.MainAxisAlignment.CENTER)
                                    ),
                                    ft.IconButton(icon=ft.Icons.ADD, icon_color="white")
                                ]),
                                ft.IconButton(icon=ft.Icons.DELETE, icon_color="white")
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)                                         
                        ]),
                    ]
                ),
                ft.Container(
                    padding=10,
                    height=210,
                    content=ft.Column(
                        controls=[
                            ft.Divider(height=1),
                            ft.Row([
                                ft.Column([
                                    ft.Text("Total", weight="bold", color="white"),
                                    ft.Text("Items: 3 Quanty: 6", color=ft.Colors.GREY_400)
                                ]),
                                ft.Text("67 Bs", size=30, weight="bold", color=cfg.COLOR_PURPLE)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ft.CupertinoButton(
                                "Imprimir Factura",
                                bgcolor=cfg.COLOR_PURPLE,
                                color=ft.Colors.WHITE,
                                width=300
                            ),
                            ft.CupertinoButton(
                                "Método de Pago",
                                bgcolor=ft.Colors.GREEN_600,
                                color=ft.Colors.WHITE,
                                width=300
                            ),
                        ]
                    )
                )
            ]
        )

    def add_product(self, product: dict):
        self.cart_items.append(product)
        self.update_cart_display()
        print(f"🛒 Producto agregado al carrito: {product.get('name', 'Sin nombre')}")

    def update_cart_display(self):
        pass


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
        if self.products_grid_ref.current:
            self.products_grid_ref.current.controls.clear()
            
            for product in self.filtered_products:
                card = ProductCard(
                    product=product,
                    page=self.page,
                    on_add_to_cart=self.shopping_cart.add_product,
                    show_details_callback=self.show_product_details
                )
                self.products_grid_ref.current.controls.append(card)
            
            self.products_grid_ref.current.update()

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
        
        # Datos de equilibrio de mercado basados en la imagen
        # Oferta: Qs = -20 + Px
        # Demanda: Qd = 100 - 2Px
        # Equilibrio: Pe = 40, Qe = 20
        
        # Generar puntos para la gráfica
        supply_points = []
        demand_points = []
        
        for px in range(0, 70, 5):
            # Línea de Oferta (verde): Qs = -20 + Px
            qs = -20 + px
            if qs >= 0:
                supply_points.append(ft.LineChartDataPoint(px, qs))
            
            # Línea de Demanda (cyan): Qd = 100 - 2Px
            qd = 100 - 2 * px
            if qd >= 0:
                demand_points.append(ft.LineChartDataPoint(px, qd))
        
        # Crear gráfica de equilibrio de mercado
        chart = ft.LineChart(
            tooltip_bgcolor=ft.Colors.with_opacity(0.8, cfg.BG_COLOR),
            data_series=[
                # Línea de Demanda (Dx) - Cyan con relleno
                ft.LineChartData(
                    data_points=demand_points,
                    color=ft.Colors.CYAN,
                    stroke_width=3,
                    curved=False,
                    stroke_cap_round=True,
                    below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.CYAN),
                ),
                # Línea de Oferta (Sx) - Verde con relleno
                ft.LineChartData(
                    data_points=supply_points,
                    color=ft.Colors.GREEN,
                    stroke_width=3,
                    curved=False,
                    stroke_cap_round=True,
                    below_line_bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN),
                ),
                # Punto de Equilibrio
                ft.LineChartData(
                    data_points=[ft.LineChartDataPoint(40, 20)],
                    color=ft.Colors.RED,
                    stroke_width=0,
                    point=True,
                ),
            ],
            min_x=0,
            max_x=70,
            min_y=0,
            max_y=70,
            border=ft.Border(
                bottom=ft.BorderSide(2, ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
                left=ft.BorderSide(2, ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
            ),
            left_axis=ft.ChartAxis(
                title=ft.Text("Cantidad (Qx)", color="white", size=11, weight="bold"),
                title_size=30,
                labels_size=25,
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("0", color="white", size=10)),
                    ft.ChartAxisLabel(value=10, label=ft.Text("10", color="white", size=10)),
                    ft.ChartAxisLabel(value=20, label=ft.Text("20", color="white", size=10)),
                    ft.ChartAxisLabel(value=30, label=ft.Text("30", color="white", size=10)),
                    ft.ChartAxisLabel(value=40, label=ft.Text("40", color="white", size=10)),
                    ft.ChartAxisLabel(value=50, label=ft.Text("50", color="white", size=10)),
                    ft.ChartAxisLabel(value=60, label=ft.Text("60", color="white", size=10)),
                    ft.ChartAxisLabel(value=70, label=ft.Text("70", color="white", size=10)),
                ],
            ),
            bottom_axis=ft.ChartAxis(
                title=ft.Text("Precio (Px)", color="white", size=11, weight="bold"),
                title_size=30,
                labels_size=25,
                labels=[
                    ft.ChartAxisLabel(value=0, label=ft.Text("0", color="white", size=10)),
                    ft.ChartAxisLabel(value=10, label=ft.Text("10", color="white", size=10)),
                    ft.ChartAxisLabel(value=20, label=ft.Text("20", color="white", size=10)),
                    ft.ChartAxisLabel(value=30, label=ft.Text("30", color="white", size=10)),
                    ft.ChartAxisLabel(value=40, label=ft.Text("40", color="white", size=10)),
                    ft.ChartAxisLabel(value=50, label=ft.Text("50", color="white", size=10)),
                    ft.ChartAxisLabel(value=60, label=ft.Text("60", color="white", size=10)),
                    ft.ChartAxisLabel(value=70, label=ft.Text("70", color="white", size=10)),
                ],
            ),
        )
        
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
                                                                                    ft.Text("Dx", size=10, color=ft.Colors.CYAN),
                                                                                ]
                                                                            )
                                                                        ),
                                                                        ft.Container(
                                                                            padding=5,
                                                                            content=ft.Row(
                                                                                spacing=3,
                                                                                controls=[
                                                                                    ft.Container(width=15, height=3, bgcolor=ft.Colors.GREEN, border_radius=2),
                                                                                    ft.Text("Sx", size=10, color=ft.Colors.GREEN),
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
        
        return ft.Row(
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            self.category_bar,
                            products_grid
                        ]
                    )
                ),
                self.shopping_cart,
            ]
        )