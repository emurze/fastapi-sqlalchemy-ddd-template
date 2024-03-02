from tests.shared.domain.repository import IExampleRepository


async def _add_client(repository: IExampleRepository, name: str) -> None:
    example_dict = {"name": name}
    await repository.add(**example_dict)


async def test_can_add_and_get_example(repository: IExampleRepository) -> None:
    await _add_client(repository, "example")

    example = await repository.get(id=1)

    assert example.id == 1
    assert example.name == "example"


async def test_list_examples(repository: IExampleRepository) -> None:
    await _add_client(repository, "example 1")
    await _add_client(repository, "example 2")

    examples = await repository.list()

    assert len(examples) == 2
    assert examples[0].name == "example 1"
    assert examples[1].name == "example 2"


async def test_delete(repository: IExampleRepository) -> None:
    await _add_client(repository, "example 1")
    await repository.delete(id=1)

    examples = await repository.list()
    assert len(examples) == 0
