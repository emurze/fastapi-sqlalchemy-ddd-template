import pytest
import sqlalchemy

from auth.domain.uow import IAuthUnitOfWork


async def test_unique_client_username(uow: IAuthUnitOfWork) -> None:
    vlad_data = {"username": "vlad"}

    async with uow:
        await uow.clients.add(**vlad_data)
        await uow.commit()

    async with uow:
        with pytest.raises(sqlalchemy.exc.IntegrityError):
            await uow.clients.add(**vlad_data)


async def test_client_username_is_more_than_or_equal_3_characters_error(
    uow: IAuthUnitOfWork,
) -> None:
    vlad_data = {"username": "vl"}
    async with uow:
        await uow.clients.add(**vlad_data)
        await uow.commit()


async def test_client_username_is_more_than_or_equal_3_characters_success(
    uow: IAuthUnitOfWork,
) -> None:
    vlad_data = {"username": "vld"}
    async with uow:
        await uow.clients.add(**vlad_data)
