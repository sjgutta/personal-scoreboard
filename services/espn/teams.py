import requests
from services import ESPN_API_PREFIX
from services.espn.sports import Sport
from app.models.team import Team
from app.models.events import MLBEvent, NormalEvent


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
        away_data = team2_data
    else:
        home_data = team2_data
        away_data = team1_data
    status_data = event_data["header"]["competitions"][0]["status"]
    status = status_data["type"]["name"]
    away_team = Team.get_team(sport_type, away_data["id"], score=away_data["score"])
    home_team = Team.get_team(sport_type, home_data["id"], score=home_data["score"])
    if sport_type == Sport.SportType.MLB:
        if status == "STATUS_IN_PROGRESS":
            inning_string = status_data["type"]["detail"]
        else:
            inning_string = "FINAL"
        return MLBEvent(away_team, home_team, inning_string, status)
    else:

        period = status_data["period"] if status != "STATUS_FINAL" else None
        clock = status_data["displayClock"] if status != "STATUS_FINAL" else None
        return NormalEvent(away_team, home_team, period, clock, status)


if __name__ == "__main__":
    # team = Team.get_team(Sport.SportType.NBA, 19)
    # teams = get_team_list(Sport.SportType.NBA)
    # for team in teams:
    #     print(team)
    score = get_score_for_team(Sport.SportType.MLB, 19)
    print(score)
