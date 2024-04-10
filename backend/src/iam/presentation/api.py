from fastapi import APIRouter

from iam.application.command.register_account import RegisterAccountCommand
from iam.presentation import schemas as shm
from seedwork.domain.errors import ErrorType
from seedwork.presentation.dependencies import BusDep
from seedwork.presentation.utils import handle_errors

iam_router = APIRouter(prefix="/iam", tags=["iam"])


@iam_router.post('/account/', response_model=shm.RegisterAccountResponse)
async def register_account(dto: shm.RegisterAccountRequest, bus: BusDep):
    command = RegisterAccountCommand.model_validate(dto)
    result = await bus.handle(command)
    handle_errors(result, errors=[ErrorType.VALIDATION])
    return result.payload
