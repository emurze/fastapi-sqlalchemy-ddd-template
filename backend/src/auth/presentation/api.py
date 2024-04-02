from fastapi import APIRouter

from auth.application.command.register_account import RegisterAccountCommand
from auth.presentation import schemas as shm
from seedwork.domain.errors import ErrorType
from seedwork.presentation.dependencies import BusDep
from seedwork.presentation.utils import handle_errors

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post('/account/', response_model=shm.RegisterAccountResponse)
async def register_account(dto: shm.RegisterAccountRequest, bus: BusDep):
    command = RegisterAccountCommand.model_validate(dto)
    result = await bus.handle(command)
    handle_errors(result, errors=[ErrorType.VALIDATION])
    return result.payload
