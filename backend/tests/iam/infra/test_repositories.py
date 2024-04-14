import pytest

from iam.domain.entities import Account
from iam.infra.mappers import AccountMapper
from iam.infra.models import AccountModel
from seedwork.domain.services import next_id


class TestAccountMapper:
    mapper = AccountMapper()

    @pytest.mark.unit
    def test_model_to_entity(self) -> None:
        model = AccountModel(id=next_id(), name="user")
        entity = self.mapper.model_to_entity(model)
        assert entity.id == model.id
        assert entity.name == "user"

    @pytest.mark.unit
    def test_entity_to_model(self) -> None:
        entity = Account(name="user")
        model = self.mapper.entity_to_model(entity)
        assert model.id == entity.id
        assert model.name == "user"
