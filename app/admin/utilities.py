from flask_admin import BaseView, expose
from flask import redirect, flash


class UtilitiesView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/utilities_index.html')

    @expose('/clear_teams_cache')
    def clear_teams_cache(self):
        from app import cache
        try:
            cache.delete('all_teams')
            flash("successfully deleted team cache", category="success")
        except Exception as e:
            flash(f"An error occurred: {e}", category="error")
        return redirect('/admin/utilities')
