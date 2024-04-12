import re
from typing import Annotated

from pydantic import AfterValidator


def check_email(value: str) -> str:
    if "@" not in value:
        raise ValueError("Email is invalid.")
    return value


def check_slug(value: str) -> str:
    if not re.match(r'^[-\w]+$', value):
        raise ValueError("Slug is invalid.")
    return value


SlugStr = Annotated[str, AfterValidator(check_slug)]
EmailStr = Annotated[str, AfterValidator(check_email)]
