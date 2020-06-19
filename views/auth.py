from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from ..models.user import User
from wtforms import StringField, validators, PasswordField
from flask_wtf import FlaskForm
from ..app import app


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.get_or_none(User.username == form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if User.get_or_none(User.username == form.username.data) is not None:
            flash('A user with that username already exists')
            return redirect(url_for('register'))
        user = User.create(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))