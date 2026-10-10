from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from src.data.diccionario import products_data, staff_users
app = FastAPI()

# ===== Modelo de datos para el cuerpo del login =====
class LoginRequest(BaseModel):
    user: str
    password: str

# ===== Endpoint: productos (se utiliza en main.py) =====       
@app.get('/')
def products():
    return products_data

# ===== Endpoint: solo para ver todos los usuarios (debug) =====
@app.get('/customers')
def customs():
    return staff_users

# ===== Endpoint: login =====
@app.post('/login')
def login(request: LoginRequest):
    # Recorremos la lista staff_users (del diccionario)
    for user in staff_users:
        # Comparamos user y password
        if user["user"] == request.user and user["password"] == request.password:
            # Copiamos los datos del usuario, pero sin la contraseña
            user_data = {k: v for k, v in user.items() if k != "password"}
            return {
                "success": True,
                "message": "Inicio de sesión exitoso",
                "user_data": user_data,
            }

    # Si ningún usuario coincide:
    return {
        "success": False,
        "message": "Usuario o contraseña incorrectos",
    } 

@app.get('/orders')
def get_orders():
    return [
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
        {'id':"27728",'date':datetime.now(),'amount':56,'cat':"food",'menu':"xima arroz"},
    ]
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)

#download the simple server api