import pytest

from auth.domain.entities import Account
from auth.domain.value_objects import AccountId
from auth.infra.mappers import AccountMapper
from auth.infra.models import AccountModel


class TestAccountMapper:
    mapper = AccountMapper()

    @pytest.mark.unit
    def test_entity_to_model(self) -> None:
        entity = Account(id=AccountId(1), name="user")
        model = self.mapper.entity_to_model(entity)
        assert model.id == 1
        assert model.name == "user"

    @pytest.mark.unit
    def test_model_to_entity(self) -> None:
        model = AccountModel(id=1, name="user")
        entity = self.mapper.model_to_entity(model)
        assert entity == Account(id=AccountId(1), name="user")
