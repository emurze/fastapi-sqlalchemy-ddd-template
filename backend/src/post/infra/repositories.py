from post.domain.entitites import Post
from post.domain.repositories import IPostRepository, IPostUnitOfWork
from shared.infra.memory.repository import InMemoryRepository
from shared.infra.memory.uow import InMemoryUnitOfWork
from shared.infra.memory.utils import id_int_gen
from shared.infra.sqlalchemy_orm.repository import SqlAlchemyRepository
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork


class PostSqlAlchemyRepository(SqlAlchemyRepository, IPostRepository):
    model = Post


class PostSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IPostUnitOfWork):
    pass


class PostInMemoryRepository(InMemoryRepository, IPostRepository):
    model = Post
    field_gens = {
        "id": id_int_gen,
    }


class PostInMemoryUnitOfWork(InMemoryUnitOfWork, IPostUnitOfWork):
    pass
