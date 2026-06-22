from pydantic import BaseModel

class TransaccionBase(BaseModel):
    cantidad: int
    valor_unitario: float
       
class TransaccionesCrear(TransaccionBase):
    pass

class TransaccionesEditar(TransaccionBase):
    pass

class Transacciones(TransaccionBase):
    id: int | None = None
    factura_id: int | None = None
    #aqui va la relacion con el modelo factura(solo un campo)