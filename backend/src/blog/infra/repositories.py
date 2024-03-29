from blog.domain.entitites import Author, Post
from blog.domain.repositories import IPostRepository
from blog.infra.models import PostModel
from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository


class PostSqlAlchemyRepository(SqlAlchemyRepository, IPostRepository):
    entity_class = Post
    model_class = PostModel


class PostInMemoryRepository(InMemoryRepository, IPostRepository):
    entity_class = Publisher
    field_gens = {
        "id": id_int_gen,
    }
