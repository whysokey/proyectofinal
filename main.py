from flask import *
import db
from models import Stock
from flask_sqlalchemy import SQLAlchemy

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

    return render_template("admin.html")

def mostrar_productos():

    if request.method == "POST":

        nombre = request.form('nombre')

        producto = Stock(nombre)

        db.session.add(producto)
        db.session.commit()
        db.session.close()
        db.session.query(Stock).all()


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
    db.Base.metadata.create_all(db.enginge)  # creamos el modelo de datos

    # arranca el servidor web
    app.run(host="0.0.0.0", port=8000, debug=True)