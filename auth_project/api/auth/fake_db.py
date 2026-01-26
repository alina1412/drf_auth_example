fake_db = {
    "John Doe": {
        "username": "John Doe",
        "password": "$5$rounds=535000$ldGZ.MDfZ1ejbsNH$lnj5XF2WpS6CwQ..Oi3NrBev5KJVMT.YlJFERZuFsF3",
        "is_admin": True,
    },
    "joe": {
        "username": "joe",
        "password": "$5$rounds=535000$ldGZ.MDfZ1ejbsNH$lnj5XF2WpS6CwQ..Oi3NrBev5KJVMT.YlJFERZuFsF3",
        "is_admin": False,
    },
}


def get_user(username) -> dict:
    return fake_db.get(username, {})
