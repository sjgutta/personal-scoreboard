from flask import Flask, render_template
from flask_caching import Cache
from peewee import MySQLDatabase
from flask_login import LoginManager
from flask_mail import Mail
import os


db = MySQLDatabase(os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"),
                   host=os.environ.get("DB_HOST"))
login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})
mail = Mail()

TEAM_CACHE_KEY = 'all_teams'


class Config(object):
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = [os.environ.get('MAIL_USERNAME')]
    SECRET_KEY = os.environ.get('SECRET_KEY')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    mail.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.views import bp as views_bp
    app.register_blueprint(views_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    cache_servers = os.environ.get('MEMCACHIER_SERVERS')

    if cache_servers is None:
        cache.init_app(app)
    else:
        cache_user = os.environ.get('MEMCACHIER_USERNAME') or ''
        cache_pass = os.environ.get('MEMCACHIER_PASSWORD') or ''
        cache_config = {
            'CACHE_TYPE': 'saslmemcached',
            'CACHE_MEMCACHED_SERVERS': cache_servers.split(','),
            'CACHE_MEMCACHED_USERNAME': cache_user,
            'CACHE_MEMCACHED_PASSWORD': cache_pass,
            'CACHE_OPTIONS': {'behaviors': {
                # Faster IO
                'tcp_nodelay': True,
                # Keep connection alive
                'tcp_keepalive': True,
                # Timeout for set/get requests
                'connect_timeout': 2000,  # ms
                'send_timeout': 750 * 1000,  # us
                'receive_timeout': 750 * 1000,  # us
                '_poll_timeout': 2000,  # ms
                # Better failover
                'ketama': True,
                'remove_failed': 1,
                'retry_timeout': 2,
                'dead_timeout': 30}
            }
        }
        cache.init_app(app, config=cache_config)

    @app.route('/')
    def index():
        return render_template('index.html')

    from app.models.team import Team
    all_teams = {f"{team.sport_type}-{team.espn_id}": team for team in Team.select()}
    cache.set(TEAM_CACHE_KEY, all_teams)

    return app


app = create_app()
