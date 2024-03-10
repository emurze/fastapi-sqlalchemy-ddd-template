from typing import ClassVar

from pydantic import BaseModel, ConfigDict
from starlette import status

from shared.application.dtos import FailedOutputDto


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FailedJsonResponse(Schema):
    detail: str

    STATUS_CODES: ClassVar[dict[str, int]] = {
        FailedOutputDto.RESOURCE_ERROR: status.HTTP_404_NOT_FOUND,
        FailedOutputDto.RESOURCE_NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
        FailedOutputDto.RESOURCE_CONFLICT_ERROR: status.HTTP_409_CONFLICT,
        FailedOutputDto.PARAMETERS_ERROR: status.HTTP_400_BAD_REQUEST,
        FailedOutputDto.UNAUTHORIZED_ERROR: status.HTTP_401_UNAUTHORIZED,
        FailedOutputDto.SYSTEM_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
