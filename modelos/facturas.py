from pydantic import BaseModel, computed_field
from .clientes import Cliente
from datetime import datetime
from .transacciones import Transacciones
from sqlmodel import SQLModel, Field, Relationship


# Crear el modelo facturas

class FacturasBase(SQLModel):
    #cliente: Cliente
    fecha:str = Field(default=datetime.now())
    #transacciones: list[Transacciones] 

    @computed_field
    @property
    def vr_total(self) -> float:
        # calcular (cantidad * valor unitario)
        # Consultar id actual de factura
        # factura_id_actual = getattr(self, 'id', None)
        # total_factura = 0.0
        # if not factura_id_actual or not self.transacciones:
        #     return total_factura
        # #Recorrer la lista de transacciones segun el factura_id
        # for transaccion in self.transacciones:
        #     if transaccion.factura_id == factura_id_actual:
        #        total_factura += transaccion.valor_unitario * transaccion.cantidad

        return 0.0

class FacturasCrear(FacturasBase):
    pass

class FacturasEditar(FacturasBase):
    pass

class Facturas(FacturasBase, table= True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
  