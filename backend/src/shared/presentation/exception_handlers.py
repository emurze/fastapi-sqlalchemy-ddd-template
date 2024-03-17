from starlette.requests import Request
from starlette.responses import JSONResponse


async def server_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
