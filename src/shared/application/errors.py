from typing import Self, Optional

from shared.application.model import Model

RESOURCE_ERROR = "Resource Error"
RESOURCE_NOT_FOUND_ERROR = "Resource Not Found Error"
RESOURCE_CONFLICT_ERROR = "Resource Conflict Error"
PARAMETERS_ERROR = "Parameters Error"
SYSTEM_ERROR = "System Error"
UNAUTHORIZED_ERROR = "Unauthorized Error"


class ErrorBuilder(Model):
    error: Optional[str] = None

    @classmethod
    def build_resource_error(cls) -> Self:
        return cls(error=[RESOURCE_ERROR])

    @classmethod
    def build_resource_not_found_error(cls) -> Self:
        return cls(error=RESOURCE_NOT_FOUND_ERROR)

    @classmethod
    def build_resource_conflict_error(cls) -> Self:
        return cls(error=RESOURCE_CONFLICT_ERROR)

    @classmethod
    def build_parameters_error(cls) -> Self:
        return cls(error=PARAMETERS_ERROR)

    @classmethod
    def build_system_error(cls) -> Self:
        return cls(error=SYSTEM_ERROR)

    @classmethod
    def build_unauthorized_error(cls) -> Self:
        return cls(error=UNAUTHORIZED_ERROR)

    @property
    def status(self) -> bool:
        return not self.error
