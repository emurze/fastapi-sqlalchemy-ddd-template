from collections.abc import Callable
from typing import Any as Model, Any, Generator, NoReturn

from shared.domain.exceptions import ResourceNotFoundException
from shared.domain.repository import IGenericRepository


class GeneratorsManager:
    """
    Imitates database triggers and sequences
    """

    initialized_gens: dict[str, Generator]

    def __init__(self, field_gens: dict[str, Callable]):
        self.initialized_gens = self.initialize_generators(field_gens)

    @staticmethod
    def initialize_generators(field_gens) -> dict[str, Generator]:
        return {field: gen() for field, gen in field_gens.items()}

    def iterate_generators(self, kw: dict) -> dict:
        return kw | {
            field: next(gen)
            for field, gen in self.initialized_gens.items()
            if not kw.get(field)
        }


class InMemoryRepository(IGenericRepository):
    aggregate_root: type[Model]
    field_gens: dict[str, Callable]

    def __init__(self, gen_manager: type[Any] = GeneratorsManager) -> None:
        self._models: list[Model] = []
        self._gen_manager = gen_manager(self.field_gens)

    @property
    def model(self) -> type[Model]:
        return self.aggregate_root

    async def add(self, instance: Model) -> int:
        instance_dict = instance.to_dict()
        kw_gen_values = self._gen_manager.iterate_generators(instance_dict)
        instance_with_generated_fields = self.model(**kw_gen_values)
        self._models.append(instance_with_generated_fields)
        return instance.id

    async def delete(self, **kw) -> None:
        if not kw:
            self._models.clear()
        else:
            for key, value in kw.items():
                for model in self._models:
                    if getattr(model, key) == value:
                        self._models.remove(model)

    async def get(self, **kw) -> NoReturn | Model:
        try:
            return next(
                model
                for model in self._models
                for k, v in kw.items()
                if getattr(model, k) == v
            )
        except StopIteration:
            raise ResourceNotFoundException()

    async def get_for_update(self, **kw) -> NoReturn | Model:
        return await self.get(**kw)

    async def list(self) -> list[Model]:
        return self._models
