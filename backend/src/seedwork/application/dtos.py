from dataclasses import asdict, dataclass, fields
from typing import Any, Self


@dataclass(slots=True)
class DTO:
    def as_dict(self, exclude: set[str] | None = None) -> dict:
        _dict = asdict(self)
        for item in exclude:
            _dict.pop(item)
        return _dict

    def from_model(self, model: Any) -> Self:
        for field in fields(self):
            model_value = getattr(model, field.name)
            setattr(self, field.name, model_value)
        return self
