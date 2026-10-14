def get_user_role(user_input):
    allowed_roles = ["admin", "editor", "viewer"]
    if user_input not in allowed_roles:
        raise ValueError("Invalid role")
    return user_input
