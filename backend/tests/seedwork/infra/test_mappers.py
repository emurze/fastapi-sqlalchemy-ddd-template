import pytest

from seedwork.domain.structs import alist, arel
from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain.entities import (
    Example,
    ExampleItem,
    Post,
    User,
    Permission,
)
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork
from tests.seedwork.confdata.domain.value_objects import Address, Photo
from tests.seedwork.confdata.infra.mappers import ExampleMapper, PostMapper
from tests.seedwork.confdata.infra.models import (
    ExampleModel,
    ExampleItemModel,
    AddressModel,
    PostModel,
)

post_mapper = PostMapper(PostModel)
mapper = ExampleMapper(ExampleModel)


def make_example_model() -> ExampleModel:
    return ExampleModel(
        id=next_id(),
        name="Example1",
        items=[
            ExampleItemModel(
                id=next_id(),
                name="ExampleItem1",
                addresses=[
                    AddressModel(id=next_id(), city="Kiev"),
                ],
            )
        ],
    )


def make_example_entity() -> Example:
    return Example(
        name="Example1",
        items=alist(
            [
                ExampleItem(
                    name="ExampleItem1",
                    addresses=alist([Address(city="Kiev")]),
                )
            ]
        ),
    )


@pytest.mark.unit
async def test_model_to_entity() -> None:
    entity = mapper.model_to_entity(make_example_model())
    await entity.items.load()
    await entity.items[0].addresses.load()
    assert entity.name == "Example1"
    assert entity.items[0].name == "ExampleItem1"
    assert entity.items[0].addresses[0].city == "Kiev"


@pytest.mark.unit
def test_can_add_using_entity_with_list_loading() -> None:
    model = mapper.entity_to_model(make_example_entity())
    assert model.name == "Example1"
    assert model.items[0].name == "ExampleItem1"
    assert model.items[0].addresses[0].city == "Kiev"


@pytest.mark.unit
def test_can_update_without_extra_loading() -> None:
    model = make_example_model()
    entity = mapper.model_to_entity(model)
    entity.name = "Vlados"
    mapper.update_model(entity, model)
    assert entity.items.is_loaded() is False
    assert model.name == "Vlados"
    assert model.items[0].name == "ExampleItem1"
    assert model.items[0].addresses[0].city == "Kiev"


@pytest.mark.unit
async def test_can_update_with_loaded_items() -> None:
    model = make_example_model()
    entity = mapper.model_to_entity(model)
    entity.name = "Vlados"
    await entity.items.load()
    await entity.items[0].addresses.load()
    mapper.update_model(entity, model)
    assert entity.items.is_loaded() is True
    assert model.name == "Vlados"
    assert model.items[0].name == "ExampleItem1"
    assert model.items[0].addresses[0].city == "Kiev"


# @pytest.mark.marked
@pytest.mark.integration
async def test_mapper_updates_o2m_m2o(sql_uow: ITestUnitOfWork) -> None:
    async with sql_uow as uow:
        model = Example(
            name="Hello",
            items=alist(
                ExampleItem(
                    name="Item A",
                    addresses=alist(Address(city="Lersk") for _ in range(2)),
                )
                for _ in range(2)
            ),
        )
        # Just appends model as one piece
        uow.examples.add(model)
        await uow.commit()

    async with sql_uow as uow:
        entity = await uow.examples.get_by_id(model.id)
        await entity.items.load()
        await entity.items[0].addresses.load()

        entity.name = "Item Vlad"
        entity.items.pop()  # relation.pop, for each item.pop()
        entity.items.append(  # relation.append as one piece
            ExampleItem(
                name="Item B", addresses=alist([Address(city="lersk")])
            )
        )
        entity.items.append(ExampleItem(name="Item C"))  # relation.append

        entity.items[0].name = "New Item"
        entity.items[0].addresses.pop(0)
        entity.items[0].addresses.append(Address(city="Vladivostok"))
        entity.items[0].addresses.append(Address(city="Vladivostok 2"))
        entity.items[0].addresses[0] = Address(city="Vladivostok -1")
        entity.items[-1].name = "Best Item"
        await uow.commit()


@pytest.mark.marked
@pytest.mark.integration
async def test_mapper_can_update_m2m_o2o(sql_uow: ITestUnitOfWork) -> None:
    # todo: OneToOne
    async with sql_uow as uow:
        entity = Post(
            title="Post 1",
            users=alist(
                User(
                    name=f"User {index + 1}",
                    permissions=alist(
                        Permission(name="Perm") for _ in range(3)
                    ),
                    photo=arel(Photo(url="URL", context="cats")),
                )
                for index in range(4)
            ),
        )
        uow.posts.add(entity)
        await uow.commit()

    async with sql_uow as uow:
        post = await uow.posts.get_by_id(entity.id)
        await post.users.load()
        post.title = "New Post"
        post.users.pop(0)
        post.users.pop(0)
        post.users[0].name = "New User"
        await post.users[0].photo.load()
        post.users[0].photo = None
        post.users.append(
            User(
                name="Vlados", permissions=alist([Permission(name="Perm -1")])
            )
        )
        user_3 = post.users.find_one(name="User 4")
        await user_3.photo.load()
        user_3.photo = arel(Photo(url="DOG", context="dogs"))  # todo: problem
        await user_3.permissions.load()
        user_3.permissions.pop()
        user_3.permissions.pop()
        user_3.permissions.append(Permission(name="New Perm"))
        await uow.commit()

    async with sql_uow as uow:
        post = await uow.posts.get_by_id(entity.id)
        await post.users.load()
        assert len(post.users) == 3
        assert (new_user := post.users.find_one(name="New User"))
        assert await new_user.photo.load() is None
        assert post.users.find_one(name="Vlados")
        assert (user_3 := post.users.find_one(name="User 4"))
        assert len(await user_3.permissions.load()) == 2
        photo = await user_3.photo.load()
        assert photo.url == "DOG" and photo.context == "dogs"
        assert user_3.permissions.find_one(name="Perm")
        assert user_3.permissions.find_one(name="New Perm")


@pytest.mark.unit
async def test_mem_mapper_updates_o2m_m2o(
    mem_uow: ITestUnitOfWork,
) -> None:
    await test_mapper_updates_o2m_m2o(mem_uow)


@pytest.mark.unit
async def test_mem_mapper_updates_m2m_o2o(mem_uow: ITestUnitOfWork) -> None:
    await test_mapper_can_update_m2m_o2o(mem_uow)
