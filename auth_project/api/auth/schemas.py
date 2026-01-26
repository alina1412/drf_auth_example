from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenDataDto:
    username: str
    expire: datetime


@dataclass
class TokenCheckedDataDto:
    token: str
    claims: TokenDataDto
    token_type: str
