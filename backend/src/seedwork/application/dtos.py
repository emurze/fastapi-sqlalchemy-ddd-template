from dataclasses import asdict, fields
from typing import Any, Self


class DTO:
    """
    Inherit this DTO superclass to enhance your dataclass implementations.
    """

    def as_dict(
        self,
        exclude: set | None = None,
        exclude_none: bool = True,
    ) -> dict:
        dto_dict = asdict(self)  # noqa

        if exclude:
            for item in exclude:
                dto_dict.pop(item)

        if exclude_none:
            dto_dict = {k: v for k, v in dto_dict.items() if v is not None}

        return dto_dict

    @classmethod
    def from_model(cls, model: Any) -> Self:
        dto_cls_fields = fields(cls)  # noqa
        model_kw = {f.name: getattr(model, f.name) for f in dto_cls_fields}
        return cls(**model_kw)  # noqa
