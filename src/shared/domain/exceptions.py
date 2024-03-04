

class ExceptionMixin(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)


class ResourceNotFoundError(ExceptionMixin):
    pass


class ResourceAlreadyExistsError(ExceptionMixin):
    pass


class ResourceAlreadyDeletedError(ExceptionMixin):
    pass


class InvalidParamInputError(ExceptionMixin):
    pass


class ParameterNotSpecifiedError(ExceptionMixin):
    pass
