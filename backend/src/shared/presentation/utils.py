from typing import NoReturn

from fastapi import HTTPException

from shared.application.dtos import OutputDto
from shared.presentation.json_dtos import FailedJsonResponse


def raise_errors(output_dto: OutputDto) -> NoReturn | OutputDto:
    if not output_dto.status:
        message = output_dto.message
        raise HTTPException(
            status_code=FailedJsonResponse.STATUS_CODES[message],
            detail=message
        )
    return output_dto
