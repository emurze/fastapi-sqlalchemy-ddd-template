import pytest

from post.domain.repositories import IPostUnitOfWork


@pytest.fixture
def uow(container) -> IPostUnitOfWork:
    return container.post_uow()
