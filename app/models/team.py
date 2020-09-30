import json

import requests

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
