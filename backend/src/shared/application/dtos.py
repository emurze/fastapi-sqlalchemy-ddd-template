import inspect
from typing import Any, Self

from shared.application.utils import DataclassMixin


class DTO(DataclassMixin):
    def model_from(self, dto: Any) -> Self:
        fields = inspect.getmembers(self)
        for attr, value in (x for x in fields if not x[0].startswith("_")):
            print(attr, value)
