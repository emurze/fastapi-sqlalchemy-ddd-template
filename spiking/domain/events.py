from uuid import UUID

from seedwork.domain.events import DomainEvent


class PostCreatedEvent(DomainEvent):
    id: UUID


class PostPublishedEvent(DomainEvent):
    id: UUID


class PostPopulatedEvent(DomainEvent):
    id: UUID
