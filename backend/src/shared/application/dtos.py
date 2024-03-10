from typing import Optional, ClassVar, Self, TypeAlias

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SuccessResult(Model):
    @staticmethod
    def get_error() -> None:
        return None

    @staticmethod
    def get_status() -> bool:
        return True


class FailedResult(Model):
    error: Optional[str] = None

    RESOURCE_ERROR: ClassVar[str] = "Resource Error"
    RESOURCE_NOT_FOUND_ERROR: ClassVar[str] = "Resource Not Found Error"
    RESOURCE_CONFLICT_ERROR: ClassVar[str] = "Resource Conflict Error"
    PARAMETERS_ERROR: ClassVar[str] = "Parameters Error"
    SYSTEM_ERROR: ClassVar[str] = "System Error"
    UNAUTHORIZED_ERROR: ClassVar[str] = "Unauthorized Error"

    @classmethod
    def build_resource_error(cls) -> Self:
        return cls(error=cls.RESOURCE_ERROR)

    @classmethod
    def build_resource_not_found_error(cls) -> Self:
        return cls(error=cls.RESOURCE_NOT_FOUND_ERROR)

    @classmethod
    def build_resource_conflict_error(cls) -> Self:
        return cls(error=cls.RESOURCE_CONFLICT_ERROR)

    @classmethod
    def build_parameters_error(cls) -> Self:
        return cls(error=cls.PARAMETERS_ERROR)

    @classmethod
    def build_system_error(cls) -> Self:
        return cls(error=cls.SYSTEM_ERROR)

    @classmethod
    def build_unauthorized_error(cls) -> Self:
        return cls(error=cls.UNAUTHORIZED_ERROR)

    def get_error(self) -> Optional[str]:
        return self.error

    def get_status(self) -> bool:
        return not self.error


Result: TypeAlias = SuccessResult | FailedResult
