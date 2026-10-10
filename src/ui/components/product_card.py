import flet as ft
from flet import Icons

from src import config as cfg

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
                            # Botones: agregar al carrito y ver detalles
                            ft.Row(
                                spacing=5,
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.FilledButton(
                                        "Agregar",
                                        icon=ft.Icons.ADD_SHOPPING_CART,
                                        bgcolor=cfg.COLOR_BLUE,
                                        expand=True,
                                        style=ft.ButtonStyle(
                                            padding=ft.padding.symmetric(horizontal=4),
                                            text_style=ft.TextStyle(size=12),
                                        ),
                                        on_click=self.handle_add_to_cart,
                                    ),
                                    ft.FilledButton(
                                        "Detalles",
                                        bgcolor=cfg.COLOR_PURPLE,
                                        expand=True,
                                        style=ft.ButtonStyle(
                                            padding=ft.padding.symmetric(horizontal=4),
                                            text_style=ft.TextStyle(size=12),
                                        ),
                                        on_click=self.handle_details_click,
                                    ),
                                ],
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

    def handle_add_to_cart(self, e):
        """
        Maneja el clic en el boton Agregar: envia el producto al carrito.
        """
        print(f"CLICK AGREGAR en: {self.product.get('name', 'Sin nombre')}")
        if self.on_add_to_cart:
            self.on_add_to_cart(self.product)
        else:
            print("No hay callback de carrito configurado")
