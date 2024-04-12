import pytest

from iam.domain.entities import Account
from iam.domain.value_objects import AccountId
from iam.infra.models import AccountModel
from iam.infra.repositories import AccountMapper
from seedwork.domain.services import next_id


class TestAccountMapper:
    mapper = AccountMapper()

    @pytest.mark.unit
    def test_entity_to_model(self) -> None:
        entity = Account(id=AccountId(next_id()), name="user")
        model = self.mapper.entity_to_model(entity)
        assert model.id == 1
        assert model.name == "user"

    @pytest.mark.unit
    def test_model_to_entity(self) -> None:
        model = AccountModel(id=1, name="user")
        entity = self.mapper.model_to_entity(model)
        assert entity == Account(id=AccountId(1), name="user")
