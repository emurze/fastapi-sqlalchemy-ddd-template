from typing import Annotated

from fastapi import Request, Depends

from shared.application.messagebus import MessageBus


def get_bus(request: Request) -> MessageBus:
    return request.app.extra["container"].message_bus()


BusDep = Annotated[MessageBus, Depends(get_bus)]
