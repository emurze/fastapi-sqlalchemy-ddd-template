# import pytest
#
# from shared.application.messagebus import MessageBus
# from tests.shared.conftest_data.application.create_example import (
#     CreateExampleCommand,
#     CreateExampleHandler,
# )
# from tests.shared.conftest_data.application.get_example import (
#     GetExampleQuery,
#     GetExampleHandler,
# )
# from tests.shared.conftest_data.repositories import (
#     ExampleInMemoryUnitOfWork,
#     ExampleInMemoryRepository,
# )
#
# uow = ExampleInMemoryUnitOfWork(examples=ExampleInMemoryRepository)
#
# command_handlers = {
#     CreateExampleCommand: CreateExampleHandler(uow),
# }
# query_handlers = {
#     GetExampleQuery: GetExampleHandler(uow),
# }
#
# message_bus = MessageBus(command_handlers, query_handlers, {})
#
#
# @pytest.mark.unit
# async def test_can_handle_message() -> None:
#     output_dto = await message_bus.handle(CreateExampleCommand(name="Hello"))
#     assert output_dto.status
#     assert output_dto.id == 1
#
#     output_dto_get = await message_bus.handle(GetExampleQuery(id=1))
#     assert output_dto_get.status
#     assert output_dto_get.name == "Hello"
