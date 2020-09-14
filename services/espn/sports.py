from enum import Enum


class Sport:
    class SportType(Enum):
        NBA = "NBA"
        MLB = "MLB"
        NFL = "NFL"
        NHL = "NHL"

    @classmethod
    def get_resource_url(cls, sport_type):
        if sport_type == Sport.SportType.NBA:
            return "/basketball/nba"
        elif sport_type == Sport.SportType.MLB:
            return "/baseball/mlb"
        elif sport_type == Sport.SportType.NFL:
            return "/football/nfl"
        elif sport_type == Sport.SportType.NHL:
            return "/hockey/nhl"
        else:
            return ""
