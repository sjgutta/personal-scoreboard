from enum import Enum


class Status(Enum):
    STATUS_FINAL = "FINAL"
    STATUS_CANCELED = "CANCELED"
    STATUS_SCHEDULED = "SCHEDULED"
    STATUS_IN_PROGRESS = "IN PROGRESS"

    @classmethod
    def status_from_espn_string(cls, espn_string):
        if espn_string == "STATUS_FINAL":
            return cls.STATUS_FINAL
        elif espn_string == "STATUS_CANCELED":
            return cls.STATUS_CANCELED
        elif espn_string == "STATUS_SCHEDULED":
            return cls.STATUS_SCHEDULED
        else:
            return cls.STATUS_IN_PROGRESS


class NormalEvent:

    def __init__(self, away_team, home_team, quarter, time, status):
        self.status = Status.status_from_espn_string(status)
        self.away_team = away_team
        self.home_team = home_team
        self.quarter = quarter
        self.time = time

    @property
    def status_string(self):
        if self.status == Status.STATUS_FINAL:
            return "FINAL"
        elif self.status == Status.STATUS_CANCELED:
            return "CANCELED"
        elif self.status == Status.STATUS_SCHEDULED:
            return "UPCOMING"
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


class MLBEvent:

    def __init__(self, away_team, home_team, inning_string, status):
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
