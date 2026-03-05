from fastapi import APIRouter, Path, Query
from uuid import UUID
from app.models.producto import ProductCreate, ProductUpdate, ProductOut, ProductList
from app.services.products_servise import list_product, get_product, create_product, update_product, delete_product

router = APIRouter(prefix="/products")
# mostrar un listado de varios productos max 500 por default 100
# https://localhost:8000/products/?limit=100&offset=0
# https://localhost:8000/products/?limit=200&offset=10
# https_://localhost:8000/products/?limit=50&offset=abc
# limit es el numero de registros a mostrar y offset es el numero de registros que va a comenzar

@router.get("/", name="get_products") # Se corrigió el name para que coincida con el diccionario en exceptions.py
def listar_productos(
    limit: int = Query(100, ge=1, le=500), # Ajustado a 500 max según tus requerimientos
    offset: int = Query(0, ge=0)
    ):
    # La validación RequestValidationError ocurre antes de este punto.
    # Si llega aquí y da 500, el error está en list_product.
    return list_product(limit, offset)

# Se recomienda dejar las rutas fijas antes que las rutas con variables si hubiera colisión, 
# pero aquí usamos UUID para diferenciar product_id de los parámetros query.

@router.get("/{product_id}", response_model=ProductOut, name="obtener_producto")
def obtener_producto(
    product_id: UUID = Path(..., description="El ID del producto debe ser un UUID válido")
    ):
    return get_product(product_id)

@router.post(
    "/",
    # response_model=ProductCreate, # Opcional: revisa si ProductCreate es el modelo de salida correcto
    name="crear_producto"
)
def api_create_product(body: ProductCreate):
    return create_product(body.model_dump())

@router.put("/{product_id}",
    response_model=ProductUpdate, 
    name="actualizar_producto"
    )
def api_update_product(product_id: UUID, body: ProductUpdate):
    return update_product(product_id, body.model_dump(exclude_none=True))

@router.delete(
    "/{product_id}",
    name="eliminar_producto"
    )
def api_delete_product(product_id: UUID):
    return delete_product(product_id)