from fastapi import APIRouter

router = APIRouter(prefix="/products", 
                   tags=["Products"],
                   responses={404: {"message":"Not Found Product"}})

products_list = ["Producto 1", "Producto 2", "Producto 3", "Producto 4"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}") ## Due to prefix definition I do not need to define route each time
async def products(id: int):
    return products_list[id]
