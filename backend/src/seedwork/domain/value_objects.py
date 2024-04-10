from pydantic import BaseModel, ConfigDict


class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)


class Money(ValueObject):
    amount: int = 0
    currency: str = 'USD'
