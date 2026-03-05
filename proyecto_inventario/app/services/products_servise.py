from uuid import UUID
from datetime import datetime,timezone
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from app.core.supabase_client import get_supabase
from app.core.config import config
from postgrest import CountMethod

def _table():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_table)

#muetsra una lista de productos,de acuerdo a los parametros
def list_product(limit: int=100,offset: int=0):
   try:
      res= _table().select("*",count=CountMethod.exact).range(offset,offset+limit-1).execute()
      if not res.data:
            raise HTTPException(status_code=404,detail=f"error al encontrar registros")
      return {"items":res.data or [],"total":res.count or 0}
   except Exception as e:
        raise HTTPException(status_code=500,detail=f"error al mostrar registros: {e}")

#mostrar que el producto coindida con el id
def get_product(product_id: UUID):
    try:
        res=_table().select("*").eq("id",str(product_id)).execute()
        #encontrar un limite
        #res=_table().select("*").eq("id",str(product_id)).limit(1).execute()
        if not res.data:
            raise HTTPException(status_code=404,detail=f"error al encontrar el registro con el id {product_id}")
        return{"item":res.data or []}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error al mostrar registros: {e}")


def create_product(datos:dict):
    try:
        print("------------")
        if not datos or product_id:
            raise HTTPException(status_code=400,detail=f"error,datos incompletos")
        datos=jsonable_encoder(datos)
        print("------------")
        print(datos)
        res=_table().insert(datos).execute()
        return {"item":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error al intertar el nuevo registro: {e}")


def update_product(product_id: UUID,datos:dict):
    try:
        if not datos or product_id:
            raise HTTPException(status_code=400,detail=f"error,datos incompletos")
        datos=jsonable_encoder(datos)
        res=_table().update(datos).eq("id",str(product_id)).execute()
        return {"item":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error al actualizar el registro: {e}")


def delete_product(product_id: UUID):
    try:
        if not product_id:
            raise HTTPException(status_code=400,detail=f"error,datos incompletos")
        res=_table().delete().eq("id",str(product_id)).execute()
        return {"item":res.data[0] if res.data else None}
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error al eliminar el registro: {e}")

