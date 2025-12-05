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
    def __init__(self, product: dict, page: ft.Page, on_add_to_cart=None):
        """
        Args:
            product (dict): Diccionario con los datos del producto
            page (ft.Page): Referencia a la página principal
            on_add_to_cart (callable): Función que se ejecuta al agregar al carrito
        """
        self.product = product
        self.page = page
        self.on_add_to_cart = on_add_to_cart
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
                        self.product['image'], 
                        width=200,
                        fit=ft.ImageFit.COVER
                    ), 
                    expand=1
                ),
                ft.Container(
                    padding=ft.padding.only(left=10, right=10, bottom=10), 
                    content=ft.Column(
                        controls=[
                            # Título del producto
                            ft.Text(
                                self.product['name'], 
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
                                        f"Bs.{self.product['saleprice']}", 
                                        color="white",
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    ft.Text(
                                        f"Bs.{self.product['purchaseprice']}", 
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
                                on_click=lambda e: self.show_product_details()
                            )
                        ], 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        height=121
                    )   
                )
            ]
        )

    def show_product_details(self):
        """
        Muestra un diálogo con los detalles del producto
        """
        # Crear el diálogo con fondo oscurecido
        details_dialog = ft.AlertDialog(
            modal=True,
            bgcolor=cfg.CONTAINER_COLOR,
            content=ft.Container(
                width=1000,  # Ancho del contenedor (ajustable)
                height=600,  # Alto del contenedor (ajustable)
                padding=20,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        # ========================================
                        # HEADER: Título y botón de cerrar
                        # ========================================
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text(
                                    "Detalles del Producto", 
                                    size=24, 
                                    weight="bold", 
                                    color="white"
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="white",
                                    icon_size=30,
                                    on_click=lambda e: self.close_dialog(details_dialog)
                                )
                            ]
                        ),
                        
                        ft.Divider(height=20, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                        
                        # ========================================
                        # AQUÍ EMPIEZA TU ÁREA DE CONTENIDO
                        # Puedes agregar cualquier diseño aquí
                        # ========================================
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                scroll=ft.ScrollMode.ADAPTIVE,
                                spacing=15,
                                controls=[
                                    # 🎨 AGREGA TU CONTENIDO AQUÍ
                                    # Ejemplo de estructura que puedes usar:
                                    
                                    ft.Text(
                                        "✨ Aquí puedes diseñar tu interfaz ✨",
                                        size=18,
                                        color=ft.Colors.GREY_400,
                                        text_align=ft.TextAlign.CENTER
                                    ),
                                    
                                    ft.Container(height=20),
                                    
                                    # Puedes agregar filas, columnas, imágenes, etc.
                                    ft.Text(
                                        f"Producto: {self.product['name']}",
                                        size=16,
                                        color="white"
                                    ),
                                    
                                    # Más elementos...
                                    
                                ]
                            )
                        ),
                        
                        # ========================================
                        # FOOTER: Botones de acción (opcional)
                        # ========================================
                        ft.Container(
                            padding=ft.padding.only(top=15),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.FilledButton(
                                        "Agregar al Carrito",
                                        bgcolor="green",
                                        icon=ft.Icons.ADD_SHOPPING_CART,
                                        height=45,
                                        on_click=lambda e: self.add_to_cart(details_dialog)
                                    ),
                                    ft.FilledButton(
                                        "Cerrar",
                                        bgcolor=cfg.COLOR_PURPLE,
                                        height=45,
                                        on_click=lambda e: self.close_dialog(details_dialog)
                                    )
                                ]
                            )
                        )
                    ]
                )
            )
        )
        
        self.page.dialog = details_dialog
        details_dialog.open = True
        self.page.update()

    def close_dialog(self, dialog):
        """
        Cierra el diálogo
        """
        dialog.open = False
        self.page.update()

    def add_to_cart(self, dialog):
        """
        Agrega el producto al carrito
        """
        if self.on_add_to_cart:
            self.on_add_to_cart(self.product)
        self.close_dialog(dialog)


