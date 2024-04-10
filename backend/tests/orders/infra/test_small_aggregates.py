import time

import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from iam.infra.models import AccountModel
from orders.infra.models import OrderItemModel, OrderModel, CustomerModel
from tests.conftest import session_factory


@pytest.mark.integration
async def test_(_restart_tables) -> None:
    # todo: test logs

    async with session_factory() as session:
        account = AccountModel(name="Account 1")
        session.add(account)
        await session.commit()

    async with session_factory() as session:
        customer = CustomerModel(account_id=account.id)
        session.add(customer)
        await session.commit()

    async with session_factory() as session:
        order = OrderModel(customer_id=customer.id)
        order.items += (
            OrderItemModel(quantity=1, price=1) for _ in range(2000)
        )
        session.add(order)
        await session.commit()

    t0 = time.perf_counter()
    async with session_factory() as session:
        stmt = (
            select(OrderModel)
            .options(selectinload(OrderModel.items))
        )
        await session.execute(stmt)
    print(f"Time: {time.perf_counter() - t0}")
