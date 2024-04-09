import pytest
from sqlalchemy import insert

from auth.domain.entities import Account
from orders.domain.entities import Order, OrderItem
from orders.infra.models import CustomerModel, OrderModel, OrderItemModel
from orders.infra.repositories import OrderMapper
from seedwork.domain.uows import IUnitOfWork


class TestOrder:
    mapper = OrderMapper()

    @staticmethod
    async def add_customer(uow: IUnitOfWork) -> int:
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
        # awaitable_attrs
        customer_id = await self.add_customer(sqlalchemy_uow)
        async with sqlalchemy_uow as uow:
            entity = Order(
                customer_id=customer_id,
                items=[OrderItem(quantity=1, price=10)],
            )
            model = self.mapper.entity_to_model(entity)
            uow.session.add(model)
            # await uow.orders.add(Order(customer_id=customer_id))
            await uow.commit()
            await uow.session.refresh(model)
            print(f'RESULT {model=}')
            print(await model.awaitable_attrs.items)

        async with sqlalchemy_uow as uow:
            order = await uow.session.get(OrderModel, 1)
            print(order)
