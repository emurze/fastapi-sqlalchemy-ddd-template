from typing import Annotated

from fastapi import Request, Depends

from shared.application import Application


def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application


AppDep = Annotated[Application, Depends(get_application)]
