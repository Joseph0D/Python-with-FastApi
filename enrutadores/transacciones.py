from fastapi import APIRouter, HTTPException,status
from modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from modelos.facturas import Facturas
from listas import lista_facturas, lista_transacciones
from conexion_bd import Sesion_dependecia
from sqlmodel import select


rutas_transacciones = APIRouter()
#lista_facturas: list[Facturas] = []
#lista_transacciones: list[Transacciones] = []

#Endpoints para transacciones

@rutas_transacciones.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones(sesion : Sesion_dependecia):
    # consulta = select(Transacciones)
    # lista_transacciones = sesion.exec(consulta).all()
    # return lista_transacciones
    return sesion.exec(select(Transacciones)).all()

@rutas_transacciones.get("/transacciones/{transaccion_id}", response_model=Transacciones)
async def listar_transaccion(transaccion_id: int):
    pass


@rutas_transacciones.post("/transacciones/{factura_id}", response_model=Transacciones)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionesCrear, sesion: Sesion_dependecia):
    #Buscar factura
    factura_encontrada = sesion.get(Facturas, factura_id)
    #Mensaje si no exista la factura
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"La factura con id {factura_id} no existe"
        )

    #Validar datos de la transaccion-json y pasamos a dict
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_val = Transacciones.model_validate(transaccion_dict)
    #guardar en bd
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)
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
