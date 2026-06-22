from fastapi import APIRouter, HTTPException,status
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from listas import lista_clientes

rutas_clientes = APIRouter()
#lista_clientes: list[Cliente] = []


#endpoint para obtener un cliente
@rutas_clientes.get("/clientes",response_model=list[Cliente])
async def listar_clientes():
    return lista_clientes

@rutas_clientes.post("/clientes",response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    #generar id
    id_cliente =len(lista_clientes) + 1
    cliente_val.id = id_cliente
    lista_clientes.append(cliente_val)
    return cliente_val

#endpoint para listar un solo cliente
@rutas_clientes.get("/clientes/{cliente_id}",response_model=Cliente)
async def listar_cliente(cliente_id: int):
    #recorrer lista clientes
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == cliente_id:
            return objeto_cliente
        



#enpoint editar cliente, y agregar a la lista
@rutas_clientes.patch("/clientes/{cliente_id}",response_model=Cliente)
async def editar_cliente(cliente_id: int, datos_cliente: ClienteEditar):
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == cliente_id:
            #validar cliente
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = cliente_id
            lista_clientes[i] = cliente_val
            return cliente_val
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con id {cliente_id} no existe"
        )


#enpoint para eliminar cliente, y eliminar de la lista
@rutas_clientes.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int):
    for i, objeto_cliente in enumerate(lista_clientes):
        if objeto_cliente.id == cliente_id:
            lista_clientes.pop(i)
            return {"detail": f"El cliente con id {cliente_id} ha sido eliminado"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente con id {cliente_id} no existe"
        )