from flask_admin import Admin
from flask_admin.menu import MenuLink
from app.admin.users import UserAdmin
from app.admin.teams import TeamAdmin


def create_admin():
    from app.models.user import User
    from app.models.team import Team

    scoreboard_admin = Admin()
    scoreboard_admin.add_view(UserAdmin(User, name="Users", endpoint="users"))
    scoreboard_admin.add_view(TeamAdmin(Team, name="Teams", endpoint="teams"))

    scoreboard_admin.add_link(MenuLink(name='Log Out', url="/logout", class_name='logout'))

    return scoreboard_admin
