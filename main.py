from flask import *
import db
from models import Stock
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_report import Reporter
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np


# inicializar el servidor en el dominio actual
app = Flask(__name__)

@app.route('/') #ruta de home, muestra solamente la ventana de login
def home():
    return render_template("index.html")

@app.route('/', methods=['GET', 'POST'])
def autentificacion_admin(): #funcion que verifica el usuario

    if request.method == 'POST':
        db = open("database/usuarios.txt", "r") #txt con los login
        db2 = open("database/contrasenas.txt", "r") #txt con las contrasenas

        usuario = request.form['email']
        contrasena = request.form['contrasena']
        usuarios = db.readlines()
        contrasenas = db2.readlines()
        usuariosDict = dict.fromkeys(usuarios, None)

        acceso = dict(zip(usuarios, contrasenas)) #convierte los dos txt en un diccionario

        #mira si la contrasena introducida corresponde a la contrasena
        if usuario == "admin" and contrasena == "1234":
            return redirect(url_for('acceso_admin'))
        if usuario == "cliente" and contrasena == "5678":
            return redirect(url_for('acceso_cliente'))
        if usuario == "proveedor" and contrasena == "prove":
            return redirect(url_for('acceso_proveedor'))


@app.route('/a', methods=['GET', 'POST'])

def acceso_admin(): #funcion de la vista admin.html

    todas_las_filas = db.session.query(Stock).all()
    ventas = {}
    compras = {}


    for i in todas_las_filas: #calcula las ventas y las compras por producto

        if i.nombre in ventas:

            ventas[i.nombre] += i.vendidos*i.precio_venta

        else:
            ventas[i.nombre] = i.vendidos*i.precio_venta

        if i.nombre in compras:

            compras[i.nombre] += (i.vendidos+i.stock)*i.precio_compra

        else:

            compras[i.nombre] = (i.vendidos+i.stock)*i.precio_compra


    headings_stock = ("ID", "Nombre", "Precio", "Localización", "Disponibilidad", "Ventas", "Descripción")
    image_total = url_for('static', filename='image_total.jpg') #guarda la graifca en una imagen

    style.use("fivethirtyeight") #aplica un estilo
    productos = compras.keys()
    valores_ventas = ventas.values()
    valores_compras = compras.values()

    x = np.arange(len(list(productos)))
    width = 0.35


    fig, ax = plt.subplots()
    #describe los parametros de las axes
    rects1 = ax.bar(x - width / 2, valores_compras, width)
    rects2 = ax.bar(x + width / 2, valores_ventas, width)

    ax.set_ylabel('Ganancias')
    ax.set_title('Ventas y compras')
    ax.set_xticks(x)
    ax.set_xticklabels(productos)
    ax.tick_params(labelsize=8) #cambia el tamano de letra
    plt.legend()
    plt.xticks(rotation='vertical') #gira el texto de las etiquetas
    plt.savefig("static/image_total.jpg",bbox_inches='tight', dpi=500)


    return render_template("admin.html", image_total=image_total)



@app.route('/anadir_productos', methods=['POST'])
def anadir_productos(): #permite modificar la cantidad de stock ## funcion inactiva

    nombre = request.form.get("nombre")
    precio = request.form.get("precio")
    lugar = request.form.get("lugar")
    stock = request.form.get("stock")
    vendidos = request.form.get("vendidos")
    descripcion = request.form.get("descripcion")


    producto = Stock(nombre=nombre, precio=float(precio), lugar=lugar, stock=int(stock), vendidos=vendidos, descripcion=descripcion)

    db.session.add(producto)
    db.session.commit()
    db.session.close()

    return render_template("admin.html")

