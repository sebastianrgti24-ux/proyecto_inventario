from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


MENSAJES_ERROR = {
    "get_products": { # Este nombre debe coincidir con el name="get_products" del router
        "limit": {
            "less_than_equal": "El límite debe ser menor o igual a 500",
            "greater_than_equal": "El límite debe ser un número positivo (mínimo 1).",
            "int_parsing": "El límite debe ser un número entero, no texto",
        },
        "offset": {
            "greater_than_equal": "El offset no puede ser un número negativo (mínimo 0)",
            "int_parsing": "El offset debe ser un número entero, no texto",
        }
    }
}

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores_personalizados = []
    
    # Intentamos obtener el nombre de la ruta de forma segura
    try:
        route = request.scope.get("route")
        ruta_name = getattr(route, "name", "") if route else ""
    except Exception:
        ruta_name = ""

    for error in exc.errors():
        # Extraemos el parámetro (limit u offset)
        # Usamos try-except por si la estructura de 'loc' cambia
        try:
            parametro = error["loc"][-1]
            tipo_error = error["type"]
            
            # Mapeo simple para Pydantic V2 (compatibilidad)
            if "int" in tipo_error: 
                tipo_error = "int_parsing"
            elif "less_than" in tipo_error: 
                tipo_error = "less_than_equal"
            elif "greater_than" in tipo_error: 
                tipo_error = "greater_than_equal"

            # Buscamos el mensaje en nuestro diccionario
            mensaje = (
                MENSAJES_ERROR.get(ruta_name, {})
                .get(parametro, {})
                .get(tipo_error)
            )
            
            if mensaje:
                errores_personalizados.append(mensaje)
            else:
                errores_personalizados.append(f"Error en {parametro}: {error.get('msg')}")
        except Exception:
            errores_personalizados.append("Error de validación en los parámetros enviados.")

    return JSONResponse(
        status_code=422,
        content={
            "detalles": errores_personalizados
        }
    )