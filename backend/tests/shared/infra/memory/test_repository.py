import pytest

from shared.domain.errors import ResourceNotFoundException
from shared.domain.repositories import IGenericRepository
from tests.shared.conftest_data.domain import Example


@pytest.mark.unit
async def test_can_add_and_get(repo: IGenericRepository) -> None:
    await repo.add(Example(name="example"))

    example = await repo.get(id=1)

    assert example.id == 1
    assert example.name == "example"


@pytest.mark.unit
async def test_get_not_found_error(repo: IGenericRepository) -> None:
    with pytest.raises(ResourceNotFoundException):
        await repo.get(id=1)


@pytest.mark.unit
async def test_can_get_for_update(repo: IGenericRepository) -> None:
    await repo.add(Example(name="example"))

    example = await repo.get_for_update(id=1)

    assert example.id == 1
    assert example.name == "example"


@pytest.mark.unit
async def test_get_for_update_not_found_error(
    repo: IGenericRepository,
) -> None:
    with pytest.raises(ResourceNotFoundException):
        await repo.get_for_update(id=1)


@pytest.mark.unit
async def test_list(repo: IGenericRepository) -> None:
    await repo.add(Example(name="example 1"))
    await repo.add(Example(name="example 2"))

    examples = await repo.list()

    assert len(examples) == 2
    assert examples[0].name == "example 1"
    assert examples[1].name == "example 2"


@pytest.mark.unit
async def test_delete_all(repo: IGenericRepository) -> None:
    await repo.add(Example(name="example 1"))
    await repo.add(Example(name="example 2"))

    await repo.delete()

    examples = await repo.list()
    assert len(examples) == 0


@pytest.mark.unit
async def test_delete_one(repo: IGenericRepository) -> None:
    await repo.add(Example(name="example"))

    await repo.delete(id=1)

    examples = await repo.list()
    assert len(examples) == 0
