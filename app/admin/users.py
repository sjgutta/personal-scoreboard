from app.admin.base import BaseModelView


class UserAdmin(BaseModelView):
    column_list = ["id", "username", "email", "is_admin", "has_free_access", "expiration_date", "has_access"]
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]
    column_searchable_list = ["username", "email"]
