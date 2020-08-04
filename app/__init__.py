from flask import Flask, render_template
from peewee import MySQLDatabase
from flask_login import LoginManager


db = MySQLDatabase('sports_analytics_proj', user='root', password='***REMOVED***', host='localhost', port=3306)
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'this-is-a-placeholder'

    login_manager.init_app(app)

    from app.auth import bp as views_bp
    app.register_blueprint(views_bp)

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
