from fastapi import APIRouter

from auth.presentation import schemas as s
from auth.application import commands
from auth.application import queries
from auth.presentation.container import command_handlers
from auth.presentation.container import query_handlers

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("/", response_model=s.AddClientJsonResponse)
async def add_client(request: s.AddClientJsonRequest):
    command = commands.AddClientCommand.model_validate(request)
    result = await command_handlers.add_client(command)
    return s.AddClientJsonResponse.model_validate(result.payload)
