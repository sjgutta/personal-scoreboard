from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from app.models.user import User
from wtforms import StringField, validators, PasswordField, SubmitField
from flask_wtf import FlaskForm
from app.auth import bp


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.email(), validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(),
                                                     validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[validators.DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Request Password Reset')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.get_or_none(User.username == form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        if User.get_or_none(User.username == form.username.data) is not None:
            flash('A user with that username already exists')
            return redirect(url_for('auth.register'))
        if User.get_or_none(User.email == form.email.data) is not None:
            flash('A user with that email already exists')
            return redirect(url_for('auth.register'))
        user = User.create(username=form.username.data, email=form.email.data, is_admin=False)
        user.set_password(form.password.data)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    from app.email import send_password_reset_email

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.select().where(User.email == form.email.data)
        if user.exists():
            send_password_reset_email(user[0])
            flash('Check your email for the instructions to reset your password')
            return redirect(url_for('auth.login'))
        else:
            flash("No users exist with that email.")
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
