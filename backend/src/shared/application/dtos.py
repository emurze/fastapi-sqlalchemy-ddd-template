from typing import Optional, Any, Self


class DTO:
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    @classmethod
    def get_attrs(cls) -> tuple:
        return cls.__dataclass_fields__ # noqa

    def as_dict(
        self,
        exclude: Optional[set] = None,
        exclude_none: bool = False,
    ) -> dict:
        exclude = exclude or set()

        def is_not_in_exclude(attr: Any) -> bool:
            return attr not in exclude

        def is_not_none(attr: Any) -> bool:
            if exclude_none:
                return False if attr is None else True
            return True

        res = {
            attr: value
            for attr in self.get_attrs()
            if all((
                is_not_in_exclude(attr),
                is_not_none(value := getattr(self, attr)),
            ))
        }
        return res

    @classmethod
    def model_from(cls, obj: Any) -> Self:
        return cls(**{name: getattr(obj, name) for name in cls.get_attrs()})
