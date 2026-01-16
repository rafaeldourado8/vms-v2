"""Assign Role Use Case."""
from src.admin.application.dtos.assign_role_dto import AssignRoleDTO
from src.admin.application.dtos.user_response_dto import UserResponseDTO
from src.admin.domain.repositories.role_repository import IRoleRepository
from src.admin.domain.repositories.user_repository import IUserRepository
from src.shared_kernel.application.use_case import UseCase
from src.shared_kernel.domain.domain_exception import EntityNotFoundException


class AssignRoleUseCase(UseCase[AssignRoleDTO, UserResponseDTO]):
    """Use case for assigning role to user."""

    def __init__(
        self, user_repository: IUserRepository, role_repository: IRoleRepository
    ) -> None:
        """Initialize use case."""
        self.user_repository = user_repository
        self.role_repository = role_repository

    async def execute(self, input_dto: AssignRoleDTO) -> UserResponseDTO:
        """Execute use case."""
        user = await self.user_repository.find_by_id(input_dto.user_id)
        if user is None:
            raise EntityNotFoundException(f"User not found: {input_dto.user_id}")

        role = await self.role_repository.find_by_code(input_dto.role_code)
        if role is None:
            raise EntityNotFoundException(f"Role not found: {input_dto.role_code}")

        user.add_role(role)
        await self.user_repository.save(user)

        return UserResponseDTO(
            id=user.id,
            email=user.email.value,
            name=user.name,
            is_active=user.is_active,
            roles=[r.code for r in user.roles],
        )
