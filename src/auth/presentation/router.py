from fastapi import APIRouter

from auth.application import commands, queries
from auth.application.command_handlers.add_client import AddClientHandler
from auth.application.query_handlers.get_client import GetClientHandler
from auth.presentation import schemas as s
from auth.presentation.container import UoWDep
from shared.presentation.utils import to_params

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=s.AddClientJsonResponse, status_code=201)
async def add_client(dto: s.AddClientJsonRequest, uow: UoWDep):
    handler = AddClientHandler(uow)
    command = commands.AddClientCommand.model_validate(dto)
    result = await handler.execute(command)
    return s.AddClientJsonResponse.model_validate(result.payload)


@router.get(
    "/{client_id}",
    response_model=s.GetClientJsonResponse,
    status_code=200,
)
# @cache(expire=30)
async def get_client(dto: to_params(s.GetClientJsonRequest), uow: UoWDep):
    handler = GetClientHandler(uow)
    command = queries.GetClientQuery(id=dto.client_id)
    result = await handler.execute(command)
    return s.GetClientJsonResponse.model_validate(result.payload)
