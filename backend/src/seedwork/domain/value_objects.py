from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class Money:
    amount: int = 0
    currency: str = "USD"
