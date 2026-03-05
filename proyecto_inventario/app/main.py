from fastapi import FastAPI
from app.routes import productos
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import validation_exception_handler
from starlette.types import ExceptionHandler
from typing import cast

app = FastAPI()

#registrar el archivo de exceptions
app.add_exception_handler(RequestValidationError, cast(ExceptionHandler, validation_exception_handler))

#registrar el archivo de rutas(productos.py)
app.include_router(productos.router)
