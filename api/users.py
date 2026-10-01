from api.auth import hash_password


# =========================================================
# DEVELOPMENT USERS
# =========================================================

users = {

    "admin": {
        "username": "admin",
        "password": hash_password("admin123"),
        "role": "admin"
    },

    "analyst": {
        "username": "analyst",
        "password": hash_password("analyst123"),
        "role": "analyst"
    },

    "user": {
        "username": "user",
        "password": hash_password("user123"),
        "role": "user"
    }

}


# =========================================================
# GET USER
# =========================================================

def get_user(username: str):

    return users.get(username)