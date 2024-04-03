from typing import Annotated

from pydantic import AfterValidator


def check_email(val: str) -> str:
    if "@" not in val:
        raise ValueError("Email is invalid.")
    return val


EmailStr = Annotated[str, AfterValidator(check_email)]
