from pydantic import BaseModel, ConfigDict
from starlette import status

from shared.domain.errors import ErrorType


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FailedJsonResponse(Schema):
    detail: str


STATUS_CODES = {
    ErrorType.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorType.CONFLICT: status.HTTP_409_CONFLICT,
    ErrorType.VALIDATION: status.HTTP_400_BAD_REQUEST,
    ErrorType.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    ErrorType.SYSTEM: status.HTTP_500_INTERNAL_SERVER_ERROR,
}
