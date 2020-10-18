import json

import requests

from app.models.events import MLBEvent, NormalEvent, NFLEvent
from services.espn.sports import Sport
from services import ESPN_API_PREFIX


class Team:
    def __init__(self, espn_id, full_name, abbreviation, sport, logo_url, score=None):
        self.id = espn_id
        self.full_name = full_name
        self.abbreviation = abbreviation,
        self.sport = sport
        self.logo_url = logo_url
        if score:
            self.score = score

    def get_current_score(self):
        url = ESPN_API_PREFIX + Sport.get_resource_url(self.sport) + f"/teams/{self.id}"
        params = {"region": "us",
                  "lang": "en",
                  "contentorigin": "espn",
                  "limit": "99"}
        r = requests.get(url=url, params=params)
        data = r.json()
        event = data["team"]["nextEvent"][0]
        params["event"] = event["id"]

        # now using the event_id to find the current score related info
        # scoreboard_url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/scoreboard"
        event_url = ESPN_API_PREFIX + Sport.get_resource_url(self.sport) + f"/summary"
        event_r = requests.get(url=event_url, params=params)
        event_data = event_r.json()
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
        away_team = Team.get_team(self.sport, away_data["id"], score=away_data.get("score"))
        home_team = Team.get_team(self.sport, home_data["id"], score=home_data.get("score"))
        if self.sport == Sport.SportType.MLB:
            if status == "STATUS_IN_PROGRESS":
                inning_string = status_data["type"]["detail"]
            else:
                inning_string = "FINAL"
            return MLBEvent(away_team, home_team, inning_string, status)
        elif self.sport == Sport.SportType.NFL:
            if status == "STATUS_IN_PROGRESS":
                period = status_data["period"]
                clock = status_data["displayClock"]
                print(json.dumps(event_data["drives"]["current"]["plays"][-1], indent=2))
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
            return NFLEvent(away_team, home_team, period, clock, status, down, yardline, possession)
        else:
            if status == "STATUS_IN_PROGRESS":
                period = status_data["period"]
                clock = status_data["displayClock"]
            else:
                period = None
                clock = None
            return NormalEvent(away_team, home_team, period, clock, status)

    @classmethod
    def get_team(cls, league, team_id, score=None):
        url = ESPN_API_PREFIX + Sport.get_resource_url(league) + "/teams"
        params = {"region": "us",
                  "lang": "en",
                  "contentorigin": "espn",
                  "limit": "99"}
        r = requests.get(url=url, params=params)
        data = r.json()
        teams = [team["team"] for team in data["sports"][0]["leagues"][0]["teams"]]
        for team in teams:
            if team.get("id") == str(team_id):
                return Team(team["id"], team["displayName"], team["abbreviation"],
                            league, team["logos"][0]["href"], score=score)
        return None

    def __str__(self):
        return f"{self.full_name} [{self.id}]"


if __name__ == "__main__":
    team = Team.get_team(Sport.SportType.NFL, 8)
    print(team)
    game = team.get_current_score()
    print(game.current_play_status_string())
