from blog.domain.events import PostAlreadyExist


async def notify_developers(event: PostAlreadyExist) -> None:
    for i in range(50):
        print(f'NOTIFY {event}')
