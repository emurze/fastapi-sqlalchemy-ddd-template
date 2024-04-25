from seedwork.domain.mappers import IDataMapper
from tests.seedwork.confdata.domain.entities import (
    Example,
    ExampleItem,
    Post,
    Comment,
)
from tests.seedwork.confdata.domain.value_objects import Address
from tests.seedwork.confdata.infra.models import (
    ExampleModel,
    ExampleItemModel,
    AddressModel,
    PostModel,
    CommentModel,
)


class ExampleMapper(IDataMapper[Example, ExampleModel]):  # should be generated
    def model_to_entity(self, model: ExampleModel) -> Example:
        return Example(
            **model.as_dict(),
            **model.as_alist(lambda items: [
                ExampleItem(
                    **item.as_dict(),
                    **item.as_alist(lambda addresses: [
                        Address(**addr.as_dict())
                        for addr in addresses
                    ])
                )
                for item in items
            ])
        )

    def update_model(self, entity: Example, model: ExampleModel) -> None:
        model.update(
            **entity.model_dump(exclude={"items"}),
            **entity.persist(lambda items: [
                ExampleItemModel(
                    **item.model_dump(exclude={"addresses"}),
                    **item.persist(lambda addresses: [
                        AddressModel(
                            **addr.model_dump(),
                            example_item_id=item.id
                        )
                        for addr in addresses
                    ]),
                    example_id=entity.id,
                )
                for item in items
            ])
        )


class PostMapper(IDataMapper[Post, PostModel]):
    def model_to_entity(self, model: PostModel) -> Post:
        return Post(
            **model.as_dict(),
            **model.as_alist(lambda comments: [
                Comment(**comment_model.as_dict())
                for comment_model in comments
            ])
        )

    def update_model(self, entity: Post, model: PostModel) -> None:
        model.update(
            **entity.model_dump(),
            **entity.persist(lambda comments: [
                CommentModel(**comment.model_dump())
                for comment in comments
            ])
        )
