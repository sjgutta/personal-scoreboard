from flask import Flask, render_template
from peewee import MySQLDatabase
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)
app.config['SECRET_KEY'] = 'this-is-a-placeholder'


db = MySQLDatabase('sports_analytics_proj', user='root', password='***REMOVED***', host='localhost', port=3306)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response
