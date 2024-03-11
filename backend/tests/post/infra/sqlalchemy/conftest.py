import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from post.domain.repositories import IPostUnitOfWork, IPostRepository


@pytest.fixture(scope="function")
def uow(sqlalchemy_container) -> IPostUnitOfWork:
    return sqlalchemy_container.post_uow()


@pytest.fixture(scope="function")
def post_repo(sqlalchemy_container, session: AsyncSession) -> IPostRepository:
    return sqlalchemy_container.post_repo(session)
