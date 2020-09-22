from flask_login import UserMixin
from peewee import CharField, Model, IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from app.models.team import Team


@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))


class User(Model, UserMixin):
    username = CharField()
    email = CharField()
    password_hash = CharField()

    class Meta:
        database = db

    def set_password(self, password):
        print(f"generating hash using {password}")
        self.password_hash = generate_password_hash(password)
        self.save()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"[User {self.id}] {self.email}"

    def get_favorites(self):
        """
        Get favorites for a user item.
        :return: list of favorite Team objects for the User.
        """
        from app.models.favorite import Favorite

        favorites = Favorite.select().where(Favorite.user == self)
        results = []

        for favorite in favorites:
            team = Team.get_team(favorite.sport_type, favorite.team)
            if team:
                results.append(team)

        return results

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
                        Favorite.create(user=self, team=team.id, sport_type=team.sport)
                    except IntegrityError:
                        continue
                    except Exception:
                        return False
        elif isinstance(teams, Team):
            try:
                Favorite.create(user=self, team=teams.id, sport_type=teams.sport)
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
                        Favorite.delete().where(Favorite.user == self,
                                                Favorite.team == team.id, Favorite.sport_type == team.sport).execute()
                    except Exception:
                        return False
        elif isinstance(teams, Team):
            team = teams
            try:
                Favorite.delete().where(Favorite.user == self,
                                        Favorite.team == team.id, Favorite.sport_type == team.sport).execute()
            except Exception:
                return False
        return True
