from typing import Any, TypeVar

from black import Optional
from fastapi import HTTPException

from seedwork.presentation.json_dtos import STATUS_CODES

T = TypeVar('T')


def handle_errors(result: Any, errors: Optional[list] = None) -> None:
    assert errors is not None, "Please pass the errors being processed."

    if result.error and result.error.type in errors:
        raise HTTPException(
            status_code=STATUS_CODES[result.error.type],
            detail=result.error.detail,
        )
