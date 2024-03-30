import pytest

from blog.domain.repositories import IPostRepository
from seedwork.domain.uows import IUnitOfWork


@pytest.fixture(scope="function")
def uow(sqlalchemy_container, _restart_tables) -> IUnitOfWork:
    return sqlalchemy_container.uow()


@pytest.fixture(scope="function")
async def repo(uow: IUnitOfWork) -> IPostRepository:
    async with uow:
        yield uow.posts
