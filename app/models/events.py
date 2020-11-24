from enum import Enum
from services import ESPN_API_PREFIX
from services.espn.sports import Sport
import requests


def get_espn_event_data(espn_event_id, sport_type):
    params = {"region": "us",
              "lang": "en",
              "contentorigin": "espn",
              "limit": "99"}
    event_id = espn_event_id
    params["event"] = event_id
    # now using the event_id to find the current score related info
    # scoreboard_url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/scoreboard"
    event_url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/summary"
    event_r = requests.get(url=event_url, params=params)
    event_data = event_r.json()
    return event_data


class Status(Enum):
    STATUS_FINAL = "FINAL"
    STATUS_CANCELED = "CANCELED"
    STATUS_SCHEDULED = "SCHEDULED"
    STATUS_IN_PROGRESS = "IN PROGRESS"
    STATUS_HALFTIME = "HALFTIME"

    @classmethod
    def status_from_espn_string(cls, espn_string):
        if espn_string == "STATUS_FINAL":
            return cls.STATUS_FINAL
        elif espn_string == "STATUS_CANCELED":
            return cls.STATUS_CANCELED
        elif espn_string == "STATUS_SCHEDULED":
            return cls.STATUS_SCHEDULED
        elif espn_string == "STATUS_HALFTIME":
            return cls.STATUS_HALFTIME
        else:
            return cls.STATUS_IN_PROGRESS


class BaseEvent:

    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status):
        self.id = event_id
        self.status = Status.status_from_espn_string(status)
        self.away_team = away_team
        self.away_score = away_score
        self.home_score = home_score
        self.home_team = home_team
        self.quarter = quarter
        self.time = time

    @property
    def in_progess(self):
        return self.status == Status.STATUS_IN_PROGRESS

    @property
    def espn_url(self):
        return "www.espn.com"

    @property
    def status_string(self):
        if self.status == Status.STATUS_FINAL:
            return "FINAL"
        elif self.status == Status.STATUS_CANCELED:
            return "CANCELED"
        elif self.status == Status.STATUS_SCHEDULED:
            return "UPCOMING"
        elif self.status == Status.STATUS_HALFTIME:
            return "HALFTIME"
        else:
            return f"{self.time} | Q{self.quarter}"

    def __str__(self):
        if self.status == Status.STATUS_FINAL:
            return f"FINAL\n{self.away_team.full_name}: {self.away_score}\n" \
                   f"{self.home_team.full_name}: {self.home_score}"
        elif self.status == Status.STATUS_CANCELED:
            return f"CANCELED\n{self.away_team.full_name}: {self.away_score}\n" \
                   f"{self.home_team.full_name}: {self.home_score}"
        else:
            return f"{self.time}\nQ{self.quarter}\n{self.away_team.full_name}: {self.away_score}\n" \
                   f"{self.home_team.full_name}: {self.home_score}"


class NFLEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status, down, yardline, possession):
        self.down = down
        self.yardline = yardline
        if possession and int(possession) == away_team.espn_id:
            self.possession_team = away_team
        elif possession and int(possession) == home_team.espn_id:
            self.possession_team = home_team
        else:
            self.possession_team = None
        self.possession = possession
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status)

    @property
    def team_with_ball(self):
        if self.status != Status.STATUS_IN_PROGRESS:
            return None
        return self.possession_team

    @property
    def away_team_ball(self):
        return self.team_with_ball == self.away_team

    @property
    def home_team_ball(self):
        return self.team_with_ball == self.home_team

    @property
    def espn_url(self):
        return f"https://www.espn.com/nfl/game/_/gameId/{self.id}"

    @property
    def yardage_string(self):
        return f"{self.down} at {self.yardline}"

    def current_play_status_string(self):
        return f"{self.home_team}: {self.down} at {self.yardline}"


class NBAEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status):
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status)

    @property
    def espn_url(self):
        return f"https://www.espn.com/nba/game?gameId={self.id}"


class NHLEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status):
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status)

    @property
    def espn_url(self):
        return f"https://www.espn.com/nhl/boxscore/_/gameId/{self.id}"


class MLBEvent:

    def __init__(self, event_id, away_team, away_score, home_team, home_score, inning_string, status):
        self.id = event_id
        self.status = Status.status_from_espn_string(status)
        self.away_team = away_team
        self.away_score = away_score
        self.home_team = home_team
        self.home_score = home_score
        self.inning_string = inning_string

    @property
    def status_string(self):
        if self.status == Status.STATUS_FINAL:
            return "FINAL"
        elif self.status == Status.STATUS_CANCELED:
            return "CANCELED"
        elif self.status == Status.STATUS_SCHEDULED:
            return "UPCOMING"
        elif self.status == Status.STATUS_HALFTIME:
            return "HALFTIME"
        else:
            return f"Inning: {self.inning_string}"

    @property
    def espn_url(self):
        return f"https://www.espn.com/mlb/game?gameId={self.id}"

    def __str__(self):
        if self.status == Status.STATUS_FINAL:
            return f"FINAL\n{self.away_team.full_name}: {self.away_score}\n" \
                   f"{self.home_team.full_name}: {self.home_score}"
        elif self.status == Status.STATUS_CANCELED:
            return f"CANCELED\n{self.away_team.full_name}: {self.away_score}\n" \
                   f"{self.home_team.full_name}: {self.home_score}"
        else:
            return f"Inning: {self.inning_string}\n{self.away_team.full_name}: " \
                   f"{self.away_score}\n{self.home_team.full_name}: {self.home_score}"
