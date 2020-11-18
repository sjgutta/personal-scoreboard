import requests
from services import ESPN_API_PREFIX
from services.espn.sports import Sport
from app.models.events import NFLEvent, NBAEvent, NHLEvent, MLBEvent


class Team:
    """
    This team object is only used in the context of the ESPN service for managing team objects.
    The Peewee Model is used in all functions related to the webapp.
    """

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
        event_id = event["id"]
        params["event"] = event_id

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
        away_team = Team.get_team(self.sport, away_data["id"])
        home_team = Team.get_team(self.sport, home_data["id"])
        away_score = away_data.get("score")
        home_score = home_data.get("score")
        if self.sport == Sport.SportType.MLB:
            if status == "STATUS_IN_PROGRESS":
                inning_string = status_data["type"]["detail"]
            else:
                inning_string = "FINAL"
            return MLBEvent(event_id, away_team, away_score, home_team, home_score, inning_string, status)
        elif self.sport == Sport.SportType.NFL:
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
            return NFLEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status, down,
                            yardline, possession)
        elif self.sport == Sport.SportType.NBA:
            if status == "STATUS_IN_PROGRESS":
                period = status_data["period"]
                clock = status_data["displayClock"]
            else:
                period = None
                clock = None
            return NBAEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status)
        elif self.sport == Sport.SportType.NHL:
            if status == "STATUS_IN_PROGRESS":
                period = status_data["period"]
                clock = status_data["displayClock"]
            else:
                period = None
                clock = None
            return NHLEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status)

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


def get_team_list(sport_type, exclude=[]):
    """
    Takes in SportType Enum and gets a list of teams associated with it.
    :param sport_type: Should be of type SportType Enum, found within the Sport class in service/espn/sports.py
    :param exclude: list of teams objects to exclude from list
    :return: list of Team objects associated with the sport_type
    """
    url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + "/teams"
    params = {"region": "us",
              "lang": "en",
              "contentorigin": "espn",
              "limit": "99"}
    r = requests.get(url=url, params=params)
    data = r.json()
    team_list = [team["team"] for team in data["sports"][0]["leagues"][0]["teams"]]
    team_objects_list = []
    excluded_teams = [team.id for team in exclude if team.sport == sport_type]
    for team in team_list:
        if team["id"] not in excluded_teams:
            team_objects_list.append(Team(team["id"], team["displayName"], team["abbreviation"],
                                          sport_type, team["logos"][0]["href"]))
    return team_objects_list


def get_all_sports_teams(exclude=[]):
    team_data = {}
    for sport_type in Sport.SportType:
        team_data[sport_type.value] = get_team_list(sport_type, exclude)
    return team_data


def get_score_for_team(sport_type, team_id):
    url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/teams/{team_id}"
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
    event_url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/summary"
    event_r = requests.get(url=event_url, params=params)
    event_data = event_r.json()
    team1_data = event_data["header"]["competitions"][0]["competitors"][0]
    team2_data = event_data["header"]["competitions"][0]["competitors"][1]
    if team1_data["homeAway"] == "home":
        home_data = team1_data
    else:
        home_data = team2_data
    home_team = Team.get_team(sport_type, home_data["id"], score=home_data["score"])
    return home_team.get_current_score()


if __name__ == "__main__":
    # team = Team.get_team(Sport.SportType.NBA, 19)
    # teams = get_team_list(Sport.SportType.NBA)
    # for team in teams:
    #     print(team)
    score = get_score_for_team(Sport.SportType.MLB, 19)
    print(score)
