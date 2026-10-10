
products_data = [
    {
        'id': 1,
        'name': "Jamon Sandwichero Sofia 1 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img.png",
        'category' : 'Carnes',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 2,
        'name': "Achocolatado Chocolike 1 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img2.png",
        'category' : 'Abarrotes',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 3,
        'name': "Aceite Fino Light 4.5 L",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img3.png",
        'category' : 'Abarrotes',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 4,
        'name': "Te Windsor Canela 130 Sobres",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img4.png",
        'category' : 'Bebidas',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 5,
        'name': "Azucar Guabira Blanca 1 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img5.png",
        'category' : 'Abarrotes',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 6,
        'name': "Mayonesa Kris Limon 485 ml",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img7.png",
        'category' : 'Abarrotes',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 7,
        'name': "Ketchup Kris Original 200 gr",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img8.png",
        'category' : 'Abarrotes',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 8,
        'name': "Papel Higienico Nacional Clasico Celeste",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img6.png",
        'category' : 'Cuidado del Hogar',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 9,
        'name': "Lavavajilla Todo Brillo Limon Verde Doypack",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img9.png",
        'category' : 'Cuidado del Hogar',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 10,
        'name': "Detergente Polvo Omo Limon 4.8 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img10.png",
        'category' : 'Cuidado del Hogar',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 11,
        'name': "Pinza Ropa Rey Gigante 24 un",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img11.png",
        'category' : 'Cuidado del Hogar',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 12,
        'name': "Lavandina Sapolio 1 L",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img12.png",
        'category' : 'Cuidado del Hogar',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 13,
        'name': "Lapices de Colores Faber Castell 12 Colores + 2 Lapices",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img13.png",
        'category' : 'Papelería',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 14,
        'name': "Cartulina Blanca Pliego",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img14.png",
        'category' : 'Papelería',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 15,
        'name': "Acrilex Opaco Surtido",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img15.png",
        'category' : 'Papelería',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 16,
        'name': "Cartulina Oficio 10 un",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img16.png",
        'category' : 'Papelería',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 17,
        'name': "Hoja Papel Bond Chamex Carta 500 Hojas",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img17.png",
        'category' : 'Papelería',
        'stock' : '40',
        'code' : '223041556'
    },
    {
        'id': 18,
        'name': "Libro Infantil Lexus",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img18.png",
        'category' : 'Papelería',
        'stock' : '40',
        'code' : '223041556'
    }
]

# ==================== DATOS: EMPLEADOS CON ROLES ====================

staff_users = [
    # Gerente General
    {
        'ci': 1001,
        'user': "admin",
        'password': "admin123",
        'email': "carlos.rodriguez@hipermaxi.com",
        'name': "Carlos Rodríguez",
        'contact': "78899111",
        'status': "active",
        'role': "admin",
        'department': "Gerencia",
        'hire_date': "2020-01-15"
    },
    # Subgerente
    {
        'ci': 1002,
        'user': "supervisor",
        'password': "super123",
        'email': "maria.lopez@hipermaxi.com",
        'name': "María López",
        'contact': "78899222",
        'status': "active",
        'role': "supervisor",
        'department': "Supervisión",
        'hire_date': "2020-03-20"
    },
    # Jefe de Almacén
    {
        'ci': 1003,
        'user': "almacen",
        'password': "alma123",
        'email': "juan.perez@hipermaxi.com",
        'name': "Juan Pérez",
        'contact': "78899333",
        'status': "active",
        'role': "warehouse_manager",
        'department': "Almacén",
        'hire_date': "2021-05-10"
    },
    # Contador
    {
        'ci': 1004,
        'user': "contador",
        'password': "cont123",
        'email': "ana.garcia@hipermaxi.com",
        'name': "Ana García",
        'contact': "78899444",
        'status': "active",
        'role': "accountant",
        'department': "Contabilidad",
        'hire_date': "2021-08-01"
    },
    # Encargado de Inventario
    {
        'ci': 1005,
        'user': "inventario",
        'password': "inv123",
        'email': "pedro.martinez@hipermaxi.com",
        'name': "Pedro Martínez",
        'contact': "78899555",
        'status': "active",
        'role': "inventory_staff",
        'department': "Almacén",
        'hire_date': "2022-01-15"
    },
    # Cajero
    {
        'ci': 1006,
        'user': "cajero1",
        'password': "caj123",
        'email': "lucia.fernandez@hipermaxi.com",
        'name': "Lucía Fernández",
        'contact': "78899666",
        'status': "active",
        'role': "cashier",
        'department': "Ventas",
        'hire_date': "2022-06-20"
    },
    # Personal de Reposición
    {
        'ci': 1007,
        'user': "reposicion1",
        'password': "rep123",
        'email': "miguel.santos@hipermaxi.com",
        'name': "Miguel Santos",
        'contact': "78899777",
        'status': "active",
        'role': "stock_clerk",
        'department': "Almacén",
        'hire_date': "2023-02-10"
    }
]

