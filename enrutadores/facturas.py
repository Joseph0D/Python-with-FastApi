from fastapi import APIRouter, HTTPException,status
from modelos.clientes import Cliente
from modelos.facturas import Facturas, FacturasCrear,FacturasEditar
from listas import lista_clientes, lista_facturas
from conexion_bd import Sesion_dependecia
from sqlmodel import select
rutas_facturas = APIRouter()

#lista_clientes: list[Cliente] = []
#lista_facturas: list[Facturas] = []

#Endpoints para facturas


@rutas_facturas.get("/facturas",response_model=list[Facturas])
async def listar_facturas(sesion: Sesion_dependecia):
    #select * from factura
    consulta = select(Facturas)
    lista_facturas = sesion.exec(consulta).all()
    return lista_facturas



@rutas_facturas.post("/facturas/{cliente_id}",response_model=Facturas)
async def crear_factura(cliente_id: int, datos_factura: FacturasCrear, sesion: Sesion_dependecia):
    #Buscar cliente en bd

    cliente_encontrado = sesion.get(Cliente, cliente_id)
   #Mnesaje si no existe cliente
    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"El cliente con id {cliente_id} no existe"
        )


    #Validar datos de la factura-json, pasar dict
    factura_dict = datos_factura.model_dump()
    factura_dict["cliente_id"] = cliente_id
    factura_val = Facturas.model_validate(factura_dict)
    #guardar en bd
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)
    return factura_val

@rutas_facturas.get("/facturas/{factura_id}",response_model=Facturas)
async def listar_factura(factura_id: int):
    for factura in lista_facturas:
        if factura.id == factura_id:
            return factura
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"La factura con id {factura_id} no existe"
    )



@rutas_facturas.patch("/facturas/{factura_id}",response_model=Facturas)
async def editar_factura(factura_id: int, datos_factura: FacturasEditar):
    pass

@rutas_facturas.delete("/facturas/{factura_id}", response_model=Facturas)
async def eliminar_factura(factura_id: int):
    for i, factura in enumerate(lista_facturas):
        if factura.id == factura_id:
            lista_facturas.pop(i)
            return {"detail": f"La factura con id {factura_id} ha sido eliminada"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"La factura con id {factura_id} no existe"
    )
