from sqlalchemy.orm import DeclarativeBase


class TestModel(DeclarativeBase):
    __allow_unmapped__ = True

    def __str__(self) -> str:
        arguments = ", ".join(
            f"{k}={v}" for k, v in self.__dict__.items()
            if not k.startswith("_")
        )
        return f"{type(self).__name__}({arguments})"
