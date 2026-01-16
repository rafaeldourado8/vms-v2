"""Create User Use Case."""
from src.admin.application.dtos.create_user_dto import CreateUserDTO
from src.admin.application.dtos.user_response_dto import UserResponseDTO
from src.admin.domain.aggregates.user import User
from src.admin.domain.repositories.user_repository import IUserRepository
from src.admin.domain.value_objects.email import Email
from src.admin.domain.value_objects.password import Password
from src.shared_kernel.application.event_bus import EventBus
from src.shared_kernel.application.use_case import UseCase
from src.shared_kernel.domain.domain_exception import BusinessRuleViolationException


class CreateUserUseCase(UseCase[CreateUserDTO, UserResponseDTO]):
    """Use case for creating a user."""

    def __init__(self, user_repository: IUserRepository, event_bus: EventBus) -> None:
        """Initialize use case."""
        self.user_repository = user_repository
        self.event_bus = event_bus

    async def execute(self, input_dto: CreateUserDTO) -> UserResponseDTO:
        """Execute use case."""
        email = Email(input_dto.email)

        if await self.user_repository.email_exists(email):
            raise BusinessRuleViolationException(f"Email already exists: {email.value}")

        password = Password(input_dto.password)
        user = User.create(email, password, input_dto.name)

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
