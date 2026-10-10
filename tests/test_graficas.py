"""Pruebas de las graficas: meses del anio y estilo de curvas luminosas.

Ejecutar desde la raiz:   python -m tests.test_graficas
"""
import flet as ft

from src.ui.main_view import build_results_chart
from src.ui.sections.inventory_section import build_equilibrium_chart


MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


def test_meses_estado_resultados():
    chart = build_results_chart()
    etiquetas = [l.label.value for l in chart.bottom_axis.labels]
    assert etiquetas == MESES, etiquetas
    assert [l.value for l in chart.bottom_axis.labels] == list(range(1, 13))
    assert len(chart.data_series) == 3
    print("test_meses_estado_resultados OK")


def test_estilo_curvas_luminosas():
    chart = build_results_chart()
    assert chart.interactive is True
    for serie in chart.data_series:
        assert serie.curved is True
        assert serie.below_line_gradient is not None
        assert isinstance(serie.point, ft.ChartCirclePoint)
        assert isinstance(serie.selected_point, ft.ChartCirclePoint)
        assert serie.selected_point.color == ft.Colors.WHITE
        assert serie.shadow is not None
    print("test_estilo_curvas_luminosas OK")


def test_etiquetas_equilibrio():
    chart = build_equilibrium_chart()
    etiquetas = {l.value: l.label.value for l in chart.right_axis.labels}
    assert etiquetas == {0: "Demanda", 45: "Oferta"}, etiquetas
    assert chart.bottom_axis.title.value == "Precio (Px)"
    assert chart.left_axis.title.value == "Cantidad (Qx)"
    print("test_etiquetas_equilibrio OK")


def test_punto_equilibrio_luminoso():
    chart = build_equilibrium_chart()
    equilibrio = chart.data_series[2]
    assert isinstance(equilibrio.point, ft.ChartCirclePoint)
    assert equilibrio.point.color == ft.Colors.WHITE
    punto = equilibrio.data_points[0]
    assert (punto.x, punto.y) == (40.0, 20.0)
    print("test_punto_equilibrio_luminoso OK")


if __name__ == "__main__":
    test_meses_estado_resultados()
    test_estilo_curvas_luminosas()
    test_etiquetas_equilibrio()
    test_punto_equilibrio_luminoso()
    print("TODOS LOS TESTS OK")
