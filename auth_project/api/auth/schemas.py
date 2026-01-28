from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class TokenDataDto:
    username: str
    expire: datetime
    role: str


@dataclass
class TokenCheckedDataDto:
    token: str
    claims: TokenDataDto
    token_type: str


class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    BASIC = "basic"
    GUEST = "guest"

    def __gt__(self, other):
        order = {
            UserRole.ADMIN: 4,
            UserRole.MANAGER: 3,
            UserRole.BASIC: 2,
            UserRole.GUEST: 1,
        }
        return order[self] > order[other]

    def __lt__(self, other):
        return not self.__gt__(other) and self != other

    def __ge__(self, other):
        return self.__gt__(other) or self == other

    def __le__(self, other):
        return self.__lt__(other) or self == other

    @classmethod
    def has_permission(
        cls, user_role: "UserRole", required_role: "UserRole"
    ) -> bool:
        """Check if user role meets minimum required role"""
        return user_role >= required_role


@dataclass
class UserDataDto:
    username: str
    password: str
    role: UserRole | None = None
    is_active: bool | None = None
