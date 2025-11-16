from fastapi import FastAPI
from datetime import datetime
app = FastAPI()
db = [
    {
        'id': 1,
        'name': "Jamon Sandwichero Sofia 1 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img.png"
    },
    {
        'id': 2,
        'name': "Achocolatado Chocolike 1 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img2.png"
    },
    {
        'id': 3,
        'name': "Aceite Fino Light 4.5 L",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img3.png"
    },
    {
        'id': 4,
        'name': "Te Windsor Canela 130 Sobres",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img4.png"
    },
    {
        'id': 5,
        'name': "Azucar Guabira Blanca 1 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img5.png"
    },
    {
        'id': 6,
        'name': "Mayonesa Kris Limon 485 ml",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img7.png"
    },
    {
        'id': 7,
        'name': "Ketchup Kris Original 200 gr",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img8.png"
    },
    {
        'id': 8,
        'name': "Papel Higienico Nacional Clasico Celeste",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img6.png"
    },
    {
        'id': 9,
        'name': "Lavavajilla Todo Brillo Limon Verde Doypack",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img9.png"
    },
    {
        'id': 10,
        'name': "Detergente Polvo Omo Limon 4.8 kg",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img10.png"
    },
    {
        'id': 11,
        'name': "Pinza Ropa Rey Gigante 24 un",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img11.png"
    },
    {
        'id': 12,
        'name': "Lavandina Sapolio 1 L",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img12.png"
    },
    {
        'id': 13,
        'name': "Lapices de Colores Faber Castell 12 Colores + 2 Lapices",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img13.png"
    },
    {
        'id': 14,
        'name': "Cartulina Blanca Pliego",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img14.png"
    },
    {
        'id': 15,
        'name': "Acrilex Opaco Surtido",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img15.png"
    },
    {
        'id': 16,
        'name': "Cartulina Oficio 10 un",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img16.png"
    },
    {
        'id': 17,
        'name': "Hoja Papel Bond Chamex Carta 500 Hojas",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img17.png"
    },
    {
        'id': 18,
        'name': "Libro Infantil Lexus",
        'saleprice': 24.99,
        'purchaseprice': 24.99,
        'image': "\products\img18.png"
    }
]

@app.get('/')
def products():
    return db

@app.get('/customers')
def customs():
    return [
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        {'name':'Diqui Joaquim','adress':'djoaquimnamueto@gmail.com','contact':'+258860716912','orders':5,'status':'active'},
        
    ]

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