@app.route('/actualizar', methods=['POST'])
def actualizar_productos(): # actualiza el stock de los productos ## funcion inactiva

    producto = request.form.get("producto")
    compras = request.form.get("compras")

    data = db.session.query(Stock).get(producto)
    data.stock += int(compras)
    db.session.add(data)
    db.session.commit()
    db.session.close()

    todas_las_tareas = db.session.query(Stock).all()
    print(todas_las_tareas)
    data = []
    nombre_productos = {}

    for i in todas_las_tareas:
        data.append((i.id, i.nombre, i.precio_venta, i.lugar, i.stock, i.vendidos, i.descripcion))

        if i.nombre in nombre_productos:

            nombre_productos[i.nombre] += i.vendidos * i.precio_venta

        else:
            nombre_productos[i.nombre] = i.vendidos * i.precio_venta

    headings = ("ID", "Nombre", "Precio", "Localización", "Disponibilidad", "Ventas", "Descripción")
    image = url_for('static', filename='image.jpg')

    style.use("grayscale")

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    productos = nombre_productos.keys()
    vendidos = nombre_productos.values()
    ax.bar(productos, vendidos)
    plt.savefig("static/image.jpg", bbox_inches='tight', dpi=150)

    return render_template("cliente.html", headings=headings, data=data, image=image)

@app.route('/cliente', methods=['GET', 'POST'])

def acceso_cliente():
    todas_las_lineas= db.session.query(Stock).all()
    print(todas_las_lineas)
    data = []
    nombre_productos = {}

    for i in todas_las_lineas:
        data.append((i.id, i.nombre, i.precio_venta, i.capacidad, i.lugar, i.stock, i.vendidos, i.proveedor, i.descripcion))
        if i.nombre in nombre_productos:

            nombre_productos[i.nombre] += i.vendidos * i.precio_venta #calcula las ventas de cada producto

        else:
            nombre_productos[i.nombre] = i.vendidos * i.precio_venta

    headings = ("ID", "Nombre", "Precio venta", "Capacidad", "Localización", "Disponibilidad", "Ventas", "Proveedor", "Descripción")
    image = url_for('static', filename='image.jpg')

    style.use("grayscale")
#genera la grafica de los productos vendidos por el cliente

    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    productos = nombre_productos.keys()
    vendidos = nombre_productos.values()
    ax.bar(productos, vendidos)
    plt.savefig("static/image.jpg", bbox_inches='tight', dpi=150)
    plt.title("Ventas totales por producto")

    return render_template("cliente.html", headings=headings, data=data, image=image)


@app.route('/proveedor', methods=['GET', 'POST'])

def acceso_proveedor():
    todas_las_tareas = db.session.query(Stock).all()
    print(todas_las_tareas)
    data_stock = []
    nombre_productos = {}
    empresas = {}

    for i in todas_las_tareas:
        data_stock.append((i.nombre, i.precio_compra, (i.vendidos+i.stock)*i.precio_compra, i.descuento, i.iva, i.stock, i.descripcion, i.proveedor, i.telefono, i.direccion, i.cif))

        if i.nombre in nombre_productos:

            nombre_productos[i.nombre] += (i.vendidos+i.stock)*i.precio_compra

        else:
            nombre_productos[i.nombre] = (i.vendidos+i.stock)*i.precio_compra

        if i.proveedor in empresas:

            empresas[i.proveedor] += (i.vendidos+i.stock)*i.precio_compra

        else:
            empresas[i.proveedor] = (i.vendidos+i.stock)*i.precio_compra

    headings_stock = ("Nombre", "Precio Compra", "Ganancias del proveedor", "Descuento", "IVA", "Stock", "Descripción", "Empresa", "Teléfono", "Dirección", "CIF")


    image_productos = url_for('static', filename='image_productos.jpg')

    style.use("grayscale")
#calcula cuanto ha ganado el proveedor por producto
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    productos = nombre_productos.keys()
    stock = nombre_productos.values()
    ax.bar(productos, stock)
    plt.savefig("static/image_productos.jpg", bbox_inches='tight', dpi=150)

    image_empresas = url_for('static', filename='image_empresas.jpg')

    style.use("grayscale")
#calcula cuanto ha ganado el proveedor segun la empresa que le ha comprado productos
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_axes([0, 0, 1, 1])
    lista_empresas = empresas.keys()
    ganancias_empresas = empresas.values()
    ax.bar(lista_empresas, ganancias_empresas)
    plt.savefig("static/image_empresas.jpg", bbox_inches='tight', dpi=150)

    return render_template("proveedor.html", headings_stock=headings_stock, data_stock=data_stock, image_productos=image_productos, image_empresas=image_empresas)


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)  # creamos el modelo de datos

    # arranca el servidor web
    app.run(host="0.0.0.0", port=8000, debug=True)