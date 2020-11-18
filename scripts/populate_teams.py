# This is a script to fill in the database teams table with the proper data
from services.espn.sports import Sport
from services.espn.teams import get_team_list
from app.models.team import Team


def populate_teams():
    for sport in Sport.SportType:
        team_list = get_team_list(sport)
        for team in team_list:
            Team.create(espn_id=team.id, sport_type=team.sport, full_name=team.full_name,
                        abbreviation=team.abbreviation, logo_url=team.logo_url)


if __name__ == "__main__":
    populate_teams()
