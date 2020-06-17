from flask import Flask, render_template

from .views.auth import bp as auth_bp

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % str(username)


app.register_blueprint(auth_bp)
