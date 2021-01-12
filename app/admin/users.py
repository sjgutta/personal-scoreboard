from app.admin.base import BaseModelView
from markupsafe import Markup


class UserAdmin(BaseModelView):
    column_list = ["id", "username", "email", "is_admin", "has_free_access", "expiration_date", "has_access", "payment_link"]
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]
    column_searchable_list = ["username", "email"]

    def _payment_link(self, context, user, name):
        return Markup(f'<a href="{user.payment_intent_link}" target="_blank">{user.payment_intent}</a>')

    column_formatters = {
        "payment_link": _payment_link
    }
