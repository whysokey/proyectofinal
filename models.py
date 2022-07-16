import db
from sqlalchemy import Column, Integer, String, Float



class Stock(db.Base):
    __tablename__ = "Stock"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio_compra = Column(Float)
    precio_venta = Column(Float)
    lugar = Column(String)
    stock = Column(Integer, nullable=False)
    capacidad = Column(Integer)
    vendidos = Column(Integer)
    descripcion = Column(String)
    proveedor = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    cif = Column(String)
    facturacion = Column(Float)
    descuento = Column(Float)
    iva = Column(Float)


    def __init__(self, nombre, precio_compra, precio_venta, lugar, stock, capacidad, vendidos, descripcion, proveedor, telefono, direccion, cif, facturacion, descuento, iva):
        self.nombre = nombre
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.lugar = lugar
        self.stock = stock
        self.capacidad = capacidad
        self.vendidos = vendidos
        self.descripcion = descripcion
        self.proveedor = proveedor
        self.telefono = telefono
        self.direccion = direccion
        self.cif = cif
        self.facturacion = facturacion
        self.descuento = descuento
        self.iva = iva

    '''
    def __str__(self):
        return """{}:

        {} euros,
        se encuentra en {},
        hay {} en el stock...
        
        y se vendieron {} unidades
        {}

        """.format(self.nombre, self.precio, self.lugar, self.stock, self.vendidos, self.descripcion)
        
    '''

