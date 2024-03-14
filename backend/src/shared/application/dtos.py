from typing import Optional, ClassVar, Self, TypeAlias

from pydantic import BaseModel, ConfigDict


class Model:
    def model_from(self):
        pass


class SuccessOutputDto(Model):
    @property
    def status(self) -> bool:
        return True


class FailedOutputDto(Model):
    message: str

    RESOURCE_ERROR: ClassVar[str] = "Resource Error"
    RESOURCE_NOT_FOUND_ERROR: ClassVar[str] = "Resource Not Found Error"
    RESOURCE_CONFLICT_ERROR: ClassVar[str] = "Resource Conflict Error"
    PARAMETERS_ERROR: ClassVar[str] = "Parameters Error"
    SYSTEM_ERROR: ClassVar[str] = "System Error"
    UNAUTHORIZED_ERROR: ClassVar[str] = "Unauthorized Error"

    @classmethod
    def build_resource_error(cls) -> Self:
        return cls(message=cls.RESOURCE_ERROR)

    @classmethod
    def build_resource_not_found_error(cls) -> Self:
        return cls(message=cls.RESOURCE_NOT_FOUND_ERROR)

    @classmethod
    def build_resource_conflict_error(cls) -> Self:
        return cls(message=cls.RESOURCE_CONFLICT_ERROR)

    @classmethod
    def build_parameters_error(cls) -> Self:
        return cls(message=cls.PARAMETERS_ERROR)

    @classmethod
    def build_system_error(cls) -> Self:
        return cls(message=cls.SYSTEM_ERROR)

    @classmethod
    def build_unauthorized_error(cls) -> Self:
        return cls(message=cls.UNAUTHORIZED_ERROR)

    @property
    def status(self) -> bool:
        return False


OutputDto: TypeAlias = SuccessOutputDto | FailedOutputDto
