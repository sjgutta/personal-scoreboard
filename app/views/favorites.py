from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect

from services.espn.sports import Sport
from services.espn.teams import get_all_sports_teams

from app.views import bp


@bp.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user_favorites = current_user.get_favorites()
    other_teams = get_all_sports_teams(exclude=user_favorites)
    return render_template('views/favorites.html', user=current_user, favorites=user_favorites,
                           other_teams=other_teams, default_sport=Sport.SportType.NFL)
