from fastapi import APIRouter

router = APIRouter(prefix="/products")                 ### instancia de APIRouter, y prefijo para facilitar la busqueda ###

product_list = ["producto 1", "producto 2", "producto 3", "producto 4", "producto 5" ]


@router.get("/")                   
async def products():              
    return product_list


@router.get("/{id}")                   
async def products(id: int):              
    return product_list[id]