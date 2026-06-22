from pydantic import BaseModel

# crear el modelo clientesid, nombre, email, edad, descripcion

class ClienteBase(BaseModel):
    nombre: str 
    email: str
    edad: int
    descripcion: str

class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int | None = None

