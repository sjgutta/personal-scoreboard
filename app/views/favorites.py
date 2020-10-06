from flask import url_for, render_template, request
from flask_login import current_user
from werkzeug.utils import redirect

from services.espn.sports import Sport
from services.espn.teams import get_all_sports_teams
from app.models.team import Team

from app.views import bp


@bp.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        new_favorites = request.form['current_favorites']
        new_favorites = new_favorites.split(",")
        favorite_team_objects = []
        for favorite in new_favorites:
            split_favorite_string = favorite.split("-")
            league = Sport.get_sport_type_by_value(split_favorite_string[0])
            if league:
                team = Team.get_team(league, split_favorite_string[1])
                if team:
                    favorite_team_objects.append(team)
        current_user.update_favorites(favorite_team_objects)
    user_favorites = current_user.get_favorites()
    other_teams = get_all_sports_teams(exclude=user_favorites)
    return render_template('views/favorites.html', user=current_user, favorites=user_favorites,
                           other_teams=other_teams, default_sport=Sport.SportType.NFL)