class CategoryBar(ft.Container):
    """
    Barra de navegación horizontal con categorías de productos
    """
    def __init__(self, on_category_change=None):
        """
        Args:
            on_category_change (callable): Función que se ejecuta al cambiar de categoría
        """
        self.on_category_change = on_category_change
        self.current_scroll_offset = 0
        self.category_list_ref = ft.Ref[ft.ListView]()
        
        super().__init__()
        
        # Construcción del contenedor
        self.content = self.build_content()
        
        # Estilos
        self.bgcolor = cfg.CONTAINER_COLOR
        self.height = 50
        self.border_radius = 15
        self.padding = 5

    def build_content(self):
        """
        Construye la barra de categorías
        """
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
        """
        Desplaza las categorías horizontalmente
        """
        category_list = self.category_list_ref.current
        
        if category_list:
            new_scroll = self.current_scroll_offset + delta
            
            if new_scroll < 0:
                new_scroll = 0
            
            category_list.scroll_to(offset=new_scroll, duration=300)
            self.current_scroll_offset = new_scroll
            self.update()

    def handle_category_click(self, category_id: str):
        """
        Maneja el click en una categoría
        """
        if self.on_category_change:
            self.on_category_change(category_id)


class ShoppingCart(ft.Container):
    """
    Panel del carrito de compras en el lado derecho
    """
    def __init__(self):
        super().__init__()
        
        self.cart_items = []  # Lista de productos en el carrito
        self.cart_list_ref = ft.Ref[ft.ListView]()
        self.total_text_ref = ft.Ref[ft.Text]()
        
        # Construcción del contenedor
        self.content = self.build_content()
        
        # Estilos
        self.bgcolor = cfg.CONTAINER_COLOR
        self.width = 300
        self.border_radius = 15
        self.padding = 10

    def build_content(self):
        """
        Construye el contenido del carrito
        """
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
                        # Producto 1: Cartulina Oficio
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
                        # Producto 2: Lápices Faber Castell
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
        """
        Agrega un producto al carrito
        """
        self.cart_items.append(product)
        self.update_cart_display()

    def update_cart_display(self):
        """
        Actualiza la visualización del carrito
        """
        # Aquí puedes implementar la lógica para actualizar la lista de productos
        # y el total del carrito
        pass


class InventorySection(ft.Container):
    """
    Sección completa de inventario con productos y carrito
    """
    def __init__(self, page: ft.Page):
        """
        Args:
            page (ft.Page): Referencia a la página principal
        """
        self.page = page
        super().__init__()
        
        # Componentes
        self.category_bar = CategoryBar(on_category_change=self.filter_by_category)
        self.shopping_cart = ShoppingCart()
        self.products_grid_ref = ft.Ref[ft.GridView]()
        self.all_products = self.get_products()
        self.filtered_products = self.all_products.copy()
        
        # Construcción del contenedor
        self.content = self.build_content()
        
        # Estilos
        self.expand = True
        self.margin = 5

    def get_products(self):
        """
        Obtiene los productos desde el servidor
        """
        try:
            response = requests.get("http://127.0.0.1:8000/")
            return json.loads(response.text)
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    def filter_by_category(self, category_id: str):
        """
        Filtra productos por categoría
        """
        if category_id == "all":
            self.filtered_products = self.all_products.copy()
        else:
            self.filtered_products = [
                p for p in self.all_products 
                if p.get('category', '').lower() == category_id.lower()
            ]
        
        self.update_products_grid()

    def update_products_grid(self):
        """
        Actualiza la grilla de productos
        """
        if self.products_grid_ref.current:
            self.products_grid_ref.current.controls.clear()
            
            for product in self.filtered_products:
                card = ProductCard(
                    product=product,
                    page=self.page,
                    on_add_to_cart=self.shopping_cart.add_product
                )
                self.products_grid_ref.current.controls.append(card)
            
            self.products_grid_ref.current.update()

    def build_content(self):
        """
        Construye el contenido completo de la sección
        """
        # Crear tarjetas de productos
        product_cards = []
        for product in self.filtered_products:
            card = ProductCard(
                product=product,
                page=self.page,
                on_add_to_cart=self.shopping_cart.add_product
            )
            product_cards.append(card)
        
        # GridView de productos
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
                # Panel izquierdo: Categorías y productos
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            self.category_bar,
                            products_grid
                        ]
                    )
                ),
                # Panel derecho: Carrito
                self.shopping_cart,
            ]
        )