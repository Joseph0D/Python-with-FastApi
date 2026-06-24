from pydantic import BaseModel, computed_field
from .clientes import Cliente, ClienteLeer
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
        total_factura = 0.0
        if self.transacciones ==None:
           return total_factura
        # #Recorrer la lista de transacciones segun el factura_id
        for transaccion in self.transacciones:
               total_factura += transaccion.valor_unitario * transaccion.cantidad

        return total_factura

class FacturasCrear(FacturasBase):
    pass

class FacturasEditar(FacturasBase):
    pass

class Facturas(FacturasBase, table= True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
    #Relaciones virutales con cliente, transacciones . NO en la BD
    cliente : Cliente = Relationship(back_populates="factura")
    transacciones: list[Transacciones] = Relationship(back_populates="factura")

    #crear modelo para mostrar la usauario o el cliente
class FacturaLeer(FacturasBase):
        id: int
        cliente: ClienteLeer
        #pero no es recomendable, por las buenas practicas
        # Transacciones: list[Transacciones] = []

class FacturaLeerCompuesta(FacturaLeer):
     transacciones: list[Transacciones] = []
        


  