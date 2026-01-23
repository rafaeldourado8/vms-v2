"""Cidade Response DTO."""
from typing import List
from uuid import UUID

from src.shared.application.dto import DTO


class CidadeResponseDTO(DTO):
    """DTO for cidade response."""

    id: UUID
    nome: str
    cnpj: str
    tipo_plano: str
    dias_retencao: int
    limite_cameras: int
    usuarios: List[dict]
