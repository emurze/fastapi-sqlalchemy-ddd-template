from dataclasses import asdict, dataclass, fields
from typing import Any, Self


@dataclass(slots=True)
class DTO:
    def as_dict(
        self,
        exclude: set | None = None,
        exclude_none: bool = False,
    ) -> dict:
        dto_dict = asdict(self)

        if exclude:
            for item in exclude:
                dto_dict.pop(item)

        if exclude_none:
            dto_dict = {k: v for k, v in dto_dict.items() if v is not None}

        return dto_dict

    def from_model(self, model: Any) -> Self:
        for field in fields(self):
            model_value = getattr(model, field.name)
            setattr(self, field.name, model_value)
        return self
