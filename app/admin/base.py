from flask_admin.contrib.peewee import ModelView


# preparing this for later if admin expands
class BaseModelView(ModelView):
    can_delete = False
