#Importamos la libreria Flet para la interfaz grafica
import flet as ft
from flet import Icons
import flet_map as fmap
import json
import requests
import employee_seccion as emp

#Definimos la clase principal
class UIApp(ft.Container):
    #Constructor: Inicializa la pagina y define los colores base
    def __init__(self, page: ft.Page):
        super().__init__(expand = True)

        print("Window type:", page.platform) #? Imprime en que plataforma esta corriendo la ventana
        self.page = page
        self.page.padding = 0
        self.page.window_icon = "Hipermaxi_logo.ico" #! No funciona (Aun no encuentro solucion)
        self.page.title = "Hipermaxi - Gestor Administrativo"
        
        

        #Definimos paleta de colores
        self.color_blue = "#73bf16"
        self.color_purple = "#cf672b"
        self.bg_color = "#21324e"
        self.container_color = "#1c2b45"
        self.color_navegation_bt = "#21324e"
        self.color1_card = "#e3501b"
        self.color2_card = "#d6820c"

        self.page.bgcolor = self.bg_color



        #Estilo de animacion para transiciones y efectos
        self.animation_style = ft.Animation(500, ft.AnimationCurve.EASE_IN_TO_LINEAR)

        # Referencia para controlar el scroll de la lista de categorías
        self.category_list_ref = ft.Ref[ft.ListView]()
        self.current_scroll_offset = 0

        # -- Grafica: Curva de demanda y oferta --
        x_values = list(range(1,16))
        y_labels = [
            ft.ChartAxisLabel(
                value=0,
                label=ft.Text("0", color=ft.Colors.WHITE, size=15)
            ),
            ft.ChartAxisLabel(
                value=5,
                label=ft.Text("5", color=ft.Colors.WHITE, size=15)
            ),
            ft.ChartAxisLabel(
                value=10,
                label=ft.Text("10", color=ft.Colors.WHITE, size=15)
            ),
        ]
        x_labels = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Text(str(i), color=ft.Colors.WHITE, size=15)
            )
            for i in range(1, 13, 1) # Genera 1, 4, 7, 10, 13
        ]

        #? Datos para graficar: Deben ser 12 para poder distribuirlos en los 12 Meses del
        green_line = [1.2, 1.5, 2.0, 8, 3.2, 5, 2.0, 2.5, 5, 10, 2.1, 4]
        red_line = [1.8, 8, 1.5, 7, 1.6, 1.8, 2.0, 10, 1.8, 3, 2.0, 2.2]
        blue_line = [3, 1.3, 2.8, 4, 3, 1, 4, 3, 5, 9, 3, 5.2]

        #!bottom_axis = ft.ChartAxis(labels_size=25, labels_interval=3, show_labels=True) -- Sirve pero no encuentro metodo para cambiar de color los numeros
        bottom_axis = ft.ChartAxis(labels_size=25, labels=x_labels, show_labels=True)
        left_axis = ft.ChartAxis(labels_size=25, labels=y_labels, show_labels=True)
        


        # --- Series de datos para la gráfica ---
        self.green_line_data = ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, y, selected=(x==8)) for x, y in zip(x_values, green_line)],
            color="green",
            stroke_width=1,
            curved=True,
            below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.GREEN),
            visible=True
        )
        self.red_line_data = ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, y, selected=(x==8)) for x, y in zip(x_values, red_line)],
            color="red",
            stroke_width=1,
            curved=True,
            below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.RED),
            visible=True
        )
        self.blue_line_data = ft.LineChartData(
            data_points=[ft.LineChartDataPoint(x, y, selected=(x==8)) for x, y in zip(x_values, blue_line)],
            color="blue",
            stroke_width=1,
            curved=True,
            below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.BLUE),
            visible=True
        )

        self.char_data = ft.LineChart(
            tooltip_bgcolor="transparent",
            data_series=[
                self.green_line_data,
                self.red_line_data,
                self.blue_line_data,
            ],
            #? Modifica El valor maximo  y minimo del eje "Y"
            min_y=0, max_y=10,
            expand=True,
            border=ft.Border(
                bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                left=ft.BorderSide(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            ),
            bottom_axis=bottom_axis,
            left_axis=left_axis
        )
        def getProducts():
            return json.loads(requests.get("http://127.0.0.1:8000/").text)

        products = []
        
        # --- Lista de Productos: Inventario ---- 
        #? Es necesario correr el servidor local "simple_server.py"
        for product in getProducts():
            products.append(
                ft.Container(
                    aspect_ratio=1.5,
                    bgcolor=self.container_color, 
                    border_radius=10, 
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Image(
                                    product['image'], 
                                    width=page.window.width/3, 
                                    fit=ft.ImageFit.COVER
                                ), 
                                expand=1
                            ),
                            ft.Container(
                                padding=ft.padding.only(left=10, right=10, bottom=10), 
                                content=ft.Column(
                                    [
                                        # Título del producto
                                        ft.Text(

                                            product['name'], 
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
                                                    ft.Text(f"Bs.{product['saleprice']}", color="white",text_align=ft.TextAlign.CENTER),
                                                    ft.Text(f"Bs.{product['purchaseprice']}", color=self.color_purple,text_align=ft.TextAlign.CENTER),
                                                ]
                                        ),
                                        # Botón
                                        ft.FilledButton("Detalles", bgcolor=self.color_purple, expand=True,width=130)
                                    ], 
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,height=121
                                )   
                            )
                        ]
                    )
                )
            )
        
        # --- Menú de Notificaciones Flotante ---
        self.notifications_popup = ft.Container(
            visible=False,
            width=300,
            height=400,
            padding=15,
            bgcolor=self.bg_color,
            border_radius=10,
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            ),
            # Columna con notificaciones
            content=ft.Column(
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    ft.Text("Notificaciones (21)", size=18, weight="bold", color="white"),
                    ft.Divider(color="white"),
                    # Notificación 1
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Nueva Venta Registrada", size=14, weight="bold", color="white"),
                            ft.Text("Hace 5 minutos", size=12, color=ft.Colors.GREY)
                        ], spacing=0),
                        padding=ft.padding.only(bottom=10)
                    ),
                    # Notificación 2
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Inventario bajo: Leche", size=14, weight="bold", color=ft.Colors.RED),
                            ft.Text("Verificar stock", size=12, color=ft.Colors.GREY)
                        ], spacing=0),
                        padding=ft.padding.only(bottom=10)
                    ),
                    # Notificación 3
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Reporte Mensual listo", size=14, weight="bold", color="white"),
                            ft.Text("Ayer a las 10:00 AM", size=12, color=ft.Colors.GREY)
                        ], spacing=0),
                        padding=ft.padding.only(bottom=10)
                    ),
                    ft.TextButton(
                        "Ver todas", 
                        on_click=self.hide_notifications,
                        style=ft.ButtonStyle(color=self.color_purple)
                    )
                ]
            )
        )

        # --- Seccion Superior: Busqueda, Notificaciones, Usuario ---
        self.fixed_header = ft.Container( 
            height=60,
            padding=ft.padding.only(left=20, right=10),
            content=ft.Row(
                alignment= ft.MainAxisAlignment.END,
                controls=[
                # --- Campo de busqueda ---
                ft.Container(
                    width=600,
                    border_radius=18,
                    bgcolor=self.container_color,
                    content=ft.TextField(
                        hint_text="Buscar",
                        border_radius=20,
                        border_color="transparent",
                        suffix_icon=ft.Icon(Icons.SEARCH, color="white"),
                        color="white",
                        hint_style=ft.TextStyle(color="white"),
                    ),
                ),
                # --- Icono Notificaciones ---
                ft.Stack(
                    controls=[
                        # Fondo del icono
                        ft.Container(
                            bgcolor=self.container_color,
                            border_radius=20,
                            width=50,
                            height=50,
                            alignment=ft.alignment.center,
                            on_click=self.toggle_notifications,
                            content=ft.Icon(
                                Icons.NOTIFICATIONS_OUTLINED,
                                color="white",
                            ),
                        ),
                        # Numero Flotante del icono
                        ft.Container(
                            width=20,
                            height=20,
                            bgcolor=self.color1_card,
                            border_radius=10,
                            alignment=ft.alignment.center,
                            top=0,
                            right=0,
                            content=ft.Text(
                                "21",
                                size=10,
                                color="white",
                                weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ]
                ),
                # --- Icono de Usuario ---
                ft.Container(
                    bgcolor=self.container_color,
                    border_radius=20,
                    width=50, height=50,
                    content=ft.Icon(Icons.PERSON_ROUNDED, color="white")
                )
                ],
            )
        )

        # --- Contenedor 1: Seccion Inicio ---
        self.container_1 = ft.Container(
            expand=True,
            #bgcolor= self.container_color,
            offset= ft.Offset(0,0),
            animate_offset=self.animation_style,
            margin=5, border_radius=10,
            content= ft.Row(
                controls=[
                    #Parte Izquierda de la seccion Inicio (Resumen de Informacions)
                    ft.Container(
                        expand= True,
                        content= ft.Stack(
                            alignment=ft.alignment.top_center,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    bgcolor=self.container_color,
                                    border_radius=20,
                                    content = ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            # 
                                            ft.Container(
                                                height=195,
                                                padding=ft.padding.all(0),
                                                content=ft.Image(
                                                    src="supermercados3.jpg",
                                                    fit=ft.ImageFit.CONTAIN,
                                                )
                                            ),
                                            
                                            ft.Text("GESTOR ADMINISTRATIVO", color="white", size=20, weight="bold"),
                                            ft.Tabs(
                                                tab_alignment=ft.TabAlignment.CENTER,
                                                indicator_color=self.color_purple,
                                                label_color="white", unselected_label_color="white",
                                                indicator_tab_size=True,
                                                expand=True,
                                                tabs=[
                                                    ft.Tab(
                                                        "Informacion", 
                                                        content= ft.Container(
                                                            padding=15,
                                                            content=ft.Column(
                                                                spacing=0,
                                                                controls=[
                                                                    ft.Row(
                                                                        spacing=0,
                                                                        controls=[
                                                                            ft.Column(
                                                                                spacing=0,
                                                                                controls=[
                                                                                    ft.Row(
                                                                                        alignment=ft.MainAxisAlignment.START,
                                                                                        controls=[
                                                                                            ft.IconButton(ft.Icons.STORE, icon_color="white"),
                                                                                            ft.Text("Sucursal: Hipermaxi Las Brisas S.A.", size=14, color="white"),
                                                                                        ]
                                                                                    ),
                                                                                    ft.Row(
                                                                                        alignment=ft.MainAxisAlignment.START,
                                                                                        controls=[
                                                                                            ft.IconButton(ft.Icons.LOCATION_CITY, icon_color="white"),
                                                                                            ft.Text("Departamento: Santa Cruz de la Sierra", size=14, color="white"),
                                                                                        ]
                                                                                    ),
                                                                                    ft.Row(
                                                                                        alignment=ft.MainAxisAlignment.START,
                                                                                        controls=[
                                                                                            ft.IconButton(ft.Icons.LOCATION_ON_OUTLINED, icon_color="white"),
                                                                                            ft.Text("Direccion: Avenida Banzer, 4to. Anillo", size=14, color="white"),
                                                                                        ]
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            ft.Column(
                                                                                spacing=0,
                                                                                controls=[
                                                                                    ft.Row(
                                                                                        alignment=ft.MainAxisAlignment.START,
                                                                                        controls=[
                                                                                            ft.IconButton(ft.Icons.PIN, icon_color="white"),
                                                                                            ft.Text("NIT: 1028627025", size=14, color="white"),
                                                                                        ]
                                                                                    ),
                                                                                    ft.Row(
                                                                                        alignment=ft.MainAxisAlignment.START,
                                                                                        controls=[
                                                                                            ft.IconButton(ft.Icons.CALENDAR_TODAY, icon_color="white"),
                                                                                            ft.Text("Dias de Atencion: Lunes a Domingo", size=14, color="white"),
                                                                                        ]
                                                                                    ),
                                                                                    ft.Row(
                                                                                        alignment=ft.MainAxisAlignment.START,
                                                                                        controls=[
                                                                                            ft.IconButton(ft.Icons.ACCESS_TIME, icon_color="white"),
                                                                                            ft.Text("Horario: 7:00 a 23:00", size=14, color="white"),
                                                                                        ]
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                        ]
                                                                    ),
                                                                    ft.Divider(height=20, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                                                    
                                                                    ft.Text("Ubicación Sucursal : Hipermaxi Las Brisas S.A.", color="white", size=16, weight="bold"),
                                                                    
                                                                    ft.Container(
                                                                        height=400, 
                                                                        margin=ft.margin.only(top=10),
                                                                        border_radius=10,
                                                                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                                                        expand=True,
                                                                        content=fmap.Map(
                                                                            expand=True,
                                                                            initial_center=fmap.MapLatitudeLongitude(latitude=-17.74905965656158, longitude=-63.17670310453481),
                                                                            layers=[
                                                                                fmap.TileLayer(
                                                                                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                                                                                ),
                                                                                fmap.MarkerLayer(
                                                                                    markers=[
                                                                                        fmap.Marker(
                                                                                            content=ft.Icon(
                                                                                                ft.Icons.LOCATION_ON, 
                                                                                                color=self.color1_card, 
                                                                                                size=40
                                                                                            ),
                                                                                            coordinates=fmap.MapLatitudeLongitude(
                                                                                                -17.74905965656158, -63.17670310453481
                                                                                            ),
                                                                                        )
                                                                                    ]
                                                                                )
                                                                            ],
                                                                            initial_zoom=16,
                                                                        )
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    ft.Tab("Noticias"),
                                                    ft.Tab("Reportes"),
                                                    ft.Tab("Notificaciones"),
                                                    ft.Tab("Usuario")
                                                ]
                                            )
                                        ]
                                    )                              
                                ),
                            ]
                        )
                    ),
                    #Parte Derecha del la seccion Inicio (Grafica, Estado de Resultados)
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    bgcolor=self.container_color, padding=ft.padding.only(left=20,top=10,right=20,bottom=15),
                                    expand=True,border_radius=20,
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Grafica Estado de resultado", color="white", size=16, weight="bold"),
                                                    ft.PopupMenuButton(
                                                        icon=ft.Icons.MORE_HORIZ,
                                                        icon_color="white",
                                                        bgcolor= self.bg_color,
                                                        tooltip="",
                                                        items=[
                                                            ft.PopupMenuItem(
                                                                text="Línea Ingresos por Ventas",
                                                                content=ft.Text(
                                                                    "Línea Ingresos por Ventas",
                                                                    color="white",
                                                                    size=15,
                                                                ),
                                                                on_click=self.toggle_chart_visibility
                                                            ),
                                                            ft.PopupMenuItem(
                                                                text="Línea Costo de Ventas",
                                                                content=ft.Text(
                                                                    "Línea Costo de Ventas",
                                                                    color="white",
                                                                    size=15,
                                                                ),
                                                                on_click=self.toggle_chart_visibility
                                                            ),
                                                            ft.PopupMenuItem(
                                                                text="Línea Utilidad Bruta",
                                                                content=ft.Text(
                                                                    "Línea Utilidad Bruta",
                                                                    color="white",
                                                                    size=15,
                                                                ),
                                                                on_click=self.toggle_chart_visibility
                                                            ),
                                                            ft.PopupMenuItem(
                                                                text="Mostrar Todo",
                                                                content=ft.Text(
                                                                    "Mostrar Todo",
                                                                    color="white",
                                                                    size=15,
                                                                ),
                                                                on_click=self.toggle_chart_visibility
                                                            )
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            self.char_data
                                        ]
                                    )
                                ),
                                ft.Container(
                                    expand=True,
                                    bgcolor=self.container_color,
                                    border_radius=20,
                                    padding=ft.padding.only(left=20,top=10,right=20,bottom=15),
                                    content= ft.Column(
                                        spacing=0,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Estado de Resultados - Anual 2025", color="white", size=16, weight="Bold"),
                                                    ft.Row(
                                                        spacing=0,
                                                        controls=[
                                                            ft.IconButton(ft.Icons.EDIT,icon_color="white"),
                                                            ft.IconButton(ft.Icons.MORE_HORIZ,icon_color="white"), 
                                                        ]
                                                    ),
                                                ]
                                            ),
                                            ft.Container(
                                                expand=True,
                                                theme=ft.Theme(
                                                    scrollbar_theme=ft.ScrollbarTheme(
                                                        track_color={"hovered": ft.Colors.TRANSPARENT, "": self.container_color}, 
                                                        thumb_color={"hovered": self.color_purple, "": ft.Colors.WHITE}, 
                                                        thickness=5, 
                                                        radius=5, 
                                                    )
                                                ),
                                                content=ft.Column(
                                                    scroll=ft.ScrollMode.ADAPTIVE,
                                                    spacing=0,
                                                    controls=[
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.START,
                                                            controls=[
                                                                ft.IconButton(ft.Icons.LINE_AXIS, icon_color="green"),
                                                                ft.Text("Ingreso por ventas: 1,200,327.00 Bs", size=16, color="white"),
                                                            ]
                                                        ),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.START,
                                                            controls=[
                                                                ft.IconButton(ft.Icons.LINE_AXIS, icon_color="red"),
                                                                ft.Text("Costo de ventas: 850,550.00 Bs", size=16, color="white"),
                                                            ]
                                                        ),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.START,
                                                            controls=[
                                                                ft.IconButton(ft.Icons.LINE_AXIS, icon_color="blue"),
                                                                ft.Text("Utilidad Bruta: 423,250.00 Bs", size=16, color="white"),
                                                            ]
                                                        ),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.START,
                                                            controls=[
                                                                ft.IconButton(ft.Icons.LINE_AXIS, icon_color="orange"),
                                                                ft.Text("Gastos Operativos: 281,400.00 Bs", size=16, color="white"),
                                                            ]
                                                        ),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.START,
                                                            controls=[
                                                                ft.IconButton(ft.Icons.LINE_AXIS, icon_color="yellow"),
                                                                ft.Text("Utilidad Operativa: 100,933.00 Bs", size=16, color="white"),
                                                            ]
                                                        ),
                                                        ft.Row(
                                                            alignment=ft.MainAxisAlignment.START,
                                                            controls=[
                                                                ft.IconButton(ft.Icons.LINE_AXIS, icon_color="cyan"),
                                                                ft.Text("Utilidad Neta: 100,250.00 Bs", size=16, color="white"),
                                                            ]
                                                        ),
                                                    ]
                                                )
                                            ),
                                            
                                        ]
                                    )    
                                ),
                                ft.Container(
                                    expand=True,
                                    bgcolor= self.container_color,
                                    border_radius=20, padding=ft.padding.only(left=20,top=10,right=20,bottom=15),
                                    content=ft.Column(
                                        expand=True,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Notificaciones", size=16, weight="bold", color="white"),
                                                    ft.IconButton(ft.Icons.FULLSCREEN, icon_color="white"),
                                                ]
                                            ),
                                            ft.Container(
                                                expand=True,
                                                theme=ft.Theme(
                                                    scrollbar_theme=ft.ScrollbarTheme(
                                                        track_color={"hovered": ft.Colors.TRANSPARENT, "": self.container_color}, 
                                                        thumb_color={"hovered": self.color_purple, "": ft.Colors.WHITE}, 
                                                        thickness=5, 
                                                        radius=5,
                                                    )
                                                ),
                                                content=ft.Column(
                                                    scroll=ft.ScrollMode.ADAPTIVE,
                                                    controls=[
                                                        ft.Container(
                                                            bgcolor=self.bg_color,
                                                            border_radius=15, padding=15,
                                                            content=ft.Column(
                                                                spacing=0, alignment=ft.MainAxisAlignment.START,
                                                                controls=[
                                                                    ft.Text("Notificacion", size=14, color="white", weight="bold"),
                                                                    ft.Divider(height=20, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                                                    ft.Text("Son comunicaciones a través de medios electrónicos y telemáticos de las actuaciones jurisdiccionales, mediante el cual se hace saber a las partes los acuerdos, resoluciones y otros actuados dictadas por los órganos jurisdiccionales.", size=14, color="white")
                                                                ]
                                                            )  
                                                        ),
                                                        ft.Container(
                                                            bgcolor=self.bg_color,
                                                            border_radius=15, padding=15,
                                                            content=ft.Column(
                                                                spacing=0, alignment=ft.MainAxisAlignment.START,
                                                                controls=[
                                                                    ft.Text("Notificacion", size=14, color="white", weight="bold"),
                                                                    ft.Divider(height=20, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                                                    ft.Text("Son comunicaciones a través de medios electrónicos y telemáticos de las actuaciones jurisdiccionales, mediante el cual se hace saber a las partes los acuerdos, resoluciones y otros actuados dictadas por los órganos jurisdiccionales.", size=14, color="white")
                                                                ]
                                                            )  
                                                        ),
                                                        ft.Container(
                                                            bgcolor=self.bg_color,
                                                            border_radius=15, padding=15,
                                                            content=ft.Column(
                                                                spacing=0, alignment=ft.MainAxisAlignment.START,
                                                                controls=[
                                                                    ft.Text("Notificacion", size=14, color="white", weight="bold"),
                                                                    ft.Divider(height=20, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                                                    ft.Text("Son comunicaciones a través de medios electrónicos y telemáticos de las actuaciones jurisdiccionales, mediante el cual se hace saber a las partes los acuerdos, resoluciones y otros actuados dictadas por los órganos jurisdiccionales.", size=14, color="white")
                                                                ]
                                                            )  
                                                        ),
                                                        ft.Container(
                                                            bgcolor=self.bg_color,
                                                            border_radius=15, padding=15,
                                                            content=ft.Column(
                                                                spacing=0, alignment=ft.MainAxisAlignment.START,
                                                                controls=[
                                                                    ft.Text("Notificacion", size=14, color="white", weight="bold"),
                                                                    ft.Divider(height=20, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                                                    ft.Text("Son comunicaciones a través de medios electrónicos y telemáticos de las actuaciones jurisdiccionales, mediante el cual se hace saber a las partes los acuerdos, resoluciones y otros actuados dictadas por los órganos jurisdiccionales.", size=14, color="white")
                                                                ]
                                                            )  
                                                        ),
                                                        ft.Container(
                                                            bgcolor=self.bg_color,
                                                            border_radius=15, padding=15,
                                                            content=ft.Column(
                                                                spacing=0, alignment=ft.MainAxisAlignment.START,
                                                                controls=[
                                                                    ft.Text("Notificacion", size=14, color="white", weight="bold"),
                                                                    ft.Divider(height=20, color=ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                                                                    ft.Text("Son comunicaciones a través de medios electrónicos y telemáticos de las actuaciones jurisdiccionales, mediante el cual se hace saber a las partes los acuerdos, resoluciones y otros actuados dictadas por los órganos jurisdiccionales.", size=14, color="white")
                                                                ]
                                                            )  
                                                        )
                                                    ]
                                                )
                                            )
                                        ]
                                    )
                                )
                            ]
                        ),
                    )

                ]
            )
        )
        
        # --- Contenedor 2: Seccion Buscar ---
        self.container_2 = ft.Container(
            expand=True,
            bgcolor= self.container_color,
            offset= ft.Offset(0,2),
            animate_offset=self.animation_style
        )
        
        # --- Contenedor 3: Seccion Inventario ---
        self.container_3 = ft.Container(
            expand=True,
            #bgcolor= self.container_color,
            offset= ft.Offset(0,2),
            animate_offset=self.animation_style, margin=5,
            content=ft.Row(
                controls=[
                    # --- Barra de Navegacion: Categorias de Articulos
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            controls=[
                                ft.Container(
                                    bgcolor=self.container_color,
                                    height=50,
                                    border_radius=15, padding=5,
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_AROUND, spacing=0,
                                        controls=[
                                            ft.IconButton(
                                                ft.Icons.ARROW_BACK_IOS, 
                                                icon_color="white", 
                                                on_click=lambda e: self.scroll_categories(-100),
                                            ),
                                            ft.Container(
                                                expand=True,
                                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                                content=ft.ListView(
                                                    horizontal=True,
                                                    spacing=5,
                                                    ref=self.category_list_ref,
                                                    controls=[
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.ALL_INBOX, color="white"),
                                                                    ft.Text("Todo", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.LOCAL_GROCERY_STORE, color="white"),
                                                                    ft.Text("Abarrotes", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.LOCAL_BAR, color="white"),
                                                                    ft.Text("Bebidas", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.FASTFOOD, color="white"),
                                                                    ft.Text("Carnes", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.AC_UNIT, color="white"),
                                                                    ft.Text("Congelados", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.WATER_DROP, color="white"),
                                                                    ft.Text("Lacteos y Derivados", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.BAKERY_DINING, color="white"),
                                                                    ft.Text("Panaderia", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.CLEANING_SERVICES, color="white"),
                                                                    ft.Text("Cuidado del Hogar", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.WASH, color="white"),
                                                                    ft.Text("Cuidado Personal", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.TOYS, color="white"),
                                                                    ft.Text("Jugueteria", color="white")
                                                                ]
                                                            )
                                                        ),
                                                        ft.Container(
                                                            padding=10,
                                                            bgcolor=self.color_navegation_bt,
                                                            border_radius=15,
                                                            on_click=lambda e: self.change_page(e, 1),
                                                            height=40,
                                                            content=ft.Row(
                                                                alignment=ft.MainAxisAlignment.CENTER,
                                                                controls=[
                                                                    ft.Icon(Icons.LOCAL_HOSPITAL, color="white"),
                                                                    ft.Text("Farmacia", color="white")
                                                                ]
                                                            )
                                                        )
                                                    ]
                                                )
                                            ),
                                            ft.IconButton(
                                                ft.Icons.ARROW_FORWARD_IOS, 
                                                icon_color="white", 
                                                on_click=lambda e: self.scroll_categories(100),
                                            ),
                                            
                                        ]
                                    )
                                    
                                ),
                                ft.GridView(controls=products,
                                    expand=1,
                                    runs_count=5,
                                    max_extent=200,
                                    child_aspect_ratio=0.8,
                                    spacing=5,
                                    run_spacing=5,
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        bgcolor=self.container_color,
                        width=300, border_radius=15, padding=10,
                        content=ft.Column(
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
                                        ft.Text("Sucursal: Las Brisas", weight="bold", color=self.color_purple),
                                        ft.Text("Orden #23440", weight="bold", color="white")
                                    ],
                                ),
                                ft.Divider(height=1),
                                ft.ListView(expand=True, controls=[
                                    ft.Column([
                                        ft.Row([
                                            ft.Image("\products\img16.png", width=50, height=50),
                                            ft.Column([
                                                ft.Text("Cartulina Oficio", color="white"),
                                                ft.Text("Precio: Bs.38.00", color=self.color_purple)
                                            ]),
                                            ft.Text("Bs.114.00", color=self.color_purple, size=20, weight="bold")
                                        ]),
                                        ft.Row([
                                            ft.Row([
                                                ft.IconButton(icon=ft.Icons.REMOVE, icon_color="white"),
                                                ft.Container(border_radius=3,width=40,height=25,bgcolor=self.bg_color,content=ft.Row([
                                                    ft.Text(5,color="white")
                                                ], alignment=ft.MainAxisAlignment.CENTER)),
                                                ft.IconButton(icon=ft.Icons.ADD, icon_color="white")
                                            ]),
                                            ft.IconButton(icon=ft.Icons.DELETE, icon_color="white")
                                        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)                                         
                                    ]),
                                    ft.Divider(height=1),
                                    ft.Column([
                                        ft.Row([
                                            ft.Image("\products\img13.png", width=50, height=50),
                                            ft.Column([
                                                ft.Text("Lapices Faber Castell", color="white"),
                                                ft.Text("Precio: Bs.10.00", color=self.color_purple)
                                            ]),
                                            ft.Text("Bs.40.00", color=self.color_purple, size=20, weight="bold")
                                        ]),
                                        ft.Row([
                                            ft.Row([
                                                ft.IconButton(icon=ft.Icons.REMOVE, icon_color="white"),
                                                ft.Container(border_radius=3,width=40,height=25,bgcolor=self.bg_color,content=ft.Row([
                                                    ft.Text(5,color="white")
                                                ], alignment=ft.MainAxisAlignment.CENTER)),
                                                ft.IconButton(icon=ft.Icons.ADD, icon_color="white")
                                            ]),
                                            ft.IconButton(icon=ft.Icons.DELETE, icon_color="white")
                                        ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN)                                         
                                    ]),

                                ]),
                                ft.Container(
                                    padding=10,height=210,
                                    content=ft.Column(
                                        controls=[
                                            ft.Divider(height=1),
                                            ft.Row([
                                                ft.Column([
                                                    ft.Text("Total", weight="bold", color="white"),
                                                    ft.Text("Items: 3 Quanty: 6", color=ft.Colors.GREY_400)
                                                ]),
                                                ft.Text("67 Bs", size=30, weight="bold", color=self.color_purple)
                                            ], alignment = ft.MainAxisAlignment.SPACE_BETWEEN),
                                            ft.CupertinoButton("Imprimir Factura", bgcolor= self.color_purple, color=ft.Colors.WHITE, width=300),
                                            ft.CupertinoButton("Metodo de Pago", bgcolor=ft.Colors.GREEN_600,color=ft.Colors.WHITE, width=300),
                                        ]
                                    )
                                )
                            ]
                        )
                    ),
                ]
            )
        )
        
        # --- Contenedor 4: Seccion Personal ---
        self.employee_section_right = emp.EmployeeSectionRight()
        self.employee_section_left = emp.EmployeeSectionLeft(
            on_employee_select=lambda employee: self.employee_section_right.show_employee(employee)
        )

        self.container_4 = ft.Container(
            expand=True,
            bgcolor= self.container_color,
            offset= ft.Offset(0,2),
            animate_offset=self.animation_style,
            content=ft.Row(
                # Secciones de empleados
                controls=[
                    self.employee_section_left,
                    self.employee_section_right,
                ],
                expand=True,
                spacing=5,
            )
        )

        # --- Contenedor 5: Seccion Balance ---
        self.container_5 = ft.Container(
            expand=True,
            bgcolor= self.container_color,
            offset= ft.Offset(0,2),
            animate_offset=self.animation_style
        )

        # --- Contenedor 6: Seccion Ajustes (Por cambiar) ---
        self.container_6 = ft.Container(
            expand=True,
            bgcolor= self.container_color,
            offset= ft.Offset(0,2),
            animate_offset=self.animation_style
        )


        # --- Contenedores: Carga de los contenedores de seccion ---
        self.frame = ft.Container(
            expand= True,
            content= ft.Stack(
                controls=[
                    self.container_1,
                    self.container_2,
                    self.container_3,
                    self.container_4,
                    self.container_5,
                    self.container_6
                ]
            )
        )


        # --- Parte Lateral Derecha: Barra de Busqueda, Secciones ---
        self.main_content = ft.Container(
            expand=True,
            content=ft.Stack(
                controls=[
                    ft.Column(
                        spacing=0,
                        controls=[
                            self.fixed_header,
                            self.frame,
                        ]
                    ),
                    # Contenedor del menú de notificaciones
                    ft.Container(
                        top=60,  
                        right=80, 
                        content=self.notifications_popup
                    )
                ]
            )
        )
        
        # --- Logo: logotipo de la empresa ---
        self.logo = ft.Container(
            content= ft.Column(
                alignment= ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
                controls= [
                    ft.Image(
                        src="Hipermaxi_logo.png",           
                        width=180,            
                        height=100,        
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Text("S U P E R M E R C A D O" , size=18, color="white", text_align=ft.TextAlign.CENTER)
                ]
            )
        )

        # --- Botones Menu lateral: Botones que al presionar cambia entre paginas ---
        self.option_1 = ft.Container(
            padding=10,
            bgcolor=self.color_purple,
            border_radius=15,
            offset=ft.Offset(0,0),
            animate_offset= self.animation_style,
            on_click=lambda e: self.change_page(e, 1),
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(Icons.HOME, color="white"),
                    ft.Text("Inicio", width=120, color="white")
                ]
            )
        )
        self.option_2 = ft.Container(
            padding=10,
            bgcolor=self.color_navegation_bt,
            border_radius=15,
            offset=ft.Offset(0,0),
            animate_offset= self.animation_style,
            on_click=lambda e: self.change_page(e, 2),
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(Icons.SEARCH, color="white"),
                    ft.Text("Buscar", width=120, color="white")
                ]
            )
        )
        self.option_3 = ft.Container(
            padding=10,
            bgcolor=self.color_navegation_bt,
            border_radius=15,
            offset=ft.Offset(0,0),
            animate_offset= self.animation_style,
            on_click=lambda e: self.change_page(e, 3),
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(Icons.INVENTORY, color="white"),
                    ft.Text("Inventario", width=120, color="white")
                ]
            )
        )
        self.option_4 = ft.Container(
            padding=10,
            bgcolor=self.color_navegation_bt,
            border_radius=15,
            offset=ft.Offset(0,0),
            animate_offset= self.animation_style,
            on_click=lambda e: self.change_page(e, 4),
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(Icons.PERSON_ROUNDED, color="white"),
                    ft.Text("Empleados", width=120, color="white")
                ]
            )
        )
        self.option_5 = ft.Container(
            padding=10,
            bgcolor=self.color_navegation_bt,
            border_radius=15,
            offset=ft.Offset(0,0),
            animate_offset= self.animation_style,
            on_click=lambda e: self.change_page(e, 5),
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(Icons.CREDIT_CARD, color="white"),
                    ft.Text("Balance", width=120, color="white")
                ]
            )
        )
        self.option_6 = ft.Container(
            padding=10,
            bgcolor=self.color_navegation_bt,
            border_radius=15,
            offset=ft.Offset(0,0),
            animate_offset= self.animation_style,
            on_click=lambda e: self.change_page(e, 6),
            height=40,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(Icons.SETTINGS, color="white"),
                    ft.Text("Ajustes", width=120, color="white")
                ]
            )
        )
        

        # --- Parte Lateral Izquierdo: Menu Lateral ---
        self.navegation = ft.Container(
            padding=8,
            bgcolor=self.container_color,
            animate_size=self.animation_style,
            content= ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    self.logo,
                    self.option_1,
                    self.option_2,
                    self.option_3,
                    self.option_4,
                    self.option_5,
                    self.option_6
                ]
            )
        )

        #Variable de tipo Diccionario que segun el numero que reciba del metodo change_page cambiara de container
        self.switch_control = {
            1: self.container_1,
            2: self.container_2,
            3: self.container_3,
            4: self.container_4,
            5: self.container_5,
            6: self.container_6
        }

        # Cargar sesión y aplicar permisos basados en rol
        self.apply_permissions()

        #Pagina: Distribuye la interfaz en dos partes
        self.content = ft.Row(
            expand=True,
            spacing=5,
            controls=[
                self.navegation,
                self.main_content,
            ]
        )
    
    # Metodo para ocultar o mostrar las lineas del grafico
    def toggle_chart_visibility(self, e):
        line_name = e.control.text 
        
        line_map = {
            "Línea Ingresos por Ventas": self.green_line_data,
            "Línea Costo de Ventas": self.red_line_data,
            "Línea Utilidad Bruta": self.blue_line_data,
        }
        if line_name == "Mostrar Todo":
            self.green_line_data.visible = True
            self.red_line_data.visible = True
            self.blue_line_data.visible = True
        elif line_name in line_map:
            data_series = line_map[line_name]
            data_series.visible = not data_series.visible
        self.char_data.update()
        self.page.update()

    # Metodo para alternar la visibilidad del menú de notificaciones
    def toggle_notifications(self, e):
        self.notifications_popup.visible = not self.notifications_popup.visible
        self.page.update()

    # Metodo para forzar el cierre del menú de notificaciones
    def hide_notifications(self, e):
        self.notifications_popup.visible = False
        self.page.update()
    
    # Metodo para desplazar las categorías horizontalmente
    def scroll_categories(self, delta: int):
        # Usamos la nueva referencia de ListView
        category_list = self.category_list_ref.current
        
        if category_list:
            # 1. CALCULAMOS EL NUEVO SCROLL USANDO LA POSICIÓN MANUAL
            # No leemos category_list.scroll_offset, usamos nuestra variable
            new_scroll = self.current_scroll_offset + delta
            
            # 2. Aseguramos que el scroll no sea negativo (no podemos desplazarnos antes del inicio)
            if new_scroll < 0:
                new_scroll = 0
            
            # 3. Enviamos el comando de scroll a la nueva posición
            category_list.scroll_to(offset=new_scroll, duration=300)
            
            # 4. ACTUALIZAMOS NUESTRA POSICIÓN MANUAL para el siguiente clic
            self.current_scroll_offset = new_scroll
            
            # Actualiza la página para que se vea el movimiento
            self.page.update()

    def apply_permissions(self):
        """
        Aplica los permisos según el rol del usuario.
        Oculta o deshabilita las opciones de menú que el usuario no puede acceder.
        """
        try:
            # Importar el SessionManager
            import session
            
            # Verificar permisos para cada módulo y ocultar los no permitidos
            if not session.session_manager.has_module_access(4):  # Módulo Empleados
                self.option_4.visible = False
            
            if not session.session_manager.has_module_access(5):  # Módulo Balance
                self.option_5.visible = False
            
            if not session.session_manager.has_module_access(6):  # Módulo Ajustes
                self.option_6.visible = False
            
        except Exception as e:
            print(f"Error al aplicar permisos: {e}")
            # Si hay error, por seguridad ocultamos módulos sensibles
            self.option_4.visible = False
            self.option_5.visible = False
            self.option_6.visible = False

    #Metodo para poder cambiar entre paginas y se vea la seleccion de boton
    def change_page(self, e, n):
        # Verificar permisos antes de cambiar de página
        try:
            import session
            if not session.session_manager.has_module_access(n):
                # Si el usuario no tiene acceso, no hacer nada
                print(f"Acceso denegado al módulo {n}")
                return
        except Exception as e:
            print(f"Error al verificar permisos: {e}")
            return

        #El for recorre las claves del diccionario (1, 2, 3, 4)
        for page in self.switch_control:
            self.switch_control[page].offset.y = 2
            self.option_1.bgcolor = self.color_navegation_bt
            self.option_2.bgcolor = self.color_navegation_bt
            self.option_3.bgcolor = self.color_navegation_bt
            self.option_4.bgcolor = self.color_navegation_bt
            self.option_5.bgcolor = self.color_navegation_bt
            self.option_6.bgcolor = self.color_navegation_bt
        if n == 1:
            self.option_1.offset.x = 0.05
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0
            self.option_5.offset.x = 0
            self.option_6.offset.x = 0
            self.option_1.bgcolor = self.color_purple
            self.option_1.update()
        elif n == 2:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0.05
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0
            self.option_5.offset.x = 0
            self.option_6.offset.x = 0
            self.option_2.bgcolor = self.color_purple
            self.option_2.update()
        elif n == 3:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0.05
            self.option_4.offset.x = 0
            self.option_5.offset.x = 0
            self.option_6.offset.x = 0
            self.option_3.bgcolor = self.color_purple
            self.option_3.update()
        elif n == 4:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0.05
            self.option_5.offset.x = 0
            self.option_6.offset.x = 0
            self.option_4.bgcolor = self.color_purple
            self.option_4.update()
        elif n == 5:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0
            self.option_5.offset.x = 0.05
            self.option_6.offset.x = 0
            self.option_5.bgcolor = self.color_purple
            self.option_5.update()
        elif n == 6:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0
            self.option_5.offset.x = 0
            self.option_6.offset.x = 0.05
            self.option_6.bgcolor = self.color_purple
            self.option_6.update()
        self.switch_control[n].offset.y = 0
        self.page.update()


#Arrancamos el programa y indicamos que se ejecute la clase "UIAPP" para mostrar la interfaz
#? "assets_dir = assets" se usa para indicar en que carpeta se buscara imagenes, etc
#ft.app(target=lambda page:UIApp(page), assets_dir="assets")