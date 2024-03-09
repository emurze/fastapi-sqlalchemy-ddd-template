from typing import NoReturn, ClassVar

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict
from starlette import status

from shared.application.dtos import FailedResult, Result


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FailedJsonResponse(Schema):
    detail: str
    STATUS_CODES: ClassVar[dict[str, int]] = {
        FailedResult.RESOURCE_ERROR: status.HTTP_404_NOT_FOUND,
        FailedResult.RESOURCE_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
        FailedResult.RESOURCE_CONFLICT_ERROR: status.HTTP_409_CONFLICT,
        FailedResult.PARAMETERS_ERROR: status.HTTP_400_BAD_REQUEST,
        FailedResult.UNAUTHORIZED_ERROR: status.HTTP_401_UNAUTHORIZED,
        FailedResult.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }

    @staticmethod
    def raise_errors(result: Result) -> NoReturn | Result:
        if not result.get_status():
            raise HTTPException(
                FailedJsonResponse.STATUS_CODES[result.error], result.error
            )
        return result
