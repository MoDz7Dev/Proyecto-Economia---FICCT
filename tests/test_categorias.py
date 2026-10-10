"""Prueba del filtrado por categoria.

Requiere el servidor de la API corriendo en http://127.0.0.1:8000
(lo levanta run.py / iniciar.bat).

Ejecutar desde la raiz:   python -m tests.test_categorias
"""
from src.ui.sections.inventory_section import InventorySection


def test_filtrado():
    sec = InventorySection(page=None)
    sec.update_products_grid = lambda: None  # no hay pagina real

    esperado = {
        "all": 18,
        "Abarrotes": 5,
        "Papelería": 6,
        "Cuidado del Hogar": 5,
        "Carnes": 1,
        "Bebidas": 1,
        "Juguetería": 0,
    }
    for cat, exp in esperado.items():
        sec.filter_by_category(cat)
        got = len(sec.filtered_products)
        assert got == exp, f"{cat}: esperado {exp}, obtenido {got}"
    print("test_filtrado OK")


if __name__ == "__main__":
    test_filtrado()
    print("TODOS LOS TESTS OK")
