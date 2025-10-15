#Importamos la libreria Flet para la interfaz grafica
import flet as ft
from flet import Icons

#Definimos la clase principal
class UIApp(ft.Container):
    #Constructor: Inicializa la pagina y define los colores base
    def __init__(self, page: ft.Page):
        super().__init__(expand = True)
        
        print("Window type:", page.platform) #? Imprime en que plataforma esta corriendo la ventana
        self.page = page
        self.page.padding = 0
        self.page.window_icon = "Hipermaxi_logo.png"  # o "ruta/icono.png"
        
        

        #Definimos paleta de colores
        self.color_blue = "#73bf16"
        self.color_purple = "#cf672b"
        self.bg_color = "#483e70"
        self.container_color = "#362e57"
        self.color_navegation_bt = "#2a2949"
        self.color1_card = "#e3501b"
        self.color2_card = "#d6820c"

        self.page.bgcolor = self.bg_color



        #Estilo de animacion para transiciones y efectos
        self.animation_style = ft.Animation(500, ft.AnimationCurve.EASE_IN_TO_LINEAR)

        #Grafica de curva de demanda y oferta
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
            for i in range(1, 16, 3) # Genera 1, 4, 7, 10, 13
        ]

        green_line = [1.2, 1.5, 2.0, 8, 3.2, 5, 2.0, 2.5, 5, 10, 2.1, 4, 2.0, 6, 1.7]
        red_line = [1.8, 8, 1.5, 7, 1.6, 1.8, 2.0, 10, 1.8, 3, 2.0, 2.2, 5, 2.0, 9]

        #!bottom_axis = ft.ChartAxis(labels_size=25, labels_interval=3, show_labels=True) -- Sirve pero no encuentro metodo para cambiar de color los numeros
        bottom_axis = ft.ChartAxis(labels_size=25, labels=x_labels, show_labels=True)
        left_axis = ft.ChartAxis(labels_size=25, labels=y_labels, show_labels=True)

        self.char_data = ft.LineChart(
            tooltip_bgcolor="transparent",
            data_series=[
                ft.LineChartData(
                    data_points=[ft.LineChartDataPoint(x, y, selected=(x==8)) for x, y in zip(x_values, green_line)],
                    color="green",
                    stroke_width=1,
                    curved=True,
                    below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.GREEN),
                    
                ),
                ft.LineChartData(
                    data_points=[ft.LineChartDataPoint(x, y, selected=(x==8)) for x, y in zip(x_values, red_line)],
                    color="red",
                    stroke_width=1,
                    curved=True,
                    below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.RED)
                )
            ],
            min_y=0, max_y=10,
            expand=True,
            border=ft.Border(
                bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
                left=ft.BorderSide(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
            ),
            bottom_axis=bottom_axis,
            left_axis=left_axis
        )


        self.container_1 = ft.Container(
            expand=True,
            #bgcolor= self.container_color,
            offset= ft.Offset(0,0),
            animate_offset=self.animation_style,
            margin=10, border_radius=10,
            content= ft.Row(
                controls=[
                    #Parte Izquierda de la seccion Principal
                    ft.Container(
                        expand= True,
                        content= ft.Stack(
                            alignment=ft.alignment.top_center,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    bgcolor=self.container_color,
                                    margin= ft.margin.only(left= 0, top = 150, right=0, bottom=0),
                                    padding= ft.padding.only(left=0, top = 100, right=0, bottom=0),
                                    border_radius=20,  
                                    content = ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("Transferencia", color="white", size=20, weight="bold"),
                                            ft.Tabs(
                                                tab_alignment=ft.TabAlignment.CENTER,
                                                indicator_color=self.color_purple,
                                                label_color="white", unselected_label_color="white",
                                                indicator_tab_size=True,
                                                expand=True,
                                                tabs=[
                                                    ft.Tab(
                                                        "Enviar", 
                                                        content= ft.Container(
                                                            padding=20,
                                                            content=ft.Column(
                                                                spacing=10,
                                                                controls=[
                                                                    ft.Text("Pagar Ahora", color="white", size=15),
                                                                    ft.TextField(
                                                                        expand=True,
                                                                        border_color= "transparent",
                                                                        border_radius=10,
                                                                        bgcolor= self.color_navegation_bt,
                                                                        color="white",
                                                                        hint_style=ft.TextStyle(color="white")
                                                                    ),
                                                                    ft.Row(
                                                                        controls=[
                                                                            ft.Column(
                                                                                expand=True,
                                                                                controls=[
                                                                                    ft.Text("Cantidad", color="white", size=15),
                                                                                    ft.TextField(
                                                                                        expand=True,
                                                                                        border_color= "transparent",
                                                                                        border_radius=10,
                                                                                        bgcolor= self.color_navegation_bt,
                                                                                        color="white",
                                                                                        hint_style=ft.TextStyle(color="white")
                                                                                    )
                                                                                ]
                                                                            ),
                                                                            ft.Column(
                                                                                expand=True,
                                                                                controls=[
                                                                                    ft.Text("Comentario", color="white", size=15),
                                                                                    ft.TextField(
                                                                                        expand=True,
                                                                                        border_color= "transparent",
                                                                                        border_radius=10,
                                                                                        bgcolor= self.color_navegation_bt,
                                                                                        color="white",
                                                                                        hint_style=ft.TextStyle(color="white")
                                                                                    )
                                                                                ]
                                                                            )
                                                                        ]
                                                                    ),
                                                                    ft.Row(
                                                                        expand=True,
                                                                        controls=[
                                                                            ft.Text("Comision: Bs 2.00", color="white", size=15),
                                                                            ft.Text("Total: Bs 502.00", color="white", size=15),
                                                                        ]
                                                                    ),
                                                                    ft.Column(
                                                                        controls=[
                                                                            ft.Container(
                                                                                height=50,
                                                                                border_radius=20,
                                                                                bgcolor= self.bg_color,
                                                                                content=ft.Row(
                                                                                    alignment=ft.MainAxisAlignment.CENTER,
                                                                                    controls=[
                                                                                        ft.Icon(Icons.SEND, color="white"),
                                                                                        ft.Text("Enviar", color="white")
                                                                                    ]
                                                                                )
                                                                            )
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        )
                                                    ),
                                                    ft.Tab("Aplicar para")
                                                ]
                                            )
                                        ]
                                    )                              
                                ),
                                ft.Container(
                                    height=180,
                                    width=320,
                                    gradient=ft.LinearGradient(
                                        rotation = 0.5,
                                        colors = [
                                            self.color_purple
                                        ]
                                    ),
                                    margin=ft.margin.only(left = 50, top = 50, right=50, bottom = 0),
                                    border_radius=20,
                                    padding=10,
                                    content=ft.Column(
                                        alignment= ft.CrossAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text("ESTADO DE RESULTADOS   MENSUAL", color= "white", size=17, text_align=ft.TextAlign.CENTER, weight="bold"),
                                            ft.Row(
                                                alignment=ft.CrossAxisAlignment.START,
                                                controls=[
                                                    ft.Container(
                                                        border_radius=10,
                                                        bgcolor=ft.Colors.with_opacity(0.3, self.bg_color),
                                                        width=40,
                                                        height=40,
                                                        alignment=ft.alignment.center,
                                                        content= ft.Icon(Icons.ARROW_UPWARD, color="white")
                                                    ),
                                                    ft.Text("Bs 100,272.50", color= "white", size=22,),
                                                ]
                                            ),
                                            ft.Row(
                                                alignment=ft.CrossAxisAlignment.START,
                                                controls=[
                                                    ft.Container(
                                                        border_radius=10,
                                                        bgcolor=ft.Colors.with_opacity(0.3, self.bg_color),
                                                        width=40,
                                                        height=40,
                                                        alignment=ft.alignment.center,
                                                        content= ft.Icon(Icons.ARROW_DOWNWARD, color="white")
                                                    ),
                                                    ft.Text("Bs 50,342.00", color= "white", size=22,)
                                                ]
                                            )
                                        ]
                                    )
                                )
                                
                            ]
                        )
                    ),
                    #Parte Derecha de la seccion principal
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                     height=50,
                                    controls=[
                                    # --- Campo de busqueda ---
                                    ft.Container(
                                        expand=True,
                                        border_radius=20,
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
                                ),
                                ft.Container(
                                    bgcolor=self.container_color, padding=20,
                                    expand=True,border_radius=20,
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Diferencia", color="white", size=16, weight="bold"),
                                                    ft.Text("$ 18,920", size=15, weight="bold", color="white")
                                                ]
                                            ),
                                            self.char_data
                                        ]
                                    )
                                ),
                                ft.Container(
                                    expand=True,
                                    bgcolor= self.container_color,
                                    border_radius=20, padding=20,
                                    content=ft.Column(
                                        expand=True,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Informacion", size=16, weight="bold", color="white"),
                                                    ft.IconButton(ft.Icons.EDIT, icon_color="white"),
                                                ]
                                            ),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.START,
                                                controls=[
                                                    ft.IconButton(ft.Icons.LOCATION_CITY, icon_color="white"),
                                                    ft.Text("Lugar: Santa Cruz", size=16, color="white"),
                                                ]
                                            ),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.START,
                                                controls=[
                                                    ft.IconButton(ft.Icons.LOCATION_ON_OUTLINED, icon_color="white"),
                                                    ft.Text("Direccion: 2do Anillo/Las Brisas", size=16, color="white"),
                                                ]
                                            ),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.START,
                                                controls=[
                                                    ft.IconButton(ft.Icons.CREDIT_CARD, icon_color="white"),
                                                    ft.Text("Balance: Bs100, 223.00", size=16, color="white"),
                                                ]
                                            )
                                        ]
                                    )
                                ),
                                ft.Container(
                                    expand=True,
                                    bgcolor=self.container_color,
                                    border_radius=20,
                                    padding=20,
                                    content= ft.Column(
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                                controls=[
                                                    ft.Text("Seguridad", color="white", size=16, weight="Bold"),
                                                    ft.IconButton(ft.Icons.MORE_HORIZ,icon_color="white")
                                                ]
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
        
        self.container_2 = ft.Container(
            expand=True,
            bgcolor= self.container_color,
            offset= ft.Offset(2,0),
            animate_offset=self.animation_style
        )
        
        self.container_3 = ft.Container(
            expand=True,
            bgcolor= self.container_color,
            offset= ft.Offset(2,0),
            animate_offset=self.animation_style
        )
        
        self.container_4 = ft.Container(
            expand=True,
            bgcolor= self.container_color,
            offset= ft.Offset(2,0),
            animate_offset=self.animation_style
        )

        self.frame = ft.Container(
            expand= True,
            content= ft.Stack(
                controls=[
                    self.container_1,
                    self.container_2,
                    self.container_3,
                    self.container_4
                ]
            )
        )

        #Logo: logotipo de la empresa
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
                    ft.Text("L A S  B R I S A S" , size=18, color="white", text_align=ft.TextAlign.CENTER)
                ]
            )
        )

        #Botones Menu lateral: Botones que al presionar cambia entre paginas
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
                    ft.Icon(Icons.SETTINGS, color="white"),
                    ft.Text("Ajustes", width=120, color="white")
                ]
            )
        )

        #Menu: Lateral Izquierdo
        self.navegation = ft.Container(
            padding=20,
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
                    self.option_4
                ]
            )
        )

        #Variable de tipo Diccionario que segun el numero que reciba del metodo change_page cambiara de container
        self.switch_control = {
            1: self.container_1,
            2: self.container_2,
            3: self.container_3,
            4: self.container_4
        }

        #Pagina: Distribuye la interfaz en dos partes
        self.page.add(
            ft.Row(
                expand=True,
                spacing=5,
                controls=[
                    self.navegation,
                    self.frame,
                ]

            )
        )
    
    #Metodo para poder cambiar entre paginas y se vea la seleccion de boton
    def change_page(self, e, n):
        #El for recorre las claves del diccionario (1, 2, 3, 4)
        for page in self.switch_control:
            self.switch_control[page].offset.y = 2
            self.option_1.bgcolor = self.color_navegation_bt
            self.option_2.bgcolor = self.color_navegation_bt
            self.option_3.bgcolor = self.color_navegation_bt
            self.option_4.bgcolor = self.color_navegation_bt
        if n == 1:
            self.option_1.offset.x = 0.05
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0
            self.option_1.bgcolor = self.color_purple
            self.option_1.update()
        elif n == 2:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0.05
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0
            self.option_2.bgcolor = self.color_purple
            self.option_2.update()
        elif n == 3:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0.05
            self.option_4.offset.x = 0
            self.option_3.bgcolor = self.color_purple
            self.option_3.update()
        elif n == 4:
            self.option_1.offset.x = 0
            self.option_2.offset.x = 0
            self.option_3.offset.x = 0
            self.option_4.offset.x = 0.05
            self.option_4.bgcolor = self.color_purple
            self.option_4.update()
        self.page.update()


#Arrancamos el programa y indicamos que se ejecute la clase "UIAPP" para mostrar la interfaz
ft.app(target=lambda page:UIApp(page), assets_dir="assets")