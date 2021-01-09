from app.admin.base import BaseModelView


class UserAdmin(BaseModelView):
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]
    column_searchable_list = ["username", "email"]
