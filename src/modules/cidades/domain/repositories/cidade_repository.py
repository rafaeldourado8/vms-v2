"""Cidade repository interface."""
from abc import abstractmethod
from typing import Optional

from src.modules.cidades.domain.aggregates.cidade import Cidade
from src.modules.cidades.domain.value_objects.cnpj import CNPJ
from src.shared.domain.repository import Repository


class ICidadeRepository(Repository[Cidade]):
    """Cidade repository interface."""

    @abstractmethod
    async def find_by_cnpj(self, cnpj: CNPJ) -> Optional[Cidade]:
        """Find cidade by CNPJ."""
        pass

    @abstractmethod
    async def cnpj_exists(self, cnpj: CNPJ) -> bool:
        """Check if CNPJ already exists."""
        pass

    @abstractmethod
    async def find_by_nome(self, nome: str) -> Optional[Cidade]:
        """Find cidade by nome."""
        pass
