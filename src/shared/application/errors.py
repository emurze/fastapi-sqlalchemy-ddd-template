from typing import ClassVar, Self, Optional

from shared.application.model import Model


class ErrorBuilder(Model):
    error_detail: Optional[str] = None

    RESOURCE_ERROR: ClassVar[str] = "Resource Error"
    RESOURCE_NOT_FOUND_ERROR: ClassVar[str] = "Resource Not Found Error"
    RESOURCE_CONFLICT_ERROR: ClassVar[str] = "Resource Conflict Error"
    PARAMETERS_ERROR: ClassVar[str] = "Parameters Error"
    SYSTEM_ERROR: ClassVar[str] = "System Error"
    UNAUTHORIZED_ERROR: ClassVar[str] = "Unauthorized Error"

    @classmethod
    def build_resource_error(cls) -> Self:
        return cls(error_detail=[cls.RESOURCE_ERROR])

    @classmethod
    def build_resource_not_found_error(cls) -> Self:
        return cls(error_detail=cls.RESOURCE_NOT_FOUND_ERROR)

    @classmethod
    def build_resource_conflict_error(cls) -> Self:
        return cls(error_detail=cls.RESOURCE_CONFLICT_ERROR)

    @classmethod
    def build_parameters_error(cls) -> Self:
        return cls(error_detail=cls.PARAMETERS_ERROR)

    @classmethod
    def build_system_error(cls) -> Self:
        return cls(error_detail=cls.SYSTEM_ERROR)

    @classmethod
    def build_unauthorized_error(cls) -> Self:
        return cls(error_detail=cls.UNAUTHORIZED_ERROR)

    @property
    def status(self) -> bool:
        return not self.error_detail
