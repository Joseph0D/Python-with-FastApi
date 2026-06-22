from fastapi import APIRouter, HTTPException,status
from modelos.transacciones import Transacciones, TransaccionesCrear
from modelos.facturas import Facturas
from listas import lista_facturas, lista_transacciones

rutas_transacciones = APIRouter()
#lista_facturas: list[Facturas] = []
#lista_transacciones: list[Transacciones] = []

#Endpoints para transacciones

@rutas_transacciones.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
    return lista_transacciones

@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transacciones)
async def listar_transaccion(transaccion_id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == transaccion_id:
            return transaccion
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"La transacción con id {transaccion_id} no existe"
    )

@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transacciones)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionesCrear):
    #Buscar factura
    factura_encontrada = None
    for factura in lista_facturas:
        if factura.id == factura_id:
            factura_encontrada = factura
    #Mensaje si no exista la factura
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con id {factura_id} no existe"
        )

    #Validar datos de la transaccion
    transaccion_val = Transacciones.model_validate(datos_transaccion.model_dump())
    transaccion_val.factura_id = factura_id
    factura_encontrada.transacciones.append(transaccion_val)
    #id transaccion
    transaccion_val.id = len(lista_transacciones) + 1
    lista_transacciones.append(transaccion_val)
    return transaccion_val

  

@rutas_transacciones.patch("/transacciones/{transaccion_id}", response_model=Transacciones)
async def editar_transaccion(transaccion_id: int, datos_transaccion: TransaccionesCrear):
    pass

@rutas_transacciones.delete("/transacciones/{transaccion_id}", response_model=Transacciones)
async def eliminar_transaccion(transaccion_id: int):
    for i, transaccion in enumerate(lista_transacciones):
        if transaccion.id == transaccion_id:
            lista_transacciones.pop(i)
            return {"detail": f"La transacción con id {transaccion_id} ha sido eliminada"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"La transacción con id {transaccion_id} no existe"
    )
