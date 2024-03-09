from dataclasses import dataclass, field


@dataclass
class Entity:
    id: int = field(hash=True)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update id"
        for key, value in kw.items():
            setattr(self, key, value)


class AggregateRoot(Entity):
    """Root Aggregate"""
