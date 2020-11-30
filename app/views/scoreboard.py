from flask import url_for, render_template
from app.models.events import Status
from flask_login import current_user
from werkzeug.utils import redirect
from app.views import bp


@bp.route('/scoreboard', methods=['GET', 'POST'])
def scoreboard():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    current_scores = current_user.get_current_scores()
    events_in_progress = []
    for sport in current_scores:
        for event in current_scores[sport]:
            if event.status == Status.STATUS_IN_PROGRESS:
                events_in_progress.append(event)
    return render_template('views/scoreboard.html', user=current_user,
                           scores=current_scores, events_in_progress=events_in_progress)
