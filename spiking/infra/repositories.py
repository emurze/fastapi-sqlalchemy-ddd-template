from seedwork.infra.repository import SqlAlchemyRepository
from spiking.domain.entities import Post


class PostSqlAlchemyRepository(SqlAlchemyRepository):
    entity_class = Post
