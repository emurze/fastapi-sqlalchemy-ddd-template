from fastapi import APIRouter

from auth.application import commands
from auth.application.command_handlers.add_client import AddClientHandler
from auth.presentation import schemas as s
from auth.presentation.container import UoWDep

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=s.AddClientJsonResponse, status_code=201)
async def add_client(request: s.AddClientJsonRequest, uow: UoWDep):
    handler = AddClientHandler(uow)
    command = commands.AddClientCommand.model_validate(request)
    result = await handler.execute(command)
    return s.AddClientJsonResponse.model_validate(result.payload)
