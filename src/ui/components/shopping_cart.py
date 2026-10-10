import flet as ft
from flet import Icons

from src import config as cfg

class ShoppingCart(ft.Container):
    """
    Panel del carrito de compras en el lado derecho.
    Permite agregar productos, modificar cantidades y quitarlos.
    """
    def __init__(self):
        super().__init__()

        # Cada elemento es un dict: {"product": <dict>, "quantity": <int>}
        self.cart_items = []
        self.cart_list_ref = ft.Ref[ft.ListView]()
        self.total_text_ref = ft.Ref[ft.Text]()
        self.items_text_ref = ft.Ref[ft.Text]()

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
                    spacing=6,
                    controls=self.build_cart_items(),
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
                                    ft.Text("Items: 0  Cantidad: 0", color=ft.Colors.GREY_400, ref=self.items_text_ref)
                                ]),
                                ft.Text("0.00 Bs", size=30, weight="bold", color=cfg.COLOR_PURPLE, ref=self.total_text_ref)
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
                                width=300,
                                on_click=self.show_payment_method_dialog,
                            ),
                        ]
                    )
                )
            ]
        )


    # ---------- Render de los items del carrito ----------

    def build_cart_items(self):
        """Devuelve la lista de controles a mostrar dentro del carrito."""
        if not self.cart_items:
            return [
                ft.Container(
                    padding=20,
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, color=ft.Colors.GREY_600, size=40),
                            ft.Text("El carrito esta vacio", color=ft.Colors.GREY_400, size=12),
                            ft.Text(
                                "Usa el boton Agregar de cada producto",
                                color=ft.Colors.GREY_600,
                                size=11,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                    ),
                )
            ]

        items = []
        for index, item in enumerate(self.cart_items):
            items.append(self.build_cart_item(item, index))
            items.append(ft.Divider(height=1))
        return items

    def build_cart_item(self, item: dict, index: int):
        """Construye la tarjeta de un producto dentro del carrito."""
        product = item["product"]
        quantity = item["quantity"]
        price = self._to_float(product.get("saleprice", 0))
        subtotal = price * quantity

        return ft.Column(
            spacing=4,
            controls=[
                ft.Row([
                    ft.Image(
                        src=product.get("image", ""),
                        width=50,
                        height=50,
                        fit=ft.ImageFit.COVER,
                        error_content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=30, color="white"),
                    ),
                    ft.Column(
                        expand=True,
                        spacing=2,
                        controls=[
                            ft.Text(
                                product.get("name", "Sin nombre"),
                                color="white",
                                size=12,
                                max_lines=2,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(f"Precio: Bs.{price:.2f}", color=cfg.COLOR_PURPLE, size=11),
                        ],
                    ),
                    ft.Text(f"Bs.{subtotal:.2f}", color=cfg.COLOR_PURPLE, size=15, weight="bold"),
                ]),
                ft.Row([
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.REMOVE,
                            icon_color="white",
                            icon_size=18,
                            on_click=lambda e, i=index: self.decrease_quantity(i),
                        ),
                        ft.Container(
                            border_radius=3,
                            width=40,
                            height=25,
                            bgcolor=cfg.BG_COLOR,
                            content=ft.Row([
                                ft.Text(quantity, color="white")
                            ], alignment=ft.MainAxisAlignment.CENTER),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            icon_color="white",
                            icon_size=18,
                            on_click=lambda e, i=index: self.increase_quantity(i),
                        ),
                    ]),
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="white",
                        tooltip="Quitar del carrito",
                        on_click=lambda e, i=index: self.remove_product(i),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ],
        )

    # ---------- Logica del carrito ----------

    def add_product(self, product: dict):
        """Agrega un producto. Si ya existe en el carrito, aumenta su cantidad."""
        for item in self.cart_items:
            if item["product"].get("id") == product.get("id"):
                item["quantity"] += 1
                break
        else:
            self.cart_items.append({"product": product, "quantity": 1})

        self.update_cart_display()
        print(f"Producto agregado al carrito: {product.get('name', 'Sin nombre')}")

    def remove_product(self, index: int):
        """Quita por completo un producto del carrito."""
        if 0 <= index < len(self.cart_items):
            removed = self.cart_items.pop(index)
            print(f"Producto quitado: {removed['product'].get('name', 'Sin nombre')}")
            self.update_cart_display()

    def increase_quantity(self, index: int):
        if 0 <= index < len(self.cart_items):
            self.cart_items[index]["quantity"] += 1
            self.update_cart_display()

    def decrease_quantity(self, index: int):
        if 0 <= index < len(self.cart_items):
            self.cart_items[index]["quantity"] -= 1
            # Si llega a cero, se elimina del carrito
            if self.cart_items[index]["quantity"] <= 0:
                self.cart_items.pop(index)
            self.update_cart_display()

    def update_cart_display(self):
        """Vuelve a dibujar la lista y recalcula los totales."""
        if self.cart_list_ref.current is not None:
            self.cart_list_ref.current.controls = self.build_cart_items()

        total = sum(
            self._to_float(item["product"].get("saleprice", 0)) * item["quantity"]
            for item in self.cart_items
        )
        total_units = sum(item["quantity"] for item in self.cart_items)

        if self.total_text_ref.current is not None:
            self.total_text_ref.current.value = f"{total:.2f} Bs"
        if self.items_text_ref.current is not None:
            self.items_text_ref.current.value = f"Items: {len(self.cart_items)}  Cantidad: {total_units}"

        self.update()

    @staticmethod
    def _to_float(value):
        """Convierte un valor a float de forma segura."""
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0


    def show_payment_method_dialog(self, e=None):
        """
        Muestra una ventana emergente (dialogo) para elegir/cargar el metodo de pago.
        """
        # --- Paleta del diseno (tema claro) ---
        WHITE = "#FFFFFF"
        DARK = "#1B1B1B"
        BORDER = "#E3E3E6"
        ORANGE = "#F0532A"
        GOLD = "#E8C766"

        def light_white(opacity=0.78):
            return ft.Colors.with_opacity(opacity, "white")

        card_type_ref = ft.Ref[ft.Text]()
        card_number_ref = ft.Ref[ft.Text]()
        card_holder_ref = ft.Ref[ft.Text]()
        method_label_ref = ft.Ref[ft.Text]()

        def close_dlg(ev=None):
            dlg.open = False
            self.page.update()

        def on_holder_change(ev):
            value = (ev.control.value or "").strip().upper()
            if card_holder_ref.current is not None:
                card_holder_ref.current.value = value if value else "CARDHOLDER NAME"
                self.page.update()

        def on_number_change(ev):
            raw = "".join(c for c in (ev.control.value or "") if c.isdigit())[:16]
            if card_number_ref.current is not None:
                if raw:
                    card_number_ref.current.value = " ".join(raw[i:i + 4] for i in range(0, len(raw), 4))
                else:
                    card_number_ref.current.value = "1234 5678 9012 3456"
                self.page.update()

        method_circles = []

        def select_method(name, circle):
            for c in method_circles:
                c.border = ft.border.all(1, BORDER)
            circle.border = ft.border.all(2, ORANGE)
            if method_label_ref.current is not None:
                method_label_ref.current.value = name
            if card_type_ref.current is not None:
                card_type_ref.current.value = name.upper()
            self.page.update()

        def build_method_circle(name, content, bgcolor=WHITE, border_color=BORDER):
            circle = ft.Container(
                width=56, height=56, border_radius=28,
                bgcolor=bgcolor, border=ft.border.all(1, border_color),
                alignment=ft.alignment.center, content=content,
                on_click=lambda ev: select_method(name, circle),
            )
            method_circles.append(circle)
            return circle

        mastercard_logo = ft.Stack(
            width=30, height=20,
            controls=[
                ft.Container(width=20, height=20, border_radius=10, bgcolor="#EB001B", left=0, top=0),
                ft.Container(width=20, height=20, border_radius=10, bgcolor="#F79E1B", left=10, top=0),
            ],
        )

        add_circle = ft.Container(
            width=56, height=56, border_radius=28, bgcolor=WHITE,
            border=ft.border.all(1, BORDER), alignment=ft.alignment.center,
            content=ft.Icon(ft.Icons.ADD, size=26, color=DARK),
        )
        mastercard_circle = build_method_circle("Master Card", mastercard_logo, bgcolor="#1A1A1A", border_color="#1A1A1A")
        visa_circle = build_method_circle("Visa", ft.Text("VISA", size=18, weight="bold", italic=True, color="#1A1F71"))
        paypal_circle = build_method_circle("PayPal", ft.Icon(ft.Icons.PAYPAL, size=28, color="#20389B"))
        apple_circle = build_method_circle("Apple Pay", ft.Icon(ft.Icons.APPLE, size=26, color="#000000"))

        methods_row = ft.Row(
            spacing=12,
            controls=[add_circle, mastercard_circle, visa_circle, paypal_circle, apple_circle],
        )
        # --- Vista previa de la tarjeta ---
        chip = ft.Container(
            width=46, height=34, border_radius=6, bgcolor=GOLD,
            content=ft.Stack(
                width=46, height=34,
                controls=[
                    ft.Container(width=46, height=1, bgcolor=ft.Colors.with_opacity(0.35, "#8a6d1f"), top=11),
                    ft.Container(width=46, height=1, bgcolor=ft.Colors.with_opacity(0.35, "#8a6d1f"), top=22),
                    ft.Container(width=1, height=34, bgcolor=ft.Colors.with_opacity(0.35, "#8a6d1f"), left=15),
                    ft.Container(width=1, height=34, bgcolor=ft.Colors.with_opacity(0.35, "#8a6d1f"), left=30),
                ],
            ),
        )

        valid_thru = ft.Column(
            spacing=3, horizontal_alignment=ft.CrossAxisAlignment.END,
            controls=[
                ft.Text("VALID THRU", size=8, color=light_white(0.7)),
                ft.Container(
                    border=ft.border.all(1, light_white(0.6)),
                    border_radius=5,
                    padding=ft.padding.symmetric(horizontal=8, vertical=2),
                    content=ft.Text("09/30", size=11, weight="bold", color="white"),
                ),
            ],
        )

        card_preview = ft.Container(
            bgcolor=ORANGE, border_radius=20, padding=18,
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text("CARD TYPE", size=11, weight="bold", color=light_white(0.75), ref=card_type_ref),
                            ft.Text("BANK NAME", size=11, weight="bold", color=light_white(0.75)),
                        ],
                    ),
                    ft.Container(height=14),
                    chip,
                    ft.Container(height=10),
                    ft.Text("1234", size=10, color=light_white(0.6)),
                    ft.Container(height=8),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("1234 5678 9012 3456", ref=card_number_ref, size=20, weight="bold", color="white"),
                            valid_thru,
                        ],
                    ),
                    ft.Container(height=14),
                    ft.Text("CARDHOLDER NAME", size=9, color=light_white(0.7)),
                    ft.Text("CARDHOLDER NAME", ref=card_holder_ref, size=13, weight="bold", color="white"),
                ],
            ),
        )

        # --- Campos del formulario ---
        def field(**kwargs):
            return ft.TextField(
                border_radius=12,
                border_color=BORDER,
                focused_border_color=ORANGE,
                text_size=14,
                cursor_color=ORANGE,
                content_padding=ft.padding.symmetric(horizontal=14, vertical=14),
                hint_style=ft.TextStyle(color="#B8B8BD", size=14),
                **kwargs,
            )

        holder_field = field(hint_text="Johan smit", on_change=on_holder_change)
        cvv_field = field(hint_text="123", password=True)
        number_field = field(
            hint_text="1234 **** **** ****",
            on_change=on_number_change,
            suffix_icon=ft.Icon(ft.Icons.CREDIT_CARD, color="#B8B8BD"),
        )

        fields_section = ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    spacing=14,
                    controls=[
                        ft.Column(
                            expand=True, spacing=6,
                            controls=[
                                ft.Text("Cardholder Name", size=14, weight="bold", color=DARK),
                                holder_field,
                            ],
                        ),
                        ft.Column(
                            width=110, spacing=6,
                            controls=[
                                ft.Text("CVV", size=14, weight="bold", color=DARK),
                                cvv_field,
                            ],
                        ),
                    ],
                ),
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text("Card Number", size=14, weight="bold", color=DARK),
                        number_field,
                    ],
                ),
            ],
        )
        def save_payment(ev):
            dlg.open = False
            self.page.update()
            try:
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Metodo de pago guardado correctamente"),
                    bgcolor="#22C55E",
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as ex:
                print("No se pudo mostrar el snackbar:", ex)
            print("Metodo de pago guardado")

        save_button = ft.ElevatedButton(
            "Save",
            bgcolor=ORANGE,
            color="white",
            width=400,
            height=54,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=27)),
            on_click=save_payment,
        )

        header = ft.Row(
            controls=[
                ft.Container(
                    width=44, height=44, border_radius=22, bgcolor=WHITE,
                    border=ft.border.all(1, BORDER), alignment=ft.alignment.center,
                    content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW, size=18, color=DARK),
                    on_click=close_dlg,
                ),
                ft.Container(
                    expand=True, alignment=ft.alignment.center,
                    content=ft.Text("Payment Method", size=16, weight="bold", color=DARK),
                ),
                ft.Container(
                    width=44, height=44, border_radius=22, bgcolor=WHITE,
                    border=ft.border.all(1, BORDER), alignment=ft.alignment.center,
                    content=ft.Icon(ft.Icons.MORE_VERT, size=18, color=DARK),
                ),
            ],
        )

        content_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=14,
            controls=[
                header,
                ft.Text("Payment Method", size=24, weight="bold", color=DARK),
                methods_row,
                ft.Text("Master Card", size=18, weight="bold", color=DARK, ref=method_label_ref),
                card_preview,
                fields_section,
                save_button,
            ],
        )

        dlg = ft.AlertDialog(
            modal=True,
            bgcolor=WHITE,
            shape=ft.RoundedRectangleBorder(radius=28),
            content_padding=ft.padding.all(22),
            inset_padding=ft.padding.symmetric(vertical=20, horizontal=24),
            barrier_color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            content=ft.Container(width=400, height=500, content=content_column),
        )

        # Marcar Master Card como seleccionada por defecto
        mastercard_circle.border = ft.border.all(2, ORANGE)

        # Evitar acumular ventanas si se abre varias veces
        previous = getattr(self, "_payment_dlg", None)
        if previous is not None and previous in self.page.overlay:
            self.page.overlay.remove(previous)
        self._payment_dlg = dlg
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
        print("Ventana de metodo de pago abierta")
