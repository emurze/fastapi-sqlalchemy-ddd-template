from uuid import UUID

import pytest
from sqlalchemy import insert, select

from iam.domain.entities import Account
from orders.domain.entities import Order, OrderItem
from orders.infra.models import CustomerModel, OrderModel
from orders.infra.repositories import OrderMapper
from seedwork.domain.async_structs import alist
from shared.domain.uow import IUnitOfWork


class TestOrder:
    mapper = OrderMapper()

    @staticmethod
    async def _add_customer(uow: IUnitOfWork) -> UUID:
        async with uow:
            account_id = await uow.accounts.add(Account(name='account'))
            await uow.commit()

        async with uow:
            stmt = insert(CustomerModel).values({"account_id": account_id})
            await uow.session.execute(stmt)
            await uow.commit()
            return account_id

    @pytest.mark.integration
    async def test_can_add_item(self, sqlalchemy_uow: IUnitOfWork) -> None:
        customer_id = await self._add_customer(sqlalchemy_uow)

        async with sqlalchemy_uow as uow:
            entity = Order(
                customer_id=customer_id,
                items=alist([OrderItem(quantity=1, price=10)]),
            )
            model = await self.mapper.entity_to_model(entity)
            uow.session.add(model)
            print((await uow.session.execute(select(OrderModel))).scalars())
            # await uow.commit()
            # await uow.session.refresh(model)
            #
            # item = (await model.awaitable_attrs.items)[0]
            # assert item.id == 1
            # assert item.quantity == 1
            # assert item.price == 10
            # assert item.order_id == 1

    @pytest.mark.integration
    async def test_can_add_item_using_repository(
        self, sqlalchemy_uow: IUnitOfWork,
    ) -> None:
        customer_id = await self._add_customer(sqlalchemy_uow)

        async with sqlalchemy_uow as uow:
            order = Order(
                customer_id=customer_id,
                items=alist([OrderItem(quantity=1, price=10)]),
            )
            await uow.orders.add(order)
            await uow.commit()

        async with sqlalchemy_uow as uow:
            model = await uow.orders.get_by_id(order.id)
            item = (await model.awaitable_attrs.items)[0]
            assert item.id == 1
            assert item.quantity == 1
            assert item.price == 10
            assert item.order_id == 1
