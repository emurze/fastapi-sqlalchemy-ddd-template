import pytest

from blog.domain.repositories import IPostRepository
from seedwork.domain.uows import IUnitOfWork


@pytest.fixture(scope="function")
def uow(sqlalchemy_container, _restart_tables) -> IUnitOfWork:
    uow = sqlalchemy_container.uow()
    print(uow.session_factory.kw['bind'].url)
    print(dir(uow.session_factory))
    return uow


@pytest.fixture(scope="function")
async def repo(uow: IUnitOfWork) -> IPostRepository:
    async with uow:
        yield uow.posts
