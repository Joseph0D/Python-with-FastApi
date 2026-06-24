from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

class TransaccionBase(SQLModel):
    cantidad: int = Field(default=0)
    valor_unitario: float = Field(default=0.0)
       
class TransaccionesCrear(TransaccionBase):
    pass

class TransaccionesEditar(TransaccionBase):
    pass

class Transacciones(TransaccionBase, table=True):
    id: int | None = Field(default=None , primary_key=True)
    factura_id: int | None = Field(default=None, foreign_key="facturas.id")
    #aqui va la relacion con el modelo factura(solo un campo)