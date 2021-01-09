from app.admin.base import BaseModelView
from markupsafe import Markup


class TeamAdmin(BaseModelView):
    column_list = ["id", "photo", "full_name", "sport_type", "espn_id", "abbreviation", "logo_url"]
    column_searchable_list = ["full_name"]

    def _photo(self, context, team, name):
        return Markup(f'<img style="height: 40px;" src="{team.logo_url}"/>')

    column_formatters = {
        "photo": _photo
    }
