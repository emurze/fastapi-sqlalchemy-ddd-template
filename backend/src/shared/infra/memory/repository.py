from collections.abc import Callable
from typing import Any, Generator, NoReturn

from shared.domain.entities import AggregateRoot, EntityId
from shared.domain.exceptions import ResourceNotFoundException
from shared.domain.repositories import IGenericRepository


class GeneratorsManager:
    """
    Imitates database triggers and sequences
    """

    initialized_gens: dict[str, Generator]

    def __init__(self, field_gens: dict[str, Callable]):
        self.initialized_gens = self.initialize_gens(field_gens)

    @staticmethod
    def initialize_gens(field_gens) -> dict[str, Generator]:
        return {field: gen() for field, gen in field_gens.items()}

    def iterate_gens(self, kw: dict) -> dict:
        return kw | {
            field: next(gen)
            for field, gen in self.initialized_gens.items()
            if not kw.get(field)
        }


class InMemoryRepository(IGenericRepository):
    aggregate_root: type[AggregateRoot]
    field_gens: dict[str, Callable]

    def __init__(self, gen_manager: type[Any] = GeneratorsManager) -> None:
        self._models: dict[EntityId, AggregateRoot] = {}
        self._gen_manager = gen_manager(self.field_gens)

    @property
    def model(self) -> type[Any]:
        return self.aggregate_root

    async def add(self, entity: AggregateRoot) -> EntityId:
        kw_gen_values = self._gen_manager.iterate_gens(entity.to_dict())
        extended_instance = self.model(**kw_gen_values)
        self._models[extended_instance.id] = extended_instance
        return extended_instance.id

    async def delete(self, entity_id: EntityId) -> None:
        del self._models[entity_id]

    async def get(self, **kw) -> NoReturn | AggregateRoot:
        try:
            return next(
                model
                for model in self._models.values()
                for k, v in kw.items()
                if getattr(model, k) == v
            )
        except StopIteration:
            raise ResourceNotFoundException()

    async def get_for_update(self, **kw) -> NoReturn | AggregateRoot:
        return await self.get(**kw)

    async def list(self) -> list[AggregateRoot]:
        return list(self._models.values())
