from .app import app, db
from .views import auth, index
from .models.user import load_user
from .models import *
from .templates import *
app.run()
