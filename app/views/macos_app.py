from flask import render_template
from flask_login import current_user
from app.views import bp


@bp.route('/macos-app', methods=['GET', 'POST'])
def macos_app():
    download_link = "https://github.com/sjgutta/personal-scoreboard/releases/latest/download/personal-scoreboard.zip"
    has_access = current_user.is_authenticated and current_user.has_access
    return render_template('views/macos_app.html', has_access=has_access, download_link=download_link)
