"""Cidade repository implementation."""
from typing import List, Optional
from uuid import UUID

from src.modules.cidades.domain.aggregates.cidade import Cidade
from src.modules.cidades.domain.entities.plano import Plano, TipoPlano
from src.modules.cidades.domain.entities.usuario_cidade import TipoUsuarioCidade, UsuarioCidade
from src.modules.cidades.domain.repositories.cidade_repository import ICidadeRepository
from src.modules.cidades.domain.value_objects.cnpj import CNPJ
from src.modules.cidades.domain.value_objects.limite_cameras import LimiteCameras
from src.modules.cidades.infrastructure.persistence.models import (
    CidadeModel,
    PlanoModel,
    UsuarioCidadeModel,
)


class CidadeRepository(ICidadeRepository):
    """Cidade repository implementation using Django ORM."""

    async def save(self, aggregate: Cidade) -> None:
        """Save cidade aggregate."""
        plano_model, _ = await PlanoModel.objects.aget_or_create(
            id=aggregate.plano.id if aggregate.plano else None,
            defaults={
                "tipo": aggregate.plano.tipo.value if aggregate.plano else "BASICO",
                "nome": aggregate.plano.nome if aggregate.plano else "Básico",
            },
        )

        cidade_model, created = await CidadeModel.objects.aget_or_create(
            id=aggregate.id,
            defaults={
                "nome": aggregate.nome,
                "cnpj": aggregate.cnpj.value,
                "plano": plano_model,
                "limite_cameras": aggregate.limite_cameras.value,
            },
        )

        if not created:
            cidade_model.nome = aggregate.nome
            cidade_model.cnpj = aggregate.cnpj.value
            cidade_model.plano = plano_model
            cidade_model.limite_cameras = aggregate.limite_cameras.value
            await cidade_model.asave()

        # Sync usuarios
        await UsuarioCidadeModel.objects.filter(cidade=cidade_model).adelete()
        for usuario in aggregate.usuarios:
            await UsuarioCidadeModel.objects.acreate(
                id=usuario.id,
                cidade=cidade_model,
                user_id=usuario.user_id,
                tipo=usuario.tipo.value,
            )

    async def find_by_id(self, aggregate_id: UUID) -> Optional[Cidade]:
        """Find cidade by ID."""
        try:
            cidade_model = await CidadeModel.objects.select_related("plano").aget(
                id=aggregate_id
            )
            return await self._to_domain(cidade_model)
        except CidadeModel.DoesNotExist:
            return None

    async def find_by_cnpj(self, cnpj: CNPJ) -> Optional[Cidade]:
        """Find cidade by CNPJ."""
        try:
            cidade_model = await CidadeModel.objects.select_related("plano").aget(
                cnpj=cnpj.value
            )
            return await self._to_domain(cidade_model)
        except CidadeModel.DoesNotExist:
            return None

    async def cnpj_exists(self, cnpj: CNPJ) -> bool:
        """Check if CNPJ exists."""
        return await CidadeModel.objects.filter(cnpj=cnpj.value).aexists()

    async def find_by_nome(self, nome: str) -> Optional[Cidade]:
        """Find cidade by nome."""
        try:
            cidade_model = await CidadeModel.objects.select_related("plano").aget(nome=nome)
            return await self._to_domain(cidade_model)
        except CidadeModel.DoesNotExist:
            return None

    async def find_all(self) -> List[Cidade]:
        """Find all cidades."""
        cidade_models = CidadeModel.objects.select_related("plano").all()
        return [await self._to_domain(cm) async for cm in cidade_models]

    async def delete(self, aggregate_id: UUID) -> None:
        """Delete cidade."""
        await CidadeModel.objects.filter(id=aggregate_id).adelete()

    async def _to_domain(self, cidade_model: CidadeModel) -> Cidade:
        """Convert Django model to domain aggregate."""
        plano = Plano(
            entity_id=cidade_model.plano.id,
            tipo=TipoPlano(cidade_model.plano.tipo),
            nome=cidade_model.plano.nome,
            descricao=cidade_model.plano.descricao,
        )

        usuarios = []
        async for usuario_model in cidade_model.usuarios.all():
            usuarios.append(
                UsuarioCidade(
                    entity_id=usuario_model.id,
                    user_id=usuario_model.user_id,
                    tipo=TipoUsuarioCidade(usuario_model.tipo),
                )
            )

        return Cidade(
            entity_id=cidade_model.id,
            nome=cidade_model.nome,
            cnpj=CNPJ(cidade_model.cnpj),
            plano=plano,
            limite_cameras=LimiteCameras(cidade_model.limite_cameras),
            usuarios=usuarios,
        )
