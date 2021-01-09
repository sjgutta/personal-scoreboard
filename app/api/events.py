from flask_login import current_user
import os
from app.api import bp
from services.espn.sports import Sport
from app.models.events import get_espn_event_data, NHLEvent, MLBEvent, NFLEvent, NBAEvent
from app.models.team import get_team, BareTeam
from app.models.user import User
from flask import request


def parse_event_data(sport_type, event_id, event_data):
    team1_data = event_data["header"]["competitions"][0]["competitors"][0]
    team2_data = event_data["header"]["competitions"][0]["competitors"][1]
    if team1_data["homeAway"] == "home":
        home_data = team1_data
        away_data = team2_data
    else:
        home_data = team2_data
        away_data = team1_data
    status_data = event_data["header"]["competitions"][0]["status"]
    status = status_data["type"]["name"]
    away_team = get_team(sport_type, away_data["id"])
    if away_team is None:
        away_team = BareTeam(away_data, sport_type)
    home_team = get_team(sport_type, home_data["id"])
    if home_team is None:
        home_team = BareTeam(home_data, sport_type)
    away_score = away_data.get("score")
    home_score = home_data.get("score")
    if sport_type == Sport.SportType.MLB:
        if status == "STATUS_IN_PROGRESS":
            inning_string = status_data["type"]["detail"]
        else:
            inning_string = "FINAL"
        return MLBEvent(event_id, away_team, away_score, home_team, home_score, inning_string, status)
    elif sport_type == Sport.SportType.NFL:
        if status == "STATUS_IN_PROGRESS":
            period = status_data["period"]
            clock = status_data["displayClock"]
            play = event_data["drives"]["current"]["plays"][-1]["end"]
            down = play.get("shortDownDistanceText")
            yardline = play.get("possessionText")
            possession = play["team"]["id"]
        else:
            period = None
            clock = None
            down = None
            yardline = None
            possession = None
        return NFLEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status, down, yardline,
                        possession)
    elif sport_type == Sport.SportType.NBA:
        if status == "STATUS_IN_PROGRESS":
            period = status_data["period"]
            clock = status_data["displayClock"]
        else:
            period = None
            clock = None
        return NBAEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status)
    elif sport_type == Sport.SportType.NHL:
        if status == "STATUS_IN_PROGRESS":
            period = status_data["period"]
            clock = status_data["displayClock"]
        else:
            period = None
            clock = None
        return NHLEvent(event_id, away_team, away_score, home_team, home_score, period, clock, status)


@bp.route('/events/<sport>/<int:event_id>', methods=['GET', 'POST'])
def get_espn_event_info(sport, event_id):
    if request.method == "GET" and current_user.is_authenticated:
        sport_enum = Sport.get_sport_type_by_value(sport)
        event_data = get_espn_event_data(event_id, sport_enum)
        event = parse_event_data(sport_enum, event_id, event_data)
        if event is None:
            return {}
        else:
            return event.to_dict()
    elif request.method == "POST":
        data = request.get_json()
        if data.get("secret_key") != os.environ.get('SECRET_KEY'):
            return "Not Authorized", 401
        sport_enum = Sport.get_sport_type_by_value(sport)
        event_data = get_espn_event_data(event_id, sport_enum)
        event = parse_event_data(sport_enum, event_id, event_data)
        if event is None:
            return {}
        else:
            return event.to_dict()
    else:
        return "Bad request", 400


@bp.route('/users/events', methods=['POST'])
def get_user_bare_events():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if data.get("secret_key") != os.environ.get('SECRET_KEY'):
        return "Not Authorized", 401
    user = User.get_or_none(username=username)
    if user and user.check_password(password):
        user_events = user.api_get_current_scores()
        return {"events": user_events}
    else:
        return {"error": "invalid credentials"}
