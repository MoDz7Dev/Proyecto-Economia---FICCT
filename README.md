# Hipermaxi - Gestor Administrativo

Aplicacion hecha con **Flet** (Python) + una **API** local en **FastAPI**.
Incluye: Login, Inventario (carrito y metodo de pago), Busqueda, Empleados,
Balance y Ajustes.

## Estructura del proyecto

```
Proyecto-Economia---FICCT/
├── run.py                  # Punto de entrada: levanta la API y abre la app
├── requirements.txt
├── iniciar.bat             # Lanzador para Windows (doble clic)
├── assets/                 # Imagenes y logos (lo que Flet carga)
├── storage/                # Datos de ejecucion (sesion del usuario)
├── src/
│   ├── config.py           # Paleta de colores y constantes
│   ├── core/               # Logica de negocio (sin UI)
│   │   └── session.py
│   ├── api/                # Servidor FastAPI
│   │   └── server.py
│   ├── data/               # Datos (productos y usuarios)
│   │   └── diccionario.py
│   └── ui/                 # Interfaz Flet
│       ├── app.py          # Construccion de la app (main)
│       ├── login.py
│       ├── main_view.py    # Ventana principal (UIApp)
│       ├── components/     # Widgets reutilizables
│       │   ├── product_card.py
│       │   ├── category_bar.py
│       │   └── shopping_cart.py
│       └── sections/       # Secciones de la app
│           ├── inventory_section.py
│           ├── employee_section.py
│           ├── balance_section.py
│           ├── search_section.py
│           └── settings_section.py
└── tests/
    ├── test_carrito.py
    └── test_categorias.py
```

## Requisitos

- Python 3.10+ (probado con 3.14)
- Windows

## Instalacion

```powershell
python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt
```

> **Importante:** el proyecto usa **Flet 0.28.3**. No instales `flet` sin
> version, porque la 1.0.x rompe la app.

## Ejecucion

Desde la **raiz** del proyecto:

```powershell
venv\Scripts\python run.py
```

o doble clic en **`iniciar.bat`**.

Esto levanta la API en `http://127.0.0.1:8000` y abre la app en
`http://127.0.0.1:8080`.

### Usuarios de prueba

| Usuario    | Contrasena | Rol        |
|------------|------------|------------|
| admin      | admin123   | admin      |
| supervisor | super123   | supervisor |
| almacen    | alma123    | warehouse  |

## Notas

- Ejecuta siempre desde la **raiz** del proyecto (las rutas `assets/` y
  `storage/` son relativas).
- La app corre en el navegador (Flet `WEB_BROWSER`).
