from blog.domain.entitites import Publisher
from blog.domain.repositories import IPostRepository
from blog.infra.mappers import PostMapper
from seedwork.infra.repositories import SqlAlchemyRepository, InMemoryRepository
from shared_kernel.utils.functional import id_int_gen


class PostSqlAlchemyRepository(SqlAlchemyRepository, IPostRepository):
    model = Publisher
    mapper = PostMapper


class PostInMemoryRepository(InMemoryRepository, IPostRepository):
    model = Publisher
    mapper = PostMapper
    field_gens = {
        "id": id_int_gen,
    }
