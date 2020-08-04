from flask_login import UserMixin
from peewee import CharField, Model
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


class User(Model, UserMixin):
    username = CharField()
    email = CharField()
    password_hash = CharField()

    class Meta:
        database = db

    def set_password(self, password):
        print(f"generating hash using {password}")
        self.password_hash = generate_password_hash(password)
        self.save()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
