import pytest
from fastapi import HTTPException

from shared.application.dtos import SuccessOutputDto, FailedOutputDto
from shared.presentation.utils import raise_errors


@pytest.mark.unit
def test_raise_errors_do_nothing_and_returns_the_same_dto() -> None:
    success_output_dto = SuccessOutputDto()
    assert raise_errors(success_output_dto) == success_output_dto


@pytest.mark.unit
def test_raise_errors_raises_errors() -> None:
    failed_output_dto = FailedOutputDto.build_system_error()
    with pytest.raises(HTTPException, match="System Error"):
        assert raise_errors(failed_output_dto)
