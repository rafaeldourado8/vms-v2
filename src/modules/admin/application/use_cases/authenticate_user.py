"""Authenticate User Use Case."""
from src.modules.admin.application.dtos.authenticate_dto import AuthenticateDTO
from src.modules.admin.application.dtos.user_response_dto import UserResponseDTO
from src.modules.admin.domain.repositories.user_repository import IUserRepository
from src.modules.admin.domain.value_objects.email import Email
from src.shared.application.event_bus import EventBus
from src.shared.application.use_case import UseCase
from src.shared.domain.domain_exception import BusinessRuleViolationException


class AuthenticateUserUseCase(UseCase[AuthenticateDTO, UserResponseDTO]):
    """Use case for authenticating a user."""

    def __init__(self, user_repository: IUserRepository, event_bus: EventBus) -> None:
        """Initialize use case."""
        self.user_repository = user_repository
        self.event_bus = event_bus

    async def execute(self, input_dto: AuthenticateDTO) -> UserResponseDTO:
        """Execute use case."""
        email = Email(input_dto.email)
        user = await self.user_repository.find_by_email(email)

        if user is None:
            raise BusinessRuleViolationException("Invalid credentials")

        user.authenticate(input_dto.password)

        await self.user_repository.save(user)

        for event in user.domain_events:
            await self.event_bus.publish(event)

        user.clear_domain_events()

        return UserResponseDTO(
            id=user.id,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            roles=[role.code for role in user.roles],
        )
