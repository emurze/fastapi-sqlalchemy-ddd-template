from typing import TypeVar, NoReturn

from fastapi import HTTPException
from starlette import status
from shared.application import errors

status_codes = {
    errors.RESOURCE_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
    errors.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
}

T = TypeVar('T')


def raise_errors(result: T) -> NoReturn | T:
    if not result.status:
        raise HTTPException(status_codes[result.error], result.error)
    return result

