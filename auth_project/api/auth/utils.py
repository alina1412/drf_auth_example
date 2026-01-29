import bcrypt
from auth_project.settings import logger


class EncodingPassword:
    @staticmethod
    def verify_password(password_in_db: str, raw_password: str) -> bool:
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), password_in_db.encode("utf-8")
        )

    @staticmethod
    def set_password(raw_password: str) -> str:
        password_hash = bcrypt.hashpw(
            raw_password.encode("utf-8"), bcrypt.gensalt()
        )
        return password_hash
