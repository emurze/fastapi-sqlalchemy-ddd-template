import itertools
from dataclasses import dataclass
from typing import NoReturn

from sqlalchemy import select, insert, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import Entity
from seedwork.domain.errors import EntityAlreadyExistsError
from seedwork.domain.events import Event
from seedwork.domain.mapper import IMapper
from seedwork.domain.repositories import IGenericRepository

from collections.abc import Callable, Iterator
from typing import Any, Generator

from seedwork.domain.value_objects import Deferred
from seedwork.infra.database import Model


@dataclass(frozen=True, slots=True)
class Mapper(IMapper):
    entity_class: type[Entity]
    model_class: type[Model]

    def entity_to_model(self, entity: Entity) -> Model:
        return self.model_class(**entity.model_dump())

    def model_to_entity(self, model: Model) -> Entity:
        return self.entity_class.model_validate(model)


class SqlAlchemyRepository(IGenericRepository):
    entity_class: type[Entity]
    model_class: type[Model]
    mapper_class: type[IMapper] = Mapper

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._mapper = self.mapper_class(self.entity_class, self.model_class)
        self._identity_map = {}

    async def add(self, entity: Entity) -> NoReturn | int:
        try:
            stmt = (
                insert(self.model_class)
                .values(**entity.model_dump(exclude_deferred=True))
                .returning(self.model_class)
                # todo: returns only deferred fields
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one()
            entity.insert_deferred_values(model)
            self._identity_map[entity.id] = entity
            return entity.id
        except IntegrityError:
            raise EntityAlreadyExistsError()

    async def delete(self, entity: Entity) -> None:
        query = delete(self.model_class).filter_by(id=entity.id)
        await self.session.execute(query)

    async def delete_by_id(self, entity_id: int) -> None:
        query = delete(self.model_class).filter_by(id=entity_id)
        await self.session.execute(query)

    async def get_by_id(
        self,
        entity_id: int,
        for_share: bool = False,
        for_update: bool = False,
    ) -> Entity | None:
        query = select(self.model_class).filter_by(id=entity_id)

        if for_share:
            query = query.with_for_update(key_share=True, read=True)
        elif for_update:
            query = query.with_for_update()

        res = await self.session.execute(query)
        model = res.scalars().first()

        if model is None:
            return None

        entity = self._mapper.model_to_entity(model)

        # Saves store_entity events
        if store_entity := self._identity_map.get(entity.id):
            return store_entity

        self._identity_map[entity.id] = entity
        return entity

    async def count(self) -> int:
        query = select(func.Count(self.model_class))
        res = await self.session.execute(query)
        return res.scalar_one()

    def collect_events(self) -> Iterator[Event]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self._identity_map.values()
        )


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
            if kw.get(field) == Deferred
        }


class InMemoryRepository(IGenericRepository):
    entity_class: type[Entity]
    field_gens: dict[str, Callable]

    def __init__(self, gen_manager: type[Any] = GeneratorsManager) -> None:
        self._objects: dict[int, Entity] = {}
        self._gen_manager = gen_manager(self.field_gens)

    async def add(self, entity: Entity) -> int:
        kw_gen_values = self._gen_manager.iterate_gens(entity.model_dump())
        extended_instance = self.entity_class(**kw_gen_values)
        entity.insert_deferred_values(extended_instance)
        self._objects[extended_instance.id] = extended_instance
        return extended_instance.id

    async def delete(self, entity: Entity) -> None:
        del self._objects[entity.id]

    async def delete_by_id(self, entity_id: int) -> None:
        del self._objects[entity_id]

    async def get_by_id(
        self,
        entity_id: int,
        for_share: bool = False,
        for_update: bool = False
    ) -> Entity | None:
        try:
            return next(
                model
                for model in self._objects.values()
                if model.id == entity_id
            )
        except StopIteration:
            return None

    async def count(self) -> int:
        return len(self._objects)

    async def list(self) -> list[Entity]:
        return list(self._objects.values())

    def collect_events(self) -> Iterator[Event]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self._objects.values()
        )
