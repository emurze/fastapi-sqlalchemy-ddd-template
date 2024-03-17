from collections.abc import Callable
from typing import Any, Generator, cast

from shared.domain.entities import AggregateRoot
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
        self._models: dict[int, AggregateRoot] = {}
        self._gen_manager = gen_manager(self.field_gens)
        self.model = cast(Any, self.aggregate_root)

    async def add(self, entity: AggregateRoot) -> int:
        kw_gen_values = self._gen_manager.iterate_gens(entity.as_dict())
        extended_instance = self.model(**kw_gen_values)
        self._models[extended_instance.id] = extended_instance
        return extended_instance.id

    async def delete(self, entity: AggregateRoot) -> None:
        del self._models[entity.id]

    async def delete_by_id(self, entity_id: int) -> None:
        del self._models[entity_id]

    async def get_by_id(
        self, entity_id: int, for_update: bool = False
    ) -> AggregateRoot | None:
        try:
            return next(
                model
                for model in self._models.values()
                if model.id == entity_id
            )
        except StopIteration:
            return None

    async def count(self) -> int:
        return len(self._models)

    async def list(self) -> list[AggregateRoot]:
        return list(self._models.values())

    def collect_events(self):
        pass
