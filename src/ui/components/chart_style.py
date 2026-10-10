"""Estilo compartido para las graficas de lineas.

Reune la paleta de colores y los ayudantes que dan a las graficas el aspecto
de "curvas luminosas": trazo con brillo, degradado bajo la curva, rejilla y
puntos resaltados al pasar el mouse por encima.
"""
import flet as ft

# --- Paleta viva de las curvas ---
GREEN = "#22c55e"
RED = "#ef4444"
BLUE = "#38bdf8"
CYAN = "#22d3ee"
ORANGE = "#fb923c"
YELLOW = "#facc15"

# Fondo oscuro del area de la grafica
CHART_BG = "#0e1b2e"

# Colores de la rejilla y de los bordes suaves
GRID_COLOR = ft.Colors.with_opacity(0.10, ft.Colors.WHITE)
BORDER_COLOR = ft.Colors.with_opacity(0.35, ft.Colors.WHITE)

# Meses del anio usados por el eje X del Estado de Resultados
MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
          "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def grid_lines(interval, color=GRID_COLOR, width=1):
    """Lineas de rejilla (horizontales o verticales) del area de la grafica."""
    return ft.ChartGridLines(interval=interval, color=color, width=width)


def fill_gradient(color, opacity=0.45):
    """Degradado que rellena el area bajo la curva y se desvanece hacia abajo."""
    return ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
        colors=[
            ft.Colors.with_opacity(opacity, color),
            ft.Colors.with_opacity(0.0, color),
        ],
    )


def dot(color, radius=2.6):
    """Punto pequenio dibujado sobre cada valor de la serie."""
    return ft.ChartCirclePoint(radius=radius, color=color, stroke_width=0)


def glow_dot(color, radius=3.6, halo=6):
    """Punto luminoso: circulo blanco con un halo del color de la curva."""
    return ft.ChartCirclePoint(
        radius=radius,
        color=ft.Colors.WHITE,
        stroke_color=ft.Colors.with_opacity(0.35, color),
        stroke_width=halo,
    )


def line_glow(color, blur=14, opacity=0.55):
    """Sombra que hace que la curva parezca iluminada."""
    return ft.BoxShadow(
        blur_radius=blur,
        color=ft.Colors.with_opacity(opacity, color),
        offset=ft.Offset(0, 0),
    )


def border_axes():
    """Borde inferior e izquierdo del area de la grafica (estilo de las curvas)."""
    return ft.border.only(
        left=ft.BorderSide(1, BORDER_COLOR),
        bottom=ft.BorderSide(1, BORDER_COLOR),
    )
