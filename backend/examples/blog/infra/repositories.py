from blog.domain.entitites import Post
from blog.domain.repositories import IPostRepository
from blog.infra.models import PostModel
from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository
from seedwork.utils.functional import id_int_gen


class PostSqlAlchemyRepository(SqlAlchemyRepository, IPostRepository):
    entity_class = Post
    model_class = PostModel


class PostInMemoryRepository(InMemoryRepository, IPostRepository):
    entity_class = Post
    field_gens = {
        "id": id_int_gen,
    }
