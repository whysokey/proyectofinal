from flask import *
import db
from models import Stock
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy_report import Reporter

# inicializar el servidor en el dominio actual
app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if request.form.get('admin') == 'admin':
            pass  # do something

        elif request.form.get('cliente_b') == 'cliente':
            pass

        elif request.form.get('proveedor_b') == 'proveedor':
            pass

        else:
            pass  # unknown

    elif request.method == 'GET':
        return render_template('index.html')

    return render_template("index.html")


@app.route('/a', methods=['GET', 'POST'])
def admin():
    todas_las_tareas = db.session.query(Stock).all()
    print(todas_las_tareas)
    data = []
    for i in todas_las_tareas:
        data.append((i.nombre, i.precio, i.lugar, i.stock, i.descripcion))


    headings = ("Nombre", "Precio", "Localización", "Disponibilidad", "Descripción")

    return render_template("admin.html", headings=headings, data=data)


@app.route('/anadir_productos', methods=['POST'])
def anadir_productos():

    nombre = request.form.get("nombre")
    precio = request.form.get("precio")
    lugar = request.form.get("lugar")
    stock = request.form.get("stock")
    descripcion = request.form.get("descripcion")


    producto = Stock(nombre=nombre, precio=precio, lugar=lugar, stock=stock, descripcion=descripcion)

    db.session.add(producto)
    db.session.commit()
    db.session.close()

    return render_template("admin.html")



@app.route('/cliente', methods=['GET', 'POST'])
def acceso_cliente():
    return render_template("cliente.html")


@app.route('/proveedor', methods=['GET', 'POST'])
def acceso_proveedor():
    return render_template("proveedor.html")


@app.route('/c')
def cliente():
    pass


@app.route('/p')
def proveedor():
    pass


if __name__ == "__main__":
    db.Base.metadata.create_all(db.engine)  # creamos el modelo de datos

    # arranca el servidor web
    app.run(host="0.0.0.0", port=8000, debug=True)