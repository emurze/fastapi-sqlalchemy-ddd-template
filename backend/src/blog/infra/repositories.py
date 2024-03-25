from blog.domain.entitites import Publisher
from blog.domain.repositories import IPostRepository
from blog.infra.mappers import PostMapper
from seedwork.infra.functional import id_int_gen
from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository


class PostSqlAlchemyRepository(SqlAlchemyRepository, IPostRepository):
    model = Publisher
    mapper = PostMapper


class PostInMemoryRepository(InMemoryRepository, IPostRepository):
    model = Publisher
    mapper = PostMapper
    field_gens = {
        "id": id_int_gen,
    }
