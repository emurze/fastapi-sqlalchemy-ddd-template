from starlette.requests import Request
from starlette.responses import JSONResponse


async def system_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=500,
        content={"detail": "System error"},
    )
