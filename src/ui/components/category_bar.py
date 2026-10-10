import flet as ft
from flet import Icons

from src import config as cfg

class CategoryBar(ft.Container):
    """
    Barra de navegación horizontal con categorías de productos
    """
    def __init__(self, on_category_change=None):
        self.on_category_change = on_category_change
        self.current_scroll_offset = 0
        self.category_list_ref = ft.Ref[ft.ListView]()
        self.selected_category = "all"
        self.category_buttons = {}
        
        super().__init__()
        
        self.content = self.build_content()
        
        self.bgcolor = cfg.CONTAINER_COLOR
        self.height = 50
        self.border_radius = 15
        self.padding = 5

    def build_content(self):
        categories = [
            ("all", Icons.ALL_INBOX, "Todo"),
            ("Abarrotes", Icons.LOCAL_GROCERY_STORE, "Abarrotes"),
            ("Bebidas", Icons.LOCAL_BAR, "Bebidas"),
            ("Carnes", Icons.FASTFOOD, "Carnes"),
            ("Congelados", Icons.AC_UNIT, "Congelados"),
            ("Lácteos y Derivados", Icons.WATER_DROP, "Lácteos y Derivados"),
            ("Panadería", Icons.BAKERY_DINING, "Panadería"),
            ("Cuidado del Hogar", Icons.CLEANING_SERVICES, "Cuidado del Hogar"),
            ("Cuidado Personal", Icons.WASH, "Cuidado Personal"),
            ("Papelería", Icons.EDIT, "Papelería"),
            ("Juguetería", Icons.TOYS, "Juguetería"),
            ("Farmacia", Icons.LOCAL_HOSPITAL, "Farmacia"),
        ]
        
        category_buttons = []
        for cat_id, icon, name in categories:
            selected = (cat_id == self.selected_category)
            btn = ft.Container(
                padding=10,
                bgcolor=cfg.COLOR_PURPLE if selected else cfg.COLOR_NAVEGATION_BT,
                border_radius=15,
                on_click=lambda e, c=cat_id: self.handle_category_click(c),
                height=40,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(icon, color="white"),
                        ft.Text(name, color="white", weight="bold" if selected else "normal")
                    ]
                )
            )
            self.category_buttons[cat_id] = btn
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
        self.selected_category = category_id
        self.update_selection()
        if self.on_category_change:
            self.on_category_change(category_id)

    def update_selection(self):
        """Resalta el boton de la categoria actualmente seleccionada."""
        for cat_id, btn in self.category_buttons.items():
            selected = (cat_id == self.selected_category)
            btn.bgcolor = cfg.COLOR_PURPLE if selected else cfg.COLOR_NAVEGATION_BT
            row = btn.content
            if row is not None and len(row.controls) > 1:
                row.controls[1].weight = "bold" if selected else "normal"
        self.update()
