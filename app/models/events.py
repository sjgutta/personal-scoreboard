from enum import Enum


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


class NormalEvent:

    def __init__(self, event_id, away_team, home_team, quarter, time, status):
        self.id = event_id
        self.status = Status.status_from_espn_string(status)
        self.away_team = away_team
        self.home_team = home_team
        self.quarter = quarter
        self.time = time

    @property
    def in_progess(self):
        return self.status == Status.STATUS_IN_PROGRESS

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
            return f"{self.time} | Quarter: {self.quarter}"

    def __str__(self):
        if self.status == Status.STATUS_FINAL:
            return f"FINAL\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"
        elif self.status == Status.STATUS_CANCELED:
            return f"CANCELED\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"
        else:
            return f"{self.time}\nQuarter: {self.quarter}\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"


class NFLEvent(NormalEvent):
    def __init__(self, event_id, away_team, home_team, quarter, time, status, down, yardline, possession):
        self.down = down
        self.yardline = yardline
        if possession and int(possession) == away_team.id:
            away_team.possession = True
        elif possession and int(possession) == home_team.id:
            home_team.possession = True
        self.possession = possession
        super().__init__(event_id, away_team, home_team, quarter, time, status)

    @property
    def team_with_ball(self):
        if self.status != Status.STATUS_IN_PROGRESS:
            return None
        if self.away_team.possession:
            return self.away_team
        elif self.home_team.possession:
            return self.home_team
        return None

    @property
    def yardage_string(self):
        return f"{self.down} at {self.yardline}"

    def current_play_status_string(self):
        return f"{self.home_team}: {self.down} at {self.yardline}"


class MLBEvent:

    def __init__(self, event_id, away_team, home_team, inning_string, status):
        self.id = event_id
        self.status = Status.status_from_espn_string(status)
        self.away_team = away_team
        self.home_team = home_team
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

    def __str__(self):
        if self.status == Status.STATUS_FINAL:
            return f"FINAL\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"
        elif self.status == Status.STATUS_CANCELED:
            return f"CANCELED\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"
        else:
            return f"Inning: {self.inning_string}\n{self.away_team.full_name}: " \
                   f"{self.away_team.score}\n{self.home_team.full_name}: {self.home_team.score}"
