"""Add Usuario Cidade Use Case."""
from src.modules.cidades.application.dtos.add_usuario_cidade_dto import AddUsuarioCidadeDTO
from src.modules.cidades.application.dtos.cidade_response_dto import CidadeResponseDTO
from src.modules.cidades.domain.entities.usuario_cidade import TipoUsuarioCidade, UsuarioCidade
from src.modules.cidades.domain.repositories.cidade_repository import ICidadeRepository
from src.shared.application.use_case import UseCase
from src.shared.domain.domain_exception import EntityNotFoundException


class AddUsuarioCidadeUseCase(UseCase[AddUsuarioCidadeDTO, CidadeResponseDTO]):
    """Use case for adding usuario to cidade."""

    def __init__(self, cidade_repository: ICidadeRepository) -> None:
        """Initialize use case."""
        self.cidade_repository = cidade_repository

    async def execute(self, input_dto: AddUsuarioCidadeDTO) -> CidadeResponseDTO:
        """Execute use case."""
        cidade = await self.cidade_repository.find_by_id(input_dto.cidade_id)
        if cidade is None:
            raise EntityNotFoundException(f"Cidade not found: {input_dto.cidade_id}")

        tipo = TipoUsuarioCidade(input_dto.tipo)
        usuario = UsuarioCidade(user_id=input_dto.user_id, tipo=tipo)

        cidade.add_usuario(usuario)
        await self.cidade_repository.save(cidade)

        return CidadeResponseDTO(
            id=cidade.id,
            nome=cidade.nome,
            cnpj=cidade.cnpj.value,
            tipo_plano=cidade.plano.tipo.value if cidade.plano else "",
            dias_retencao=cidade.plano.dias_retencao if cidade.plano else 0,
            limite_cameras=cidade.limite_cameras.value,
            usuarios=[
                {"user_id": str(u.user_id), "tipo": u.tipo.value} for u in cidade.usuarios
            ],
        )
