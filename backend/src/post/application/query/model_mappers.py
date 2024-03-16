from dataclasses import dataclass

from shared.application.utils import DataclassMixin
from shared.domain.entities import Entity


@dataclass
class GetPostDTO(DataclassMixin):
    id: int
    title: str
    content: str
    draft: bool


def map_post_model_to_dto(instance: Entity) -> GetPostDTO:
    return GetPostDTO.model_from(instance)
