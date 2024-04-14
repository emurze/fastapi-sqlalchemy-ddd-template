import asyncio
import os
import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import Mapped, relationship

sys.path.append(os.path.join(sys.path[0], 'src'))  # noqa

from seedwork.domain.async_structs import alist, map_coro
from seedwork.domain.entities import Entity
from seedwork.domain.mappers import IDataMapper
from seedwork.domain.services import UUIDField, next_id
from shared.infra.database import Model

async_engine = create_async_engine(
    'postgresql+asyncpg://adm1:12345678@localhost:5432/learning',
    echo=True,
    pool_size=10,
    max_overflow=0,
)
session_factory = async_sessionmaker(async_engine)


class UserModel(Model):
    __tablename__ = "user"
    id = sa.Column(sa.UUID, primary_key=True, default=next_id)
    name = sa.Column(sa.String, nullable=False)
    posts: Mapped[list['PostModel']] = relationship()


class PostModel(Model):
    __tablename__ = "post"
    id = sa.Column(sa.UUID, primary_key=True, default=next_id)
    title = sa.Column(sa.String, nullable=False)
    user_id = sa.Column(sa.UUID, sa.ForeignKey('user.id'))


class User(Entity):
    id: UUID = UUIDField
    name: str
    posts: alist['Post'] = alist()


class Post(Entity):
    id: UUID = UUIDField
    title: str


class UserMapper(IDataMapper):
    async def model_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            posts=alist(map_coro(Post, lambda: model.awaitable_attrs.posts)),
        )

    async def entity_to_model(self, entity: User) -> UserModel:
        model = UserModel(id=entity.id, name=entity.name)
        entity.posts.map_relation(model.posts, PostModel)
        return model


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)
        await conn.commit()


async def model_to_entity_then_entity_to_model() -> None:
    mapper = UserMapper()
    async with session_factory() as session:
        user = User(id=next_id(), name="Vlad", posts=alist([Post(title="Post")]))
        model = await mapper.entity_to_model(user)
        session.add(model)
        await session.commit()

    async with session_factory() as session:
        user2 = await session.get(UserModel, user.id)
        if user2 is None:
            return None
        entity = await mapper.model_to_entity(user2)
        print(await entity.posts.load())

    model = UserModel(id=next_id(), name="Vlad")
    model.posts.append(PostModel(id=next_id(), title="Post"))
    entity = await mapper.model_to_entity(model)
    print(await entity.posts.load())
    print(entity)


async def main() -> None:
    print('RUN MAIN')
    await create_tables()
    await model_to_entity_then_entity_to_model()


if __name__ == '__main__':
    asyncio.run(main())
