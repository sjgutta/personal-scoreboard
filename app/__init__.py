from flask import Flask, render_template
from flask_caching import Cache
from peewee import MySQLDatabase
from flask_login import LoginManager
import os


db = MySQLDatabase(os.environ.get("DB_NAME"), user=os.environ.get("DB_USER"), password=os.environ.get("DB_PASSWORD"))
login_manager = LoginManager()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this-is-a-placeholder'

    login_manager.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.views import bp as views_bp
    app.register_blueprint(views_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    cache.init_app(app)

    @app.before_request
    def before_request():
        db.connect()

    @app.after_request
    def after_request(response):
        db.close()
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
