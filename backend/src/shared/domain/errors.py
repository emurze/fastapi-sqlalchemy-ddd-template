from dataclasses import dataclass, field
from typing import Self


class ErrorType:
    CONFLICT: str = "Resource conflict error"
    VALIDATION: str = "Validation error"
    PARAMETERS: str = "Parameters error"
    NOT_FOUND: str = "Resource not found"
    UNAUTHORIZED: str = "Unauthorized error"
    FORBIDDEN: str = "Resource forbidden"
    SYSTEM: str = "Internal system error"


@dataclass(frozen=True, slots=True)
class Error:
    type: str
    details: list = field(default_factory=list)

    @classmethod
    def conflict(cls, detail: str = ErrorType.CONFLICT) -> Self:
        return cls(type=ErrorType.CONFLICT, details=[detail])

    @classmethod
    def validation(cls, details: list) -> Self:
        return cls(type=ErrorType.VALIDATION, details=details)

    @classmethod
    def not_found(cls, detail: str = ErrorType.NOT_FOUND) -> Self:
        return cls(type=ErrorType.NOT_FOUND, details=[detail])

    @classmethod
    def unauthorized(cls, detail: str = ErrorType.UNAUTHORIZED) -> Self:
        return cls(type=ErrorType.UNAUTHORIZED, details=[detail])

    @classmethod
    def forbidden(cls, detail: str = ErrorType.FORBIDDEN) -> Self:
        return cls(type=ErrorType.FORBIDDEN, details=[detail])

    @classmethod
    def system(cls, detail: str = ErrorType.SYSTEM) -> Self:
        return cls(type=ErrorType.SYSTEM, details=[detail])