# ==================== CONFIGURACIÓN DE ROLES Y PERMISOS ====================

ROLES_CONFIG = {
    "admin": {
        "name": "Gerente General / Administrador",
        "level": 1,
        "permissions": {
            "dashboard": {"read": True, "write": True},
            "search": {"read": True, "write": True},
            "inventory": {"read": True, "write": True, "delete": True},
            "sales": {"read": True, "write": True, "refund": True},
            "employees": {"read": True, "write": True, "delete": True},
            "finance": {"read": True, "write": True},
            "reports": {"read": True, "write": True, "export": True},
            "notifications": {"read": True, "write": True},
            "settings": {"read": True, "write": True}
        }
    },
    "supervisor": {
        "name": "Subgerente / Supervisor de Turno",
        "level": 2,
        "permissions": {
            "dashboard": {"read": "operational", "write": False},
            "search": {"read": True, "write": False},
            "inventory": {"read": True, "write": False, "delete": False},
            "sales": {"read": True, "write": True, "refund": True},
            "employees": {"read": True, "write": False, "delete": False},
            "finance": {"read": False, "write": False},
            "reports": {"read": True, "write": False, "export": False},
            "notifications": {"read": "operational", "write": False},
            "settings": {"read": False, "write": False}
        }
    },
    "warehouse_manager": {
        "name": "Jefe de Almacén",
        "level": 2,
        "permissions": {
            "dashboard": {"read": "inventory_only", "write": False},
            "search": {"read": True, "write": False},
            "inventory": {"read": True, "write": True, "delete": True},
            "sales": {"read": False, "write": False, "refund": False},
            "employees": {"read": False, "write": False, "delete": False},
            "finance": {"read": False, "write": False},
            "reports": {"read": "inventory_only", "write": True, "export": True},
            "notifications": {"read": "stock_alerts", "write": False},
            "settings": {"read": False, "write": False}
        }
    },
    "accountant": {
        "name": "Contador / Asistente Contable",
        "level": 2,
        "permissions": {
            "dashboard": {"read": "sales_data", "write": False},
            "search": {"read": True, "write": False},
            "inventory": {"read": True, "write": False, "delete": False},
            "sales": {"read": True, "write": False, "refund": False},
            "employees": {"read": False, "write": False, "delete": False},
            "finance": {"read": True, "write": True},
            "reports": {"read": True, "write": True, "export": True},
            "notifications": {"read": False, "write": False},
            "settings": {"read": False, "write": False}
        }
    },
    "inventory_staff": {
        "name": "Encargado de Inventario",
        "level": 3,
        "permissions": {
            "dashboard": {"read": False, "write": False},
            "search": {"read": True, "write": False},
            "inventory": {"read": True, "write": True, "delete": False},
            "sales": {"read": False, "write": False, "refund": False},
            "employees": {"read": False, "write": False, "delete": False},
            "finance": {"read": False, "write": False},
            "reports": {"read": "inventory_only", "write": False, "export": False},
            "notifications": {"read": "stock_alerts", "write": False},
            "settings": {"read": False, "write": False}
        }
    },
    "cashier": {
        "name": "Cajero",
        "level": 3,
        "permissions": {
            "dashboard": {"read": False, "write": False},
            "search": {"read": "products_only", "write": False},
            "inventory": {"read": "prices_only", "write": False, "delete": False},
            "sales": {"read": True, "write": True, "refund": False},
            "employees": {"read": False, "write": False, "delete": False},
            "finance": {"read": False, "write": False},
            "reports": {"read": False, "write": False, "export": False},
            "notifications": {"read": False, "write": False},
            "settings": {"read": False, "write": False}
        }
    },
    "stock_clerk": {
        "name": "Personal de Reposición",
        "level": 4,
        "permissions": {
            "dashboard": {"read": False, "write": False},
            "search": {"read": "products_only", "write": False},
            "inventory": {"read": "scan_only", "write": "restock_only", "delete": False},
            "sales": {"read": False, "write": False, "refund": False},
            "employees": {"read": False, "write": False, "delete": False},
            "finance": {"read": False, "write": False},
            "reports": {"read": False, "write": False, "export": False},
            "notifications": {"read": False, "write": False},
            "settings": {"read": False, "write": False}
        }
    }
}