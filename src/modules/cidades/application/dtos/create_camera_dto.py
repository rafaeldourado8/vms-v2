"""Create Camera DTO."""
from uuid import UUID

from src.shared.application.dto import DTO


class CreateCameraDTO(DTO):
    """DTO for creating camera."""

    nome: str
    localizacao: str
    url: str
    cidade_id: UUID
