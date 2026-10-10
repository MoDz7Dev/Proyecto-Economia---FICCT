"""Pruebas de humo del carrito y de la barra de categorias (no requiere servidor).

Ejecutar desde la raiz:   python -m tests.test_carrito
"""
from src import config as cfg
from src.ui.components.shopping_cart import ShoppingCart
from src.ui.components.category_bar import CategoryBar


def test_carrito():
    cart = ShoppingCart()
    cart.update = lambda: None  # neutraliza self.update() (no hay pagina)

    p1 = {"id": 1, "name": "Producto A", "saleprice": 10.0, "image": ""}
    p2 = {"id": 2, "name": "Producto B", "saleprice": 5.5, "image": ""}
    cart.add_product(p1)
    cart.add_product(p1)   # mismo producto -> sube cantidad
    cart.add_product(p2)

    assert len(cart.cart_items) == 2
    assert cart.cart_items[0]["quantity"] == 2

    total = sum(cart._to_float(i["product"]["saleprice"]) * i["quantity"] for i in cart.cart_items)
    assert abs(total - 25.5) < 1e-9

    cart.decrease_quantity(0)   # 2 -> 1
    assert cart.cart_items[0]["quantity"] == 1
    cart.decrease_quantity(0)   # 1 -> se elimina
    assert len(cart.cart_items) == 1

    cart.remove_product(0)
    assert len(cart.cart_items) == 0
    print("test_carrito OK")


def test_categoria_seleccionada():
    bar = CategoryBar(on_category_change=None)
    bar.update = lambda: None
    assert bar.category_buttons["all"].bgcolor == cfg.COLOR_PURPLE

    bar.handle_category_click("Papelería")
    assert bar.category_buttons["Papelería"].bgcolor == cfg.COLOR_PURPLE
    assert bar.category_buttons["all"].bgcolor == cfg.COLOR_NAVEGATION_BT
    print("test_categoria_seleccionada OK")


if __name__ == "__main__":
    test_carrito()
    test_categoria_seleccionada()
    print("TODOS LOS TESTS OK")
