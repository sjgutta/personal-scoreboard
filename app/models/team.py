from peewee import Model, IntegerField, CharField
from app.models.fields import EnumField
import requests
from app import db, cache
from app.models.events import MLBEvent, NBAEvent, NHLEvent, NFLEvent, get_espn_event_data
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
        event_id = self.current_event_id()
        event_data = get_espn_event_data(event_id, self.sport_type)
        team1_data = event_data["header"]["competitions"][0]["competitors"][0]
        team2_data = event_data["header"]["competitions"][0]["competitors"][1]
        if team1_data["homeAway"] == "home":
            home_data = team1_data
            away_data = team2_data
        else:
            home_data = team2_data
            away_data = team1_data
        status_data = event_data["header"]["competitions"][0]["status"]
        status = status_data["type"]["name"]
        away_team = Team.get_team(self.sport_type, away_data["id"])
        home_team = Team.get_team(self.sport_type, home_data["id"])
        away_score = away_data.get("score")
        home_score = home_data.get("score")
        if self.sport_type == Sport.SportType.MLB:
            if status == "STATUS_IN_PROGRESS":
                inning_string = status_data["type"]["detail"]
            else:
                inning_string = "FINAL"
            return MLBEvent(event_id, away_team, away_score, home_team, home_score, inning_string, status)
        elif self.sport_type == Sport.SportType.NFL:
            if status == "STATUS_IN_PROGRESS":
                period = status_data["period"]
                clock = status_data["displayClock"]
                play = event_data["drives"]["current"]["plays"][-1]["end"]
                down = play.get("shortDownDistanceText")
                yardline = play.get("possessionText")
                possession = play["team"]["id"]
            else:
                period = None
                clock = None
                down = None
                yardline = None
                possession = None
            return NFLEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status, down, yardline, possession)
        elif self.sport_type == Sport.SportType.NBA:
            if status == "STATUS_IN_PROGRESS":
                period = status_data["period"]
                clock = status_data["displayClock"]
            else:
                period = None
                clock = None
            return NBAEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status)
        elif self.sport_type == Sport.SportType.NHL:
            if status == "STATUS_IN_PROGRESS":
                period = status_data["period"]
                clock = status_data["displayClock"]
            else:
                period = None
                clock = None
            return NHLEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status)

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
            "sport": self.sport_type,
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
