from typing import NewType

from pydantic import PositiveInt

OrderId = NewType('OrderId', PositiveInt)
CustomerId = NewType('CustomerId', PositiveInt)
