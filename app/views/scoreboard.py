from flask import url_for, render_template
from app.models.events import Status
from flask_login import current_user
from werkzeug.utils import redirect
from app.views import bp


@bp.route('/scoreboard', methods=['GET', 'POST'])
def scoreboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    current_scores, all_scores = current_user.get_current_scores()
    events_in_progress = [event for event in all_scores if event.status == Status.STATUS_IN_PROGRESS]
    return render_template('views/scoreboard.html', user=current_user,
                           scores=current_scores, all_score=all_scores, events_in_progress=events_in_progress)
