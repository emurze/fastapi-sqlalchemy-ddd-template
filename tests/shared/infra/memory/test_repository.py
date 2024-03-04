import pytest

from tests.shared.conftest import IExampleRepository


async def _add_example(repository: IExampleRepository, name: str) -> None:
    example_dict = {"name": name}
    await repository.add(**example_dict)


async def test_can_add_and_get_example(repository: IExampleRepository) -> None:
    await _add_example(repository, "example")

    example = await repository.get(id=1)

    assert example.id == 1
    assert example.name == "example"


async def test_can_get_for_update_example(
    repository: IExampleRepository
) -> None:
    await _add_example(repository, "example")

    example = await repository.get_for_update(id=1)

    assert example.id == 1
    assert example.name == "example"


async def test_list_examples(repository: IExampleRepository) -> None:
    await _add_example(repository, "example 1")
    await _add_example(repository, "example 2")

    examples = await repository.list()

    assert len(examples) == 2
    assert examples[0].name == "example 1"
    assert examples[1].name == "example 2"


async def test_delete_one_no_id_error(repository: IExampleRepository) -> None:
    with pytest.raises(AssertionError, match="only one id param"):
        await repository.delete_one()


async def test_delete_one_example(repository: IExampleRepository) -> None:
    await _add_example(repository, "example 1")
    await _add_example(repository, "example 2")

    deleted_example = await repository.delete_one(id=2)
    assert deleted_example.id == 2
    assert deleted_example.name == "example 2"

    examples = await repository.list()
    assert len(examples) == 1


async def test_delete_examples(repository: IExampleRepository) -> None:
    await _add_example(repository, "example 1")
    await _add_example(repository, "example 2")

    deleted_examples = await repository.delete()
    assert len(deleted_examples) == 2
    assert deleted_examples[0].name == "example 1"
    assert deleted_examples[1].name == "example 2"

    examples = await repository.list()
    assert len(examples) == 0
