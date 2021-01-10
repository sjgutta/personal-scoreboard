# This is a script to fill in the database teams table with the proper data
from services.espn.sports import Sport
from services.espn.teams import get_team_list
from app.models.team import Team
from services.espn.teams import Team as ESPNTeam
import requests


def populate_teams():
    for sport in Sport.SportType:
        team_list = get_team_list(sport)
        for team in team_list:
            Team.create(espn_id=team.id, sport_type=team.sport, full_name=team.full_name,
                        abbreviation=team.abbreviation, logo_url=team.logo_url)


def populate_ncaa_teams():
    useful_conferences = ["American Athletic Conference", "Atlantic Coast Conference", "Big 12 Conference",
                          "Big Ten Conference", "Pac-12 Conference", "Southeastern Conference"]
    url = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/groups"
    params = {"region": "us",
              "lang": "en",
              "contentorigin": "espn"}
    r = requests.get(url=url, params=params)
    data = r.json()
    groups = data["groups"][0]["children"]
    team_objects_list = []
    for group in groups:
        if group["name"] in useful_conferences:
            group_teams = group["teams"]
            for team in group_teams:
                team_objects_list.append(ESPNTeam(team["id"], team["displayName"], team["abbreviation"],
                                          Sport.SportType.NCAAM, team["logos"][0]["href"]))
    for team in team_objects_list:
        Team.create(espn_id=team.id, sport_type=team.sport, full_name=team.full_name,
                    abbreviation=team.abbreviation, logo_url=team.logo_url)


def populate_soccer_teams():
    params = {"region": "us",
              "lang": "en",
              "contentorigin": "espn"}

    league_abbreviations = ["ENG.1", "ITA.1", "ESP.1", "GER.1", "FRA.1"]
    team_objects_list = []
    for league in league_abbreviations:
        url = f"http://site.api.espn.com/apis/site/v2/sports/soccer/{league}/teams"
        r = requests.get(url=url, params=params)
        data = r.json()
        teams = data["sports"][0]["leagues"][0]["teams"]
        for team in teams:
            team = team["team"]
            team_objects_list.append(ESPNTeam(team["id"], team["displayName"], team["abbreviation"],
                                              Sport.SportType.SOCCER, team["logos"][0]["href"]))

    for team in team_objects_list:
        Team.create(espn_id=team.id, sport_type=team.sport, full_name=team.full_name,
                    abbreviation=team.abbreviation, logo_url=team.logo_url)


if __name__ == "__main__":
    # populate_teams()
    # populate_ncaa_teams()
    populate_soccer_teams()
