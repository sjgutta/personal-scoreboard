import urllib.request


def download_images():
    from app.models.team import Team

    print("running")
    teams = Team.select()
    print("found teams")
    for team in teams:
        print(team.full_name)
        logo_url = team.logo_url
        urllib.request.urlretrieve(logo_url, f"logo_images/{team.full_name}.png")


if __name__ == "__main__":
    download_images()
