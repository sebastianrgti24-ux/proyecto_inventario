from pydantic import BaseModel, Field,field_validator
from datetime import datetime,date
from uuid import UUID

def validar_fecha_ingreso(value:date)-> date:
    if value<date.today():
        raise ValueError("La fecha no puede ser menor a la fecha actual")
    return value

class ProductCreate(BaseModel):
    name:str=Field(min_length=1,max_length=200)
    quantity:int=Field(ge=1)
    ingreso_date:date
    min_stock:int=Field(ge=0)
    max_stock:int=Field(ge=0,le=1000)

    @field_validator("ingreso_date")
    @classmethod
    def validar_ingreso_date(cls,value:date)->date:
        return validar_fecha_ingreso(value)

class ProductUpdate(BaseModel):
    name:str|None=Field(default=None, min_length=1,max_length=200)
    quantity:int|None=Field(default=None, ge=1)
    ingreso_date:date
    min_stock:int|None=Field(default=None, ge=0)
    max_stock:int|None=Field(default=None, ge=0,le=1000)

    @field_validator("ingreso_date")
    @classmethod
    def validar_ingreso_date(cls,value:date)->date:
        return validar_fecha_ingreso(value)

class ProductOut(BaseModel):
    id:UUID
    name:str
    quantity:int
    ingreso_date:date
    min_stock:int
    max_stock:int
    created_at:date
    updated_at:date

class ProductList(BaseModel):
    total:int
    items:ProductOut

class OneProduct(BaseModel):
    total:int
    items:list[ProductOut]
    
class OneProductOut(BaseModel):
    item:ProductOut