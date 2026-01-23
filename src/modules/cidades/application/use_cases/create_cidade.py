"""Create Cidade Use Case."""
from src.modules.cidades.application.dtos.cidade_response_dto import CidadeResponseDTO
from src.modules.cidades.application.dtos.create_cidade_dto import CreateCidadeDTO
from src.modules.cidades.domain.aggregates.cidade import Cidade
from src.modules.cidades.domain.entities.plano import Plano, TipoPlano
from src.modules.cidades.domain.repositories.cidade_repository import ICidadeRepository
from src.modules.cidades.domain.value_objects.cnpj import CNPJ
from src.shared.application.event_bus import EventBus
from src.shared.application.use_case import UseCase
from src.shared.domain.domain_exception import BusinessRuleViolationException


class CreateCidadeUseCase(UseCase[CreateCidadeDTO, CidadeResponseDTO]):
    """Use case for creating cidade."""

    def __init__(self, cidade_repository: ICidadeRepository, event_bus: EventBus) -> None:
        """Initialize use case."""
        self.cidade_repository = cidade_repository
        self.event_bus = event_bus

    async def execute(self, input_dto: CreateCidadeDTO) -> CidadeResponseDTO:
        """Execute use case."""
        cnpj = CNPJ(input_dto.cnpj)

        if await self.cidade_repository.cnpj_exists(cnpj):
            raise BusinessRuleViolationException(f"CNPJ already exists: {cnpj.value}")

        tipo_plano = TipoPlano(input_dto.tipo_plano)
        plano = Plano(tipo=tipo_plano, nome=tipo_plano.value)

        cidade = Cidade.create(input_dto.nome, cnpj, plano)

        await self.cidade_repository.save(cidade)

        for event in cidade.domain_events:
            await self.event_bus.publish(event)

        cidade.clear_domain_events()

        return CidadeResponseDTO(
            id=cidade.id,
            nome=cidade.nome,
            cnpj=cidade.cnpj.value,
            tipo_plano=cidade.plano.tipo.value if cidade.plano else "",
            dias_retencao=cidade.plano.dias_retencao if cidade.plano else 0,
            limite_cameras=cidade.limite_cameras.value,
            usuarios=[],
        )
