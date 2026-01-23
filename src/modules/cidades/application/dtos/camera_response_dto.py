"""Camera Response DTO."""
from uuid import UUID

from src.shared.application.dto import DTO


class CameraResponseDTO(DTO):
    """DTO for camera response."""

    id: UUID
    nome: str
    localizacao: str
    url: str
    status: str
    cidade_id: UUID
