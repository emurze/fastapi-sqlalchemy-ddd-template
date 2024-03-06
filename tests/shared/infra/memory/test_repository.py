import pytest

from shared.domain.exceptions import ResourceNotFoundError
from tests.shared.conftest import IExampleRepository


async def add_example(repo: IExampleRepository, name: str) -> None:
    example_dict = {"name": name}
    await repo.add(**example_dict)


@pytest.mark.unit
async def test_can_add_and_get(repo: IExampleRepository) -> None:
    await add_example(repo, "example")

    example = await repo.get(id=1)

    assert example.id == 1
    assert example.name == "example"


@pytest.mark.unit
async def test_get_not_found_error(repo: IExampleRepository) -> None:
    with pytest.raises(ResourceNotFoundError):
        await repo.get(id=1)


@pytest.mark.unit
async def test_can_get_for_update(repo: IExampleRepository) -> None:
    await add_example(repo, "example")

    example = await repo.get_for_update(id=1)

    assert example.id == 1
    assert example.name == "example"


@pytest.mark.unit
async def test_get_for_update_not_found_error(
    repo: IExampleRepository,
) -> None:
    with pytest.raises(ResourceNotFoundError):
        await repo.get_for_update(id=1)


@pytest.mark.unit
async def test_list(repo: IExampleRepository) -> None:
    await add_example(repo, "example 1")
    await add_example(repo, "example 2")

    examples = await repo.list()

    assert len(examples) == 2
    assert examples[0].name == "example 1"
    assert examples[1].name == "example 2"


@pytest.mark.unit
async def test_delete_one(repo: IExampleRepository) -> None:
    await add_example(repo, "example 1")
    await add_example(repo, "example 2")

    deleted_example = await repo.delete_one(id=2)
    assert deleted_example.id == 2
    assert deleted_example.name == "example 2"

    examples = await repo.list()
    assert len(examples) == 1


@pytest.mark.unit
async def test_delete_one_no_id_error(repo: IExampleRepository) -> None:
    with pytest.raises(AssertionError, match="only one id param"):
        await repo.delete_one()


@pytest.mark.unit
async def test_delete_one_not_found_error(repo: IExampleRepository) -> None:
    with pytest.raises(ResourceNotFoundError):
        await repo.delete_one(id=1)


@pytest.mark.unit
async def test_delete(repo: IExampleRepository) -> None:
    await add_example(repo, "example 1")
    await add_example(repo, "example 2")

    deleted_examples = await repo.delete()
    assert len(deleted_examples) == 2
    assert deleted_examples[0].name == "example 1"
    assert deleted_examples[1].name == "example 2"

    examples = await repo.list()
    assert len(examples) == 0
