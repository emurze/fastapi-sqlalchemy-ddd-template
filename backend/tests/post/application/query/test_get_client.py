import pytest

from auth.domain.uow import IAuthUnitOfWork


@pytest.mark.unit
async def test_can_get_client(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")

    container

    assert result.status is True
    assert client.id == 1


@pytest.mark.unit
async def test_get_client_not_found_error(uow: IAuthUnitOfWork) -> None:
    handler = GetClientHandler(uow)
    query = GetClientQuery(id=1)
    result = await handler.execute(query)
    assert result.status is False
