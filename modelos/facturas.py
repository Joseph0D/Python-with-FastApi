from pydantic import BaseModel, computed_field
from .clientes import Cliente
from datetime import datetime
from .transacciones import Transacciones


# Crear el modelo facturas

class FacturasBase(BaseModel):
    cliente: Cliente
    fecha:str = datetime.now()
    transacciones: list[Transacciones] 

    @computed_field
    @property
    def vr_total(self) -> float:
        #calcular (cantidad * valor unitario)
        #Consultar id actual de factura
        factura_id_actual = getattr(self, 'id', None)
        total_factura = 0.0
        if not factura_id_actual or not self.transacciones:
            return total_factura
        #Recorrer la lista de transacciones segun el factura_id
        for transaccion in self.transacciones:
            if transaccion.factura_id == factura_id_actual:
               total_factura += transaccion.valor_unitario * transaccion.cantidad

        return total_factura

class FacturasCrear(FacturasBase):
    pass

class FacturasEditar(FacturasBase):
    pass

class Facturas(FacturasBase):
    id: int | None = None
  