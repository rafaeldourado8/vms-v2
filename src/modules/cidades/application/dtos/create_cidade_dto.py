"""Create Cidade DTO."""
from src.shared.application.dto import DTO


class CreateCidadeDTO(DTO):
    """DTO for creating cidade."""

    nome: str
    cnpj: str
    tipo_plano: str
