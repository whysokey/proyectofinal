import db
from sqlalchemy import Column, Integer, String


class Stock(db.Base):
    __tablename__ = "Stock"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(String)
    lugar = Column(String)
    stock = Column(String)
    descripcion = Column(String)

    def __init__(self, nombre, precio, lugar, stock, descripcion):
        self.nombre = nombre
        self.precio = precio
        self.lugar = lugar
        self.stock = stock
        self.descripcion = descripcion

    def __str__(self):
        return """{}:

        {} euros,
        se encuentra en {},
        hay {} en el stock...

        {}

        """.format(self.nombre, self.precio, self.lugar, self.stock, self.descripcion)