import pytest

from post.domain.repositories import IPostUnitOfWork


@pytest.fixture(scope="function")
def uow(container) -> IPostUnitOfWork:
    return container.post_uow()
