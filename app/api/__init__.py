from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import events
from app.api import auth
