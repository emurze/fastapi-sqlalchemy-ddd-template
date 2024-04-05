from seedwork.domain.events import Event


class NameChanged(Event):
    name: str


async def notify_developers(event: NameChanged) -> None:
    print(f'NOTIFY DEVELOPERS {event.name}')
