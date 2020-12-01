from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from app.views import bp


@bp.route('/scoreboard', methods=['GET', 'POST'])
def scoreboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    current_scores = current_user.get_current_scores()
    last_sport = list(current_scores.keys())[-1]
    return render_template('views/scoreboard.html', user=current_user, scores=current_scores, last_sport=last_sport)
