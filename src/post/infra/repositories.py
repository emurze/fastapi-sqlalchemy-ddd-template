from post.domain.entitites import Post
from shared.domain.repository import IGenericRepository
from shared.domain.uow import IGenericUnitOfWork
from shared.infra.memory.repository import InMemoryRepository
from shared.infra.memory.uow import InMemoryUnitOfWork
from shared.infra.memory.utils import id_int_gen
from shared.infra.sqlalchemy_orm.repository import SqlAlchemyRepository
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork


class PostSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    model = Post


class PostSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IGenericUnitOfWork):
    pass


class PostInMemoryRepository(InMemoryRepository, IGenericRepository):
    model = Post
    field_gens = {
        "id": id_int_gen,
    }


class PostInMemoryUnitOfWork(InMemoryUnitOfWork, IGenericUnitOfWork):
    pass
