from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends, FastAPI


nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

#motor de bd
motor_bd = create_engine(url_bd,)

#definir el metodo para crear la tablas
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield #no hay nada para retornar o ejecutar

#definir el metodo para la sesion
def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion#Retorna la sesion

#Denominado inyeccion de dependencias
#Registrar la sesion como dependencia, utilizada en nuestros endpoints
Sesion_dependecia = Annotated[Session, Depends(obtener_sesion)]
