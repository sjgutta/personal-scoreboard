from flask import Blueprint

bp = Blueprint('views', __name__)

from app.views import favorites
from app.views import scoreboard
from app.views import account
from app.views import payment
