from dataclasses import asdict, dataclass


@dataclass
class DataclassMixin:
    def as_dict(self, exclude: set):
        return {
            attr: getattr(self, attr)
            for attr in self.__dataclass_fields__  # noqa
            if attr not in exclude
        }
