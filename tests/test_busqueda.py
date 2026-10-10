"""Pruebas de la busqueda global de la barra superior.

Ejecutar desde la raiz:   python -m tests.test_busqueda
"""
import flet as ft

from src.ui.main_view import UIApp


class _Offset:
    def __init__(self):
        self.y = 2


class _SectionProducts:
    def __init__(self):
        self.all_products = [
            {"id": 1, "name": "Jamon Sandwichero Sofia 1 kg",
             "category": "Carnes", "code": "223041556", "saleprice": 24.99},
            {"id": 13, "name": "Lapices de Colores Faber Castell",
             "category": "Papelería", "code": "999", "saleprice": 24.99},
        ]
        self.details_opened = []

    def show_product_details(self, product):
        self.details_opened.append(product)


class _SectionEmployees:
    def __init__(self):
        self.all_employees = [
            {"name": "Carlos Rodríguez", "user": "admin",
             "role": "admin", "department": "Gerencia"},
            {"name": "María López", "user": "supervisor",
             "role": "supervisor", "department": "Supervisión"},
        ]
        self.selected = []

    def handle_employee_select(self, employee):
        self.selected.append(employee)


class _Dummy:
    color_purple = "#cf672b"
    color_blue = "#73bf16"
    color1_card = "#e3501b"


def _container():
    return type("C", (), {"offset": _Offset()})()


def _make_dummy():
    d = _Dummy()
    d.inventory_section = _SectionProducts()
    d.employee_section_left = _SectionEmployees()
    d.container_3 = _container()
    d.container_4 = _container()
    d.search_popup = ft.Container(visible=True, content=ft.Column(controls=[]))
    d.global_search_ref = ft.Ref[ft.TextField]()
    d.global_search_ref.current = ft.TextField(value="")
    d.page = type("P", (), {"update": lambda self: None})()

    def fake_change_page(e, n):
        (d.container_3 if n == 3 else d.container_4).offset.y = 0

    d.change_page = fake_change_page
    d._search_result_row = UIApp._search_result_row.__get__(d)
    d._go_to_product = UIApp._go_to_product.__get__(d)
    d._go_to_employee = UIApp._go_to_employee.__get__(d)
    return d


def test_resultados():
    d = _make_dummy()

    controles = UIApp._build_search_results(d, "jamon")
    textos = [c.value for c in controles if isinstance(c, ft.Text)]
    assert "Productos" in textos, textos
    assert "Empleados" not in textos

    controles = UIApp._build_search_results(d, "maría")
    textos = [c.value for c in controles if isinstance(c, ft.Text)]
    assert "Empleados" in textos, textos
    assert "Productos" not in textos

    controles = UIApp._build_search_results(d, "zzzz")
    assert len(controles) == 1

    # buscar por categoria
    controles = UIApp._build_search_results(d, "papelería")
    textos = [c.value for c in controles if isinstance(c, ft.Text)]
    assert "Productos" in textos
    print("test_resultados OK")


def test_navegacion_producto():
    d = _make_dummy()
    prod = d.inventory_section.all_products[0]
    UIApp._go_to_product(d, prod)
    assert d.search_popup.visible is False
    assert d.inventory_section.details_opened == [prod]
    print("test_navegacion_producto OK")


def test_navegacion_empleado():
    d = _make_dummy()
    empl = d.employee_section_left.all_employees[0]
    UIApp._go_to_employee(d, empl)
    assert d.search_popup.visible is False
    assert d.employee_section_left.selected == [empl]
    print("test_navegacion_empleado OK")


if __name__ == "__main__":
    test_resultados()
    test_navegacion_producto()
    test_navegacion_empleado()
    print("TODOS LOS TESTS OK")
