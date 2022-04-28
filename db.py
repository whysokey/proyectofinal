from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# El engine permite comunicarse con la base de datos
# check same thread para permitir más usuarios
enginge = create_engine("sqlite:///database/stock.db", connect_args={"check_same_thread": False})

# Creación de la sesión que nos permite hacer transacciones en la base de datos
Session = sessionmaker(bind=enginge)
session = Session()

# se encarga de mapear la clase/clases vinculadas a la base de datos
Base = declarative_base()