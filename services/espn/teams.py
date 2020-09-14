import requests
from services import ESPN_API_PREFIX
from services.espn.sports import Sport
from app.models.team import Team


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


def get_events_for_team(sport_type, team_id):
    url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/teams/{team_id}"
    params = {"region": "us",
              "lang": "en",
              "contentorigin": "espn",
              "limit": "99"}
    r = requests.get(url=url, params=params)
    data = r.json()
    event = data["team"]["nextEvent"][0]
    team1 = event["competitions"][0]["competitors"][0]
    team2 = event["competitions"][0]["competitors"][1]
    if team1["homeAway"] == "home":
        home_team = team1
        away_team = team2
    else:
        home_team = team2
        away_team = team1
    print(f"{away_team['team']['displayName']}: {away_team['score']['displayValue']}\n"
          f"{home_team['team']['displayName']}: {home_team['score']['displayValue']}")


if __name__ == "__main__":
    teams = get_team_list(Sport.SportType.NFL)
    get_events_for_team(Sport.SportType.NFL, 8)
