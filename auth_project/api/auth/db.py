from api.auth.schemas import UserDataDto, UserRole
from api.models import Role, User

from .utils import EncodingPassword


class UserAccessDb:
    def save_user(self, username: str, password: str, email: str) -> None:
        role = Role.objects.filter(name="basic").first()
        hashed_password = EncodingPassword.set_password(password)
        user = User(
            username=username, password=hashed_password, role=role, email=email
        )
        user.save()

    def get_user(self, user_data: dict) -> UserDataDto | None:
        user = User.objects.filter(**user_data).first()
        if not user:
            return None

        role = UserRole.GUEST.value if not user.role else user.role.name
        return UserDataDto(
            user.username, user.password, UserRole(role), user.is_active
        )


class RoleAccessDb:
    def get_role(self, role_data) -> Role | None:
        return Role.objects.filter(**role_data).first()
