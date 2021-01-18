from app.api import bp
from app.models.user import User
from flask import request
import os


@bp.route('/auth/login', methods=['POST'])
def restful_login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    user = User.get_or_none(username=username)
    if user and user.check_password(password) and user.has_access:
        return {"success": os.environ.get('SECRET_KEY'), "version": "1.4"}
    else:
        return {"error": "invalid credentials"}
