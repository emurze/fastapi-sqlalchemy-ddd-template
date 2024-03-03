from fastapi import FastAPI

from auth.presentation.router import router as client_router


def include_routers(app: FastAPI):
    app.include_router(client_router)
