from typing import TypeAlias

from black import Optional
from fastapi import HTTPException
from starlette.responses import JSONResponse

from shared.presentation.json_dtos import STATUS_CODES


def handle_errors(result, errors: Optional[list] = None) -> None:
    if result.error and result.error in errors:
        raise HTTPException(
            status_code=STATUS_CODES[result.error],
            detail=result.error,
        )


def _get_response(result, schema, status_code: int) -> JSONResponse:
    model = schema.model_validate(result.payload)
    return JSONResponse(model.model_dump(), status_code)


Response: TypeAlias = _get_response
