from flask import url_for, render_template
from flask_login import current_user
from werkzeug.utils import redirect
from app.views import bp


@bp.route('/account', methods=['GET', 'POST'])
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('views/account.html', user=current_user)
