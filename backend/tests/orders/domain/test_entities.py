from uuid import UUID

import pytest
from sqlalchemy import insert, select

from iam.domain.entities import Account
from orders.domain.entities import Order, OrderItem
from orders.infra.models import CustomerModel, OrderModel
from orders.infra.repositories import OrderMapper
from seedwork.domain.async_structs import alist
from seedwork.domain.services import next_id
from shared.domain.uow import IUnitOfWork


class TestOrder:
    mapper = OrderMapper()

    @staticmethod
    async def add_customer(uow: IUnitOfWork) -> UUID:
        async with uow:
            account_id = await uow.accounts.add(Account(name='account'))
            await uow.commit()

        async with uow:
            customer_id = next_id()
            stmt = (
                insert(CustomerModel)
                .values({"id": customer_id, "account_id": account_id})
            )
            await uow.session.execute(stmt)
            await uow.commit()
            return customer_id

    @pytest.mark.integration
    async def test_can_repo_add_item(self, sql_uow: IUnitOfWork) -> None:
        customer_id = await self.add_customer(sql_uow)

        async with sql_uow as uow:
            order = Order(
                customer_id=customer_id,
                items=alist([OrderItem(quantity=1, price=10)]),
            )
            await uow.orders.add(order)
            await uow.commit()

        async with sql_uow as uow:
            model = await uow.orders.get_by_id(order.id)
            await model.items.load()
            assert model.items[0].quantity == 1
            assert model.items[0].price == 10
