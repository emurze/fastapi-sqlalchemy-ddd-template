class Error:
    CONFLICT: str = "Resource conflict error"
    VALIDATION: str = "Validation error"
    PARAMETERS: str = "Parameters error"
    NOT_FOUND: str = "Resource not found"
    UNAUTHORIZED: str = "Unauthorized error"
    FORBIDDEN: str = "Resource forbidden"
    SYSTEM: str = "Internal system error"

    def __init__(self, detail: str) -> None:
        self.detail = detail

    @classmethod
    def conflict(cls):
        return cls(detail=cls.CONFLICT)

    @classmethod
    def validation(cls):
        return cls(detail=cls.VALIDATION)

    @classmethod
    def not_found(cls):
        return cls(detail=cls.NOT_FOUND)

    @classmethod
    def unauthorized(cls):
        return cls(detail=cls.UNAUTHORIZED)

    @classmethod
    def forbidden(cls):
        return cls(detail=cls.FORBIDDEN)

    @classmethod
    def system(cls):
        return cls(detail=cls.SYSTEM)
