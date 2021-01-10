from enum import Enum
from services import ESPN_API_PREFIX
from services.espn.sports import Sport
import requests


def get_espn_event_data(espn_event_id, sport_type, league=None):
    params = {"region": "us",
              "lang": "en",
              "contentorigin": "espn",
              "limit": "99"}
    event_id = espn_event_id
    params["event"] = event_id
    # now using the event_id to find the current score related info
    # scoreboard_url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/scoreboard"
    if sport_type == Sport.SportType.SOCCER:
        event_url = ESPN_API_PREFIX + Sport.get_resource_url(sport_type) + f"/{league}/summary"
        print(event_url)
        print(event_id)
    else:
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
    STATUS_POSTPONED = "POSTPONED"
    STATUS_FULL_TIME = "FULL TIME"

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
        elif espn_string == "STATUS_POSTPONED":
            return cls.STATUS_POSTPONED
        elif espn_string == "STATUS_FULL_TIME":
            return cls.STATUS_FULL_TIME
        else:
            return cls.STATUS_IN_PROGRESS


class BareEvent:
    def __init__(self, event_id, sport, league=None):
        self.id = event_id
        self.sport = sport
        self.league = league

    @property
    def relative_events_endpoint(self):
        if self.sport == Sport.SportType.SOCCER:
            return f"/api/events/SOCCER/{self.league}/{self.id}"
        else:
            return f"/api/events/{self.sport.value}/{self.id}"

    def to_dict(self):
        data = {
            "id": self.id,
            "sport": self.sport.value
        }
        if self.league:
            data["league"] = self.league
        return data


class BaseEvent:

    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day):
        self.id = event_id
        self.status = Status.status_from_espn_string(status)
        self.away_team = away_team
        self.scheduled_day = scheduled_day
        if self.status in [Status.STATUS_POSTPONED, Status.STATUS_SCHEDULED, Status.STATUS_CANCELED]:
            self.away_score = None
            self.home_score = None
        else:
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
            return self.scheduled_day
        elif self.status == Status.STATUS_HALFTIME:
            return "HALFTIME"
        elif self.status == Status.STATUS_POSTPONED:
            return "POSTPONED"
        else:
            if self.quarter == 5:
                return f"{self.time} | OT"
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
            if self.quarter == 5:
                return f"{self.time}\nOT\n{self.away_team.full_name}: {self.away_score}\n" \
                       f"{self.home_team.full_name}: {self.home_score}"
            else:
                return f"{self.time}\nQ{self.quarter}\n{self.away_team.full_name}: {self.away_score}\n" \
                       f"{self.home_team.full_name}: {self.home_score}"


class NFLEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day,
                 down, yardline, possession):
        self.down = down
        self.yardline = yardline
        if possession and int(possession) == away_team.espn_id:
            self.possession_team = away_team
        elif possession and int(possession) == home_team.espn_id:
            self.possession_team = home_team
        else:
            self.possession_team = None
        self.possession = possession
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day)

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
        if self.down and self.yardline:
            return f"{self.down} at {self.yardline}"
        else:
            return None

    def to_dict(self):
        data = {
            "id": self.id,
            "status": self.status.value,
            "status_string": self.status_string,
            "sport": "NFL",
            "espn_url": self.espn_url,
            "away_team": self.away_team.to_dict(),
            "home_team": self.home_team.to_dict(),
            "yardage_string": self.yardage_string,
            "away_score": self.away_score,
            "home_score": self.home_score
        }
        if self.home_team_ball:
            data["possession"] = "HOME"
        elif self.away_team_ball:
            data["possession"] = "AWAY"
        else:
            data["possession"] = None
        return data

    def current_play_status_string(self):
        return f"{self.home_team}: {self.down} at {self.yardline}"


class NBAEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day):
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day)

    def to_dict(self):
        data = {
            "id": self.id,
            "status": self.status.value,
            "status_string": self.status_string,
            "sport": "NBA",
            "espn_url": self.espn_url,
            "away_team": self.away_team.to_dict(),
            "home_team": self.home_team.to_dict(),
            "away_score": self.away_score,
            "home_score": self.home_score
        }
        return data

    @property
    def espn_url(self):
        return f"https://www.espn.com/nba/game?gameId={self.id}"


class NCAAMEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day):
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day)

    def to_dict(self):
        data = {
            "id": self.id,
            "status": self.status.value,
            "status_string": self.status_string,
            "sport": "NCAAM",
            "espn_url": self.espn_url,
            "away_team": self.away_team.to_dict(),
            "home_team": self.home_team.to_dict(),
            "away_score": self.away_score,
            "home_score": self.home_score
        }
        return data

    @property
    def status_string(self):
        if self.status == Status.STATUS_FINAL:
            return "FINAL"
        elif self.status == Status.STATUS_CANCELED:
            return "CANCELED"
        elif self.status == Status.STATUS_SCHEDULED:
            return self.scheduled_day
        elif self.status == Status.STATUS_HALFTIME:
            return "HALFTIME"
        elif self.status == Status.STATUS_POSTPONED:
            return "POSTPONED"
        else:
            if self.quarter == 5:
                return f"{self.time} | OT"
            else:
                return f"{self.time} | H{self.quarter}"

    @property
    def espn_url(self):
        return f"https://www.espn.com/mens-college-basketball/boxscore?gameId={self.id}"


class NHLEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day):
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day)

    def to_dict(self):
        data = {
            "id": self.id,
            "status": self.status.value,
            "status_string": self.status_string,
            "sport": "NHL",
            "espn_url": self.espn_url,
            "away_team": self.away_team.to_dict(),
            "home_team": self.home_team.to_dict(),
            "away_score": self.away_score,
            "home_score": self.home_score
        }
        return data

    @property
    def status_string(self):
        if self.status == Status.STATUS_FINAL:
            return "FINAL"
        elif self.status == Status.STATUS_CANCELED:
            return "CANCELED"
        elif self.status == Status.STATUS_SCHEDULED:
            return self.scheduled_day
        elif self.status == Status.STATUS_HALFTIME:
            return "HALFTIME"
        elif self.status == Status.STATUS_POSTPONED:
            return "POSTPONED"
        else:
            if self.quarter == 4:
                return f"{self.time} | OT"
            else:
                return f"{self.time} | P{self.quarter}"

    @property
    def espn_url(self):
        return f"https://www.espn.com/nhl/boxscore/_/gameId/{self.id}"


class MLBEvent:

    def __init__(self, event_id, away_team, away_score, home_team, home_score, inning_string, status, scheduled_day):
        self.id = event_id
        self.status = Status.status_from_espn_string(status)
        self.away_team = away_team
        self.away_score = away_score
        self.home_team = home_team
        self.home_score = home_score
        self.inning_string = inning_string
        self.scheduled_day = scheduled_day

    @property
    def status_string(self):
        if self.status == Status.STATUS_FINAL:
            return "FINAL"
        elif self.status == Status.STATUS_CANCELED:
            return "CANCELED"
        elif self.status == Status.STATUS_SCHEDULED:
            return self.scheduled_day
        elif self.status == Status.STATUS_HALFTIME:
            return "HALFTIME"
        else:
            return f"Inning: {self.inning_string}"

    def to_dict(self):
        data = {
            "id": self.id,
            "status": self.status.value,
            "status_string": self.status_string,
            "sport": "MLB",
            "espn_url": self.espn_url,
            "away_team": self.away_team.to_dict(),
            "home_team": self.home_team.to_dict(),
            "away_score": self.away_score,
            "home_score": self.home_score
        }
        return data

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


class SoccerEvent(BaseEvent):
    def __init__(self, event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day):
        super().__init__(event_id, away_team, away_score, home_team, home_score, quarter, time, status, scheduled_day)

    def to_dict(self):
        data = {
            "id": self.id,
            "status": self.status.value,
            "status_string": self.status_string,
            "sport": "SOCCER",
            "espn_url": self.espn_url,
            "away_team": self.away_team.to_dict(),
            "home_team": self.home_team.to_dict(),
            "away_score": self.away_score,
            "home_score": self.home_score
        }
        return data

    @property
    def status_string(self):
        if self.status == Status.STATUS_FINAL:
            return "FINAL"
        elif self.status == Status.STATUS_CANCELED:
            return "CANCELED"
        elif self.status == Status.STATUS_SCHEDULED:
            return self.scheduled_day
        elif self.status == Status.STATUS_HALFTIME:
            return "HALFTIME"
        elif self.status == Status.STATUS_POSTPONED:
            return "POSTPONED"
        elif self.status == Status.STATUS_FULL_TIME:
            return "FULL TIME"
        else:
            if self.quarter >= 3:
                return f"{self.time} | Extra Time"
            else:
                return f"{self.time} | H{self.quarter}"

    @property
    def espn_url(self):
        return f"https://www.espn.com/soccer/match?gameId={self.id}"

