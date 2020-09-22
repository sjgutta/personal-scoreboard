from peewee import Model, IntegerField, ForeignKeyField
from app.models.fields import EnumField
from app.models.user import User
from services.espn.sports import Sport
from app import db


class Favorite(Model):
    """
    Represents a relationship between a user and a team.
    The team is one of the selected favorite teams for the user.
    The team field stores the id of the team in the ESPN API.
    The sport represents the sport of the team.
    """

    class Meta:
        database = db

    user = ForeignKeyField(User)
    team = IntegerField()
    sport_type = EnumField(Sport.SportType, max_length=64)
