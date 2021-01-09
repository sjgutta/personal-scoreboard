from flask_admin import Admin
from app.admin.users import UserAdmin


def create_admin():
    from app.models.user import User

    scoreboard_admin = Admin()
    scoreboard_admin.add_view(UserAdmin(User, name="Users", endpoint="users"))

    return scoreboard_admin
