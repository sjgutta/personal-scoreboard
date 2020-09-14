
class Team:
    def __init__(self, espn_id, full_name, abbreviation, sport):
        self.id = espn_id
        self.full_name = full_name
        self.abbreviation = abbreviation,
        self.sport = sport

    def __str__(self):
        return f"{self.full_name} [{self.id}]"
