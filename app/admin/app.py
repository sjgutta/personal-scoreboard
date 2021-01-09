from flask_admin import Admin
from app.admin.users import UserAdmin
from app.admin.teams import TeamAdmin


def create_admin():
    from app.models.user import User
    from app.models.team import Team

    scoreboard_admin = Admin()
    scoreboard_admin.add_view(UserAdmin(User, name="Users", endpoint="users"))
    scoreboard_admin.add_view(TeamAdmin(Team, name="Teams", endpoint="teams"))

    return scoreboard_admin
