from peewee import Model, IntegerField, CharField
from app.models.fields import EnumField
import requests
from app import db, cache
from app.models.events import BareEvent
from services.espn.sports import Sport
from services import ESPN_API_PREFIX


class Team(Model):
    """
    This is an object in the database with the information for a team.
    This is now being locally stored to speed up load times on the webapp.
    """

    class Meta:
        database = db

    espn_id = IntegerField()
    sport_type = EnumField(Sport.SportType, max_length=64)
    full_name = CharField(max_length=64)
    abbreviation = CharField(max_length=64)
    logo_url = CharField(max_length=255)

    def get_current_score(self):
        return BareEvent(self.current_event_id(), self.sport_type)

    @classmethod
    def get_team(cls, league, team_id):
        return Team.select().where(Team.sport_type == league, Team.espn_id == team_id).get()

    @cache.memoize(timeout=60 * 60 * 12)
    def current_event_id(self):
        url = ESPN_API_PREFIX + Sport.get_resource_url(self.sport_type) + f"/teams/{self.espn_id}"
        params = {"region": "us",
                  "lang": "en",
                  "contentorigin": "espn",
                  "limit": "99"}
        r = requests.get(url=url, params=params)
        data = r.json()
        event = data["team"]["nextEvent"][0]
        event_id = event["id"]
        return event_id

    def to_dict(self):
        data = {
            "id": self.espn_id,
            "sport": self.sport_type.value,
            "name": self.full_name,
            "abbreviation": self.abbreviation,
            "logo_url": self.logo_url
        }
        return data

    def __str__(self):
        return f"{self.full_name} [{self.espn_id}]"


if __name__ == "__main__":
    team = Team.get_team(Sport.SportType.NFL, 8)
    print(team)
    game = team.get_current_score()
    print(game.current_play_status_string())
