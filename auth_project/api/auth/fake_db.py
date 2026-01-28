from api.auth.schemas import UserDataDto, UserRole

fake_db = {
    "John Doe": {
        "username": "John Doe",
        "password": "$2b$12$QfU0BwNI.dJWJ/hEofl/SubOdQYVJ9SLr6qxbZQWiAuNe4yOZiXnS",
        # "is_admin": True,
        "role": "admin",
    },
    "joe": {
        "username": "joe",
        "password": "$2b$12$QfU0BwNI.dJWJ/hEofl/SubOdQYVJ9SLr6qxbZQWiAuNe4yOZiXnS",
        # "is_admin": False,
        "role": "basic",
    },
}


def get_user(username) -> UserDataDto | None:
    user = fake_db.get(username, {})
    if not user:
        return None
    user["role"] = UserRole(user["role"])
    return UserDataDto(**user)
