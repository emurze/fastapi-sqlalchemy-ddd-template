from collections.abc import Callable
from typing import Any as Model, Any, Generator, List

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
    model: type[Model]
    field_gens: dict[str, Callable]

    def __init__(self, gen_manager: type[Any] = GeneratorsManager) -> None:
        self._models: list[Model] = []
        self._gen_manager = gen_manager(self.field_gens)

    async def add(self, **kw) -> Model:
        kw_gen_values = self._gen_manager.iterate_generators(kw)
        instance = self.model(**kw_gen_values)
        self._models.append(instance)
        return instance

    async def get(self, **kw) -> Model:
        return next(
            model
            for model in self._models
            for k, v in kw.items()
            if getattr(model, k) == v
        )

    async def get_for_update(self, **kw) -> Model:
        return await self.get(**kw)

    async def list(self) -> list[Model]:
        return self._models

    async def delete_one(self, **kw) -> Model:
        id_value = kw.get('id')
        assert len(kw) == 1 and id_value is not None, \
            "delete_one accepts only one id parameter"

        for model in self._models:
            if model.id == id_value:
                self._models.remove(model)
                return model

    async def delete(self, **kw) -> List[Model]:
        if not kw:
            removed_models = self._models.copy()
            self._models.clear()
        else:
            removed_models = []
            for key, value in kw.items():
                for model in self._models:
                    if getattr(model, key) == value:
                        self._models.remove(model)
                        removed_models.append(model)
        return removed_models
