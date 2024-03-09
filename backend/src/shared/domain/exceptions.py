class ExceptionMixin(Exception):
    def __init__(self, msg: str = "") -> None:
        super().__init__(msg)


class ResourceNotFoundException(ExceptionMixin):
    pass


class ResourceAlreadyExistsException(ExceptionMixin):
    pass


class ResourceAlreadyDeletedException(ExceptionMixin):
    pass


class InvalidParamInputException(ExceptionMixin):
    pass


class ParameterNotSpecifiedException(ExceptionMixin):
    pass
