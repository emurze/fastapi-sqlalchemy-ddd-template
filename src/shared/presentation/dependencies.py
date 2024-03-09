from typing import Annotated

from fastapi import Request, Depends

from shared.application.message_bus import MessageBus


def get_bus(request: Request) -> MessageBus:
    bus = request.app.container.message_bus()
    return bus


BusDep = Annotated[MessageBus, Depends(get_bus)]
