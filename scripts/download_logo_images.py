import urllib.request
from services.espn.sports import Sport


def download_images():
    from app.models.team import Team

    print("running")
    teams = Team.select()
    print("found teams")
    for team in teams:
        print(team.full_name)
        logo_url = team.logo_url
        urllib.request.urlretrieve(logo_url, f"logo_images/{team.full_name}.png")


def download_ncaam_images():
    from app.models.team import Team

    print("running")
    teams = Team.select().where(Team.sport_type == Sport.SportType.NCAAM)
    print("found teams")
    for team in teams:
        print(team.full_name)
        logo_url = team.logo_url
        urllib.request.urlretrieve(logo_url, f"ncaam_logo_images/{team.full_name}.png")

def download_soccer_images():
    from app.models.team import Team

    print("running")
    teams = Team.select().where(Team.sport_type == Sport.SportType.SOCCER)
    print("found teams")
    for team in teams:
        print(team.full_name)
        logo_url = team.logo_url
        urllib.request.urlretrieve(logo_url, f"soccer_logo_images/{team.full_name}.png")

if __name__ == "__main__":
    download_images()
