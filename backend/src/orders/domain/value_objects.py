from typing import NewType
from uuid import UUID

OrderId = NewType("OrderId", UUID)
CustomerId = NewType("CustomerId", UUID)
