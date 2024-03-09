from typing import Annotated

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncEngine

from shared.application.message_bus import MessageBus


def get_bus(request: Request) -> MessageBus:
    return request.app.container.message_bus()


def get_engine(request: Request) -> AsyncEngine:
    return request.app.container.db_engine()


BusDep = Annotated[MessageBus, Depends(get_bus)]
EngineDep = Annotated[AsyncEngine, Depends(get_engine)]
