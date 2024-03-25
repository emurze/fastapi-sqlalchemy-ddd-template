from blog.domain.entitites import Post
from blog.infra.models import PostModel
from seedwork.domain.mappers import IDataMapper


class PostMapper(IDataMapper):
    entity_class = Post
    model_class = PostModel

    def model_to_entity(self, instance: PostModel) -> Post:
        return Post(
            id=instance.id,
            title=instance.title,
            content=instance.content,
            draft=instance.draft,
            publisher=instance.publisher,
        )

    def entity_to_model(self, instance: Post) -> PostModel:
        return PostModel(
            id=instance.id,
            title=instance.title,
            content=instance.content,
            draft=instance.draft,
            publisher=instance.publisher,
        )
