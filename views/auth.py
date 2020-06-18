from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user
from ..models.user import User
from wtforms import Form, StringField, validators
from ..app import app


class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = StringField('Password', validators=[validators.DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.get_or_none(User.username == form.username.data)
        if user is None or not user.check_password(form.password.data):
            print("failed and flashed")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register')
def register():
    return render_template('register.html')
