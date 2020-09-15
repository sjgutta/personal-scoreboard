
class NormalEvent:

    def __init__(self, away_team, home_team, quarter, time, status):
        self.away_team = away_team
        self.home_team = home_team
        self.quarter = quarter
        self.time = time
        self.status = status

    def __str__(self):
        if self.status == "final":
            return f"FINAL\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"
        else:
            return f"{self.time}\nQuarter: {self.quarter}\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"


class MLBEvent:

    def __init__(self, away_team, home_team, inning, outs, status):
        self.away_team = away_team
        self.home_team = home_team
        self.inning = inning
        self.outs = outs
        self.status = status

    def __str__(self):
        if self.status == "final":
            return f"FINAL\n{self.away_team.full_name}: {self.away_team.score}\n" \
                   f"{self.home_team.full_name}: {self.home_team.score}"
        else:
            return f"Inning: {self.inning} | {self.outs} outs\n{self.away_team.full_name}: " \
                   f"{self.away_team.score}\n{self.home_team.full_name}: {self.home_team.score}"
