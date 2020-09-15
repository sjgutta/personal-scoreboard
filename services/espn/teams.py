import requests
from services import ESPN_API_PREFIX
from services.espn.sports import Sport
from app.models.team import Team
from app.models.events import MLBEvent, NormalEvent


def get_team_list(sport_type):
    """
    Takes in SportType Enum and gets a list of teams associated with it.
    :param sport_type: Should be of type SportType Enum, found within the Sport class in service/espn/sports.py
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
    for team in team_list:
        team_objects_list.append(Team(team["id"], team["displayName"], team["abbreviation"], sport_type))
    return team_objects_list


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
        away_data = team2_data
    else:
        home_data = team2_data
        away_data = team1_data
    away_team = Team.get_team(sport_type, away_data["id"], score=away_data["score"])
    home_team = Team.get_team(sport_type, home_data["id"], score=home_data["score"])
    if sport_type == Sport.SportType.MLB:
        return MLBEvent(away_team, home_team, 9, 2, "final")
    else:
        return NormalEvent(away_team, home_team, 4, "5:00", "final")


if __name__ == "__main__":
    # teams = get_team_list(Sport.SportType.NFL)
    # for team in teams:
    #     print(team)
    event = get_score_for_team(Sport.SportType.MLB, 8)
    # team = Team.get_team(Sport.SportType.NFL, 8)
    print(event)
