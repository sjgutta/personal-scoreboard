from collections import defaultdict
import jwt
import datetime
from time import time
from flask_login import UserMixin
from peewee import CharField, Model, IntegrityError, BooleanField, DateField
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager, Config
from app.models.team import Team


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


class User(Model, UserMixin):
    username = CharField()
    email = CharField()
    password_hash = CharField()
    is_admin = BooleanField(default=False)
    has_free_access = BooleanField(default=False)
    expiration_date = DateField(null=True)
    payment_intent = CharField(null=True)

    class Meta:
        database = db

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.save()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            Config.SECRET_KEY, algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, Config.SECRET_KEY,
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.get(id=id)

    @property
    def has_access(self):
        if self.has_free_access:
            return True
        return bool(self.expiration_date and self.expiration_date >= datetime.date.today())

    @property
    def payment_intent_link(self):
        if self.payment_intent:
            return f"https://dashboard.stripe.com/test/payments/{self.payment_intent}"
        return "https://dashboard.stripe.com/payments"

    def __str__(self):
        return f"[User {self.id}] {self.email}"

    def get_favorites(self):
        """
        Get favorites for a user item.
        :return: list of favorite Team objects for the User.
        """
        from app.models.favorite import Favorite

        join_predicate = ((Team.espn_id == Favorite.team) & (Team.sport_type == Favorite.sport_type))

        favorites = Team.select().join(Favorite, on=join_predicate).where(Favorite.user_id == self.id)

        return favorites

    def update_favorites(self, new_favorites):
        """
        Takes a list of Team objects and sets the new set of favorites for the user to the list.
        This also removes any favorites that aren't in the new list.
        :param new_favorites: a list of Team objects to be the new favorites
        :return: None
        """
        current_favorites = self.get_favorites()
        current_favorites_tuples = [(team.espn_id, team.sport_type) for team in current_favorites]
        new_favorites_tuples = [(team.espn_id, team.sport_type) for team in new_favorites]
        remove_list = []
        add_list = []

        # finding favorites that must be removed
        for team in current_favorites:
            if (team.espn_id, team.sport_type) not in new_favorites_tuples:
                remove_list.append(team)

        # finding favorites that must be added
        for team in new_favorites:
            if (team.espn_id, team.sport_type) not in current_favorites_tuples:
                add_list.append(team)

        # removing old favorites and adding new ones
        self.add_favorite(add_list)
        self.remove_favorite(remove_list)

    def add_favorite(self, teams):
        """
        This function adds a team or list of teams as favorites for the user.
        :return: It returns True if successful, or False if an error occurred (other than adding a duplicate favorite).
        """
        from app.models.favorite import Favorite

        if isinstance(teams, list):
            for team in teams:
                if isinstance(team, Team):
                    try:
                        Favorite.create(user=self, team=team.espn_id, sport_type=team.sport_type)
                    except IntegrityError:
                        continue
                    except Exception:
                        return False
        elif isinstance(teams, Team):
            try:
                Favorite.create(user=self, team=teams.espn_id, sport_type=teams.sport_type)
            except IntegrityError:
                return True
            except Exception:
                return False
        return True

    def remove_favorite(self, teams):
        from app.models.favorite import Favorite

        if isinstance(teams, list):
            for team in teams:
                if isinstance(team, Team):
                    try:
                        Favorite.delete().where(Favorite.user == self, Favorite.team == team.espn_id,
                                                Favorite.sport_type == team.sport_type).execute()
                    except Exception:
                        return False
        elif isinstance(teams, Team):
            team = teams
            try:
                Favorite.delete().where(Favorite.user == self, Favorite.team == team.espn_id,
                                        Favorite.sport_type == team.sport_type).execute()
            except Exception:
                return False
        return True

    def get_current_scores(self):
        """
        This function is used for creating a list of sporting event objects that relate to the user's favorite teams.
        :return: A dict of Sport names to lists. Each list is a list of sporting event objects.
        """
        favorites = self.get_favorites()
        current_scores = defaultdict(list)
        event_ids = set()
        for team in favorites:
            team_sport = team.sport_type
            team_current_score = team.get_current_score()
            if team_current_score and team_current_score.id not in event_ids:
                current_scores[team_sport].append(team_current_score)
                event_ids.add(team_current_score.id)
        return dict(current_scores)

    def api_get_current_scores(self):
        """
        This function is used for creating a list of sporting event objects that relate to the user's favorite teams.
        It is used by the API to send json bare events to the macOS application.
        :return: A list of BareEvent objects in their json form.
        """
        favorites = self.get_favorites()
        current_scores = []
        event_ids = set()
        for team in favorites:
            team_current_score = team.get_current_score()
            if team_current_score and team_current_score.id not in event_ids:
                json_team_current_score = team_current_score.to_dict()
                current_scores.append(json_team_current_score)
                event_ids.add(team_current_score.id)
        return current_scores


if __name__ == "__main__":
    user = User.select().where(User.username == "test").get()
    favorites = user.get_favorites()
    for team in favorites:
        print(team)
