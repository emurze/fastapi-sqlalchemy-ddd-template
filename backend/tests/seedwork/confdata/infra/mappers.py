from seedwork.domain.mappers import IDataMapper
from tests.seedwork.confdata.domain.entities import (
    Example,
    ExampleItem,
    Post,
    User,
    Permission,
)
from tests.seedwork.confdata.domain.value_objects import Address, Photo
from tests.seedwork.confdata.infra.models import (
    ExampleModel,
    ExampleItemModel,
    AddressModel,
    PostModel,
    UserModel,
    PermissionModel,
    PhotoModel,
)


class ExampleMapper(IDataMapper[Example, ExampleModel]):  # should be generated
    def model_to_entity(self, model: ExampleModel) -> Example:
        return Example(
            **model.as_dict(),
            **model.as_alist(
                lambda items: [
                    ExampleItem(
                        **item.as_dict(),
                        **item.as_alist(
                            lambda addresses: [
                                Address(**addr.as_dict()) for addr in addresses
                            ]
                        ),
                    )
                    for item in items
                ]
            ),
        )

    def update_model(self, entity: Example, model: ExampleModel) -> None:
        model.update(
            **entity.model_dump(exclude={"items"}),
            **entity.persist(
                lambda items: [
                    ExampleItemModel(
                        **item.model_dump(exclude={"addresses"}),
                        **item.persist(
                            lambda addresses: [
                                AddressModel(**addr.model_dump())
                                for addr in addresses
                            ],
                        ),
                    )
                    for item in items
                ],
            ),
        )


class PostMapper(IDataMapper[Post, PostModel]):
    def model_to_entity(self, model: PostModel) -> Post:
        return Post(
            **model.as_dict(),
            **model.as_alist(
                lambda users: [
                    User(
                        **user_model.as_dict(),
                        **user_model.as_alist(
                            lambda permissions: [
                                Permission(**perm_model.as_dict())
                                for perm_model in permissions
                            ]
                        ),
                        **user_model.as_rel(
                            lambda photo: Photo(**user_model.photo.as_dict())
                        ),
                    )
                    for user_model in users
                ]
            ),
        )

    def update_model(self, entity: Post, model: PostModel) -> None:
        model.update(
            **entity.model_dump(exclude={"users"}),  # persisted
            **entity.persist(
                lambda users: [
                    UserModel(
                        **user.model_dump(exclude={"permissions", "photo"}),
                        **user.persist(
                            lambda permissions: [
                                PermissionModel(**perm.model_dump())
                                for perm in permissions
                            ]
                        ),
                        **user.persist_one(
                            lambda photo: PhotoModel(**user.photo.model_dump())
                        ),
                    )
                    for user in users
                ],
            ),
        )
