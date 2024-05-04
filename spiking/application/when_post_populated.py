from spiking.domain.events import PostPopulatedEvent
from spiking.domain.uows import IUnitOfWork


async def update_author(event: PostPopulatedEvent, uow: IUnitOfWork) -> None:
    post = await uow.posts.get_by_id(event.id, for_update=True)
    await post.update_first_author(name="Vlados")
    print("Update author")